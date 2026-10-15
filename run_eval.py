import json

def guess(email):
    text = email["body"].lower()
    if "quote" in text:
        return "customer_enquiry"
    if "leads" in text:
        return "sales_pitch"
    if "dispatched" in text:
        return "supplier"
    if "visit" in text:
        return "existing_customer"
    if "verify" in text:
        return "spam"
    if "install" in text:
        return "customer_enquiry"
    if "loan" in text:
        return "sales_pitch"
    if "invoice" in text:
        return "existing_customer"
    return "other"
if __name__ == "__main__":
    correct = 0
    total = 0

    with open("dataset.jsonl", encoding="utf-8") as f:
        for line in f:
            email = json.loads(line)
            answer = guess(email)
            total = total + 1
            if answer == email["expected"]:
                correct = correct + 1
            else:
                print("ОШИБКА в письме", email["id"], "- ответ:", answer, "правильно:", email["expected"])

    print("Точность:", correct, "из", total)