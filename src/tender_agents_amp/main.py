#!/usr/bin/env python
from tender_agents_amp.crew import TenderAgentsAmp


def run():
    inputs = {
        "topic": "Purchase Request Approval",
        "current_year": "2026",
        "purchase_request_id": 1,
        "requester": "John Doe",
        "vendor": "Dell",
        "amount_usd": 2500,
        "currency": "USD",
        "purpose": "Purchase of laptop for engineering team",
        "urgency": "High",
        "reviewer_user_id": "manager1",
        "reviewer_email": "manager@example.com",
    }

    result = TenderAgentsAmp().crew().kickoff(inputs=inputs)
    print(result)


if __name__ == "__main__":
    run()
