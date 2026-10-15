import json
from dotenv import load_dotenv
load_dotenv(override=True)

import anthropic
from classifier import parse_decision
from run_eval import guess
from ask_claude import SYSTEM

client = anthropic.Anthropic()

def ask_claude(email):
    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1000,
        system=SYSTEM,
        messages=[{"role": "user", "content": email["subject"] + "\n\n" + email["body"]}],
    )
    raw = next(block.text for block in response.content if block.type == "text")
    return parse_decision(raw)

keywords_ok = 0
claude_ok = 0
total = 0

with open("dataset.jsonl", encoding="utf-8") as f:
    for line in f:
        email = json.loads(line)
        total = total + 1

        kw = guess(email)
        ai = ask_claude(email)

        if kw == email["expected"]:
            keywords_ok = keywords_ok + 1
        if ai["category"] == email["expected"]:
            claude_ok = claude_ok + 1

        print(email["id"], "| правильно:", email["expected"], "| слова:", kw, "| Claude:", ai["category"])

print()
print("Ключевые слова:", keywords_ok, "из", total)
print("Claude:", claude_ok, "из", total)