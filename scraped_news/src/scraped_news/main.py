#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import ScrapedNews

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # inputs = {
    #     'topic': 'AI Agents',
    #     'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # }

    inputs_array = [
        {
            'topic': 'Andrej Karpathy about AI Agents',
            'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        },
        {
            'topic': 'Andrej Karpathy about recent developments in LLM Training',
            'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        },
        {
            'topic': 'Andrej Karpathy about Reinforcement learning used in training SOTA LLM',
            'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        }
    ]


    try:
        #for inputs in inputs_array:
        ScrapedNews().crew().kickoff_for_each(inputs=inputs_array)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()
