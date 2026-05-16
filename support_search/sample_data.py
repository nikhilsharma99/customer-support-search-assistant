from __future__ import annotations

from support_search.store import ConversationStore


def seed_sample_data(store: ConversationStore) -> None:
    """Add sample conversations only when the store is empty."""
    if store.list_conversations():
        return

    store.add_conversation(
        customer_name="Maya",
        topic="Refund request",
        message="Customer asked how to get a refund after cancelling an order.",
    )
    store.add_conversation(
        customer_name="Jonas",
        topic="Password reset",
        message="Customer cannot access the account and needs a password reset link.",
    )
    store.add_conversation(
        customer_name="Amina",
        topic="Shipping delay",
        message="Customer wants an update because the package delivery is delayed.",
    )
    store.add_conversation(
        customer_name="Lukas",
        topic="Subscription cancellation",
        message="Customer asked how to cancel the monthly subscription plan.",
    )
