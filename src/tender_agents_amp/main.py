import json
import os

from tender_agents_amp.crew import TenderAgentsAmp


def run():
    raw_inputs = os.getenv("CREW_INPUTS", "{}")

    try:
        inputs = json.loads(raw_inputs)
    except Exception:
        inputs = {}

    result = TenderAgentsAmp().crew().kickoff(inputs=inputs)
    print(result)


def run_crew():
    run()


if __name__ == "__main__":
    run()
    # run_crew()    
