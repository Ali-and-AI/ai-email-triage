import json

CATEGORIES = ["customer_enquiry", "existing_customer", "sales_pitch", "supplier", "spam", "other"]

def parse_decision(raw):
    try:
        data = json.loads(raw)
        if data["category"] not in CATEGORIES:
            return {"category": "other", "confidence": 0.0, "reason": "unknown category", "needs_human": True}
        data["needs_human"] = data["confidence"] < 0.7
        return data
    except ValueError:
        return {"category": "other", "confidence": 0.0, "reason": "unparseable", "needs_human": True}

