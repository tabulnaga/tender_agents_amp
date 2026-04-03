#!/usr/bin/env python
import json
import sys
import warnings
from datetime import datetime

from tender_agents_amp.crew import TenderAgentsAmp

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def build_default_inputs() -> dict:
    return {
        "purchase_request_id": "PR-1001",
        "requester": "Nora",
        "vendor": "Acme Analytics",
        "amount_usd": 18000,
        "currency": "USD",
        "purpose": "Annual BI license renewal",
        "urgency": "high",
        "reviewer_user_id": "manager-01",
        "reviewer_email": "manager@example.com",
        "current_year": str(datetime.now().year),
    }


def run():
    inputs = build_default_inputs()
    try:
        result = TenderAgentsAmp().crew().kickoff(inputs=inputs)
        print(result)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    inputs = build_default_inputs()
    try:
        TenderAgentsAmp().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    try:
        TenderAgentsAmp().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    inputs = build_default_inputs()
    try:
        TenderAgentsAmp().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = build_default_inputs()
    inputs["crewai_trigger_payload"] = trigger_payload

    try:
        result = TenderAgentsAmp().crew().kickoff(inputs=inputs)
        print(result)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")


if __name__ == "__main__":
    run()