from google import genai
from google.genai import types

client = genai.Client()

email = "Hi, I would like a quote for your website. We can rebuild it for 499 pounds."

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=email,
    config=types.GenerateContentConfig(
        system_instruction="You sort emails for a UK electrician. Is this email from a real customer or a sales pitch? Answer in one sentence.",
    ),
)

print(response.text)