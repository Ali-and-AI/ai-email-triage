from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic()

email = "Hi, I would like a quote for your website. We can rebuild it for 499 pounds."

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=200,
    system="You sort emails for a UK electrician. Is this email from a real customer or a sales pitch? Answer in one sentence.",
    messages=[{"role": "user", "content": email}],
)

print(response.content[0].text)