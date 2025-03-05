#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from pydub import AudioSegment
from pydub.utils import make_chunks
from openai import OpenAI
from pathlib import Path

from crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew
from crews.gmailcrew.gmailcrew import GmailCrew

import agentops
import os

from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

class MeetingMinutesState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""


class MeetingMinutesFlow(Flow[MeetingMinutesState]):

    @start()
    def transcribe_meeting(self):
        print("Generating Transcription")

        SCRIPT_DIR = Path(__file__).parent
        #audio_path = str(SCRIPT_DIR/ 'Earnings Call (1).wav' )
        audio_path = SCRIPT_DIR/ 'First_Applied_LLM_office_hour_of_2025.wav'
        transcript_path = SCRIPT_DIR / f"{audio_path.stem}_transcript.txt"

        if transcript_path.exists():
            print(f"Transcript for the source found at {transcript_path}, loading ...")
            with open(transcript_path, "r") as file:
                self.state.transcript = file.read()
            print(f"Transcript loaded succesfully.")
        else:
            print(f"No existing transcript found. Starting Transcription...")
            audio = AudioSegment.from_file(audio_path, format = 'wav')

            chunk_length_ms = 60000 # 1 minute = 60,000 ms
            chunks = make_chunks(audio, chunk_length_ms)

            full_transcription = ""
            save_chunks = False

            for i,chunk in enumerate(chunks):
                print(f"Transcribing chunks {i+1}/{len(chunks)}")
                chunk_path = f"chunk_{i}.wav"
                chunk.export(chunk_path, format="wav")

                with open(chunk_path, "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                    full_transcription += transcription.text + " "

                if not save_chunks:
                    os.remove(chunk_path)
                    print(f"Deleted {chunk_path}")

            self.state.transcript = full_transcription
            #print(f"Transcription: {self.state.transcript}")
            with open(transcript_path, "w") as file:
                file.write(self.state.transcript)
            print(f"Transcription completed and saved to {transcript_path}")


    @listen(transcribe_meeting)
    def generate_meeting_minutes(self):
        print("Generating meeting minutes..")

        crew = MeetingMinutesCrew()

        inputs = {
            "transcript" : self.state.transcript
        }
        meeting_minutes = crew.crew().kickoff(inputs)
        self.state.meeting_minutes = meeting_minutes

    @listen(generate_meeting_minutes)
    def create_draft_meeting_minutes(self):
        print("Creating Draft meeting minutes")

        crew = GmailCrew()

        meeting_minutes_content = str(self.state.meeting_minutes)

        inputs = {
            #"body": self.state.meeting_minutes
            "body": meeting_minutes_content
        }
        draft_crew = crew.crew().kickoff(inputs)
        print(f"Draft crew: {draft_crew}")

def kickoff():
    session= agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))

    #session =agentops.start_session()

    meeting_minutes_flow = MeetingMinutesFlow(session=session)
    meeting_minutes_flow.plot()
    meeting_minutes_flow.kickoff()

    session.end_session(end_state='Success')

if __name__ == "__main__":
    kickoff()
