#!/usr/bin/env python
import sys
import warnings
import os
from pathlib import Path
from dotenv import load_dotenv

from datetime import datetime

from coder.crew import Coder

# Load .env from repository root (/workspaces/crewai/.env)
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)
if not os.getenv('OPENAI_API_KEY'):
    print("WARNING: OPENAI_API_KEY not found in .env")
else:
    print("✓ API Key loaded successfully")

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

assignment = "Write a python program to calculate the sum of the first 10000" \
" series 1 -1/3 + 1/5 - 1/7 + ..."

def run():
    inputs = {"assignment": assignment}
    c = Coder()
    # Ensure configurations and agent/task mappings are loaded
    c.load_configurations()
    c.map_all_agent_variables()
    c.map_all_task_variables()
    results = c.crew().kickoff(inputs=inputs)
    print(results)

if __name__ == "__main__":
    run()