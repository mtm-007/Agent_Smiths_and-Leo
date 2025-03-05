#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import PdfRag
import agentops
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """

    user_input = input("Enter your question/Query here: ")
    inputs = {
        'input': user_input
    }

    try:
        result = PdfRag().crew().kickoff(inputs=inputs)
        print(result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == '__main__':
    session= agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))
    run()
    session.end_session()
