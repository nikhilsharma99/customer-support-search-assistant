def generate_ticket_summary(issue_description, category, priority, status):
    return (
        f"This ticket is about a {category.lower()} issue. "
        f"The customer reported: {issue_description} "
        f"The ticket priority is {priority.lower()} and the current status is {status.lower()}."
    )


def suggest_reply(issue_description, category, priority):
    issue_lower = str(issue_description).lower()

    if "refund" in issue_lower or "payment" in issue_lower or "billing" in issue_lower:
        return (
            "Thank you for contacting us. We understand your concern regarding the payment or refund. "
            "Our support team will review the details and provide an update as soon as possible."
        )

    if "password" in issue_lower or "login" in issue_lower or "account" in issue_lower:
        return (
            "Thank you for reaching out. Please try resetting your password and checking your login details. "
            "If the issue continues, we will help you restore access to your account."
        )

    if "crash" in issue_lower or "error" in issue_lower or "bug" in issue_lower:
        return (
            "Thank you for reporting this technical issue. Please share any error message or steps to reproduce it. "
            "Our team will investigate and help resolve it."
        )

    return (
        "Thank you for contacting support. We have received your request and will review the issue. "
        "Our team will get back to you with the next steps."
    )
    
def detect_sentiment(issue_description):
    text = str(issue_description).lower()

    negative_words = [
        "angry", "bad", "broken", "crash", "error", "failed",
        "issue", "problem", "delay", "delayed", "refund",
        "complaint", "not working", "cannot", "unable"
    ]

    positive_words = [
        "thanks", "thank you", "great", "good", "resolved",
        "happy", "helpful", "excellent", "satisfied"
    ]

    negative_score = sum(word in text for word in negative_words)
    positive_score = sum(word in text for word in positive_words)

    if negative_score > positive_score:
        return "Negative"
    elif positive_score > negative_score:
        return "Positive"
    else:
        return "Neutral"