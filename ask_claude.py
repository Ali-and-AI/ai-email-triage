from dotenv import load_dotenv
load_dotenv(override=True)

import anthropic
from classifier import parse_decision

client = anthropic.Anthropic()

SYSTEM = """You sort emails for a UK electrical contractor.
Choose exactly one category:
- customer_enquiry: someone asking for electrical work or a quote
- existing_customer: a current client about an ongoing job or invoice
- sales_pitch: someone selling a service to the contractor, even if disguised as an enquiry
- supplier: a supplier about orders, deliveries or prices
- spam: phishing or scams
- other: anything else

Reply with JSON only, no other text:
{"category": "...", "confidence": 0.0-1.0, "reason": "one short sentence"}"""

if __name__ == "__main__":
    
    email = "Hi, I would like a quote for your website. We can rebuild it for 499 pounds."

    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=200,
        system=SYSTEM,
        messages=[{"role": "user", "content": email}],
    )

    raw = next(block.text for block in response.content if block.type == "text")
    print("Claude сказал:", raw)

    decision = parse_decision(raw)
    print("Охранник решил:", decision)