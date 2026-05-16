import os
import tempfile
import unittest

from support_search.search import tokenize
from support_search.store import ConversationStore


class TestConversationStore(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, "test_conversations.json")
        self.store = ConversationStore(self.file_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_conversation(self):
        conversation = self.store.add_conversation(
            customer_name="Maya",
            topic="Refund request",
            message="Customer wants a refund for a cancelled order.",
        )

        self.assertEqual(conversation.id, 1)
        self.assertEqual(conversation.customer_name, "Maya")
        self.assertEqual(len(self.store.list_conversations()), 1)

    def test_validation_rejects_empty_customer_name(self):
        with self.assertRaises(ValueError):
            self.store.add_conversation(
                customer_name=" ",
                topic="Refund request",
                message="Customer wants a refund.",
            )

    def test_search_returns_relevant_result(self):
        self.store.add_conversation(
            customer_name="Maya",
            topic="Refund request",
            message="Customer wants a refund for a cancelled order.",
        )
        self.store.add_conversation(
            customer_name="Jonas",
            topic="Password reset",
            message="Customer cannot log in and needs a password reset link.",
        )

        results = self.store.search("reset password login")

        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["topic"], "Password reset")

    def test_search_returns_empty_list_for_blank_query(self):
        self.store.add_conversation(
            customer_name="Amina",
            topic="Shipping delay",
            message="Customer wants an update about delayed delivery.",
        )

        results = self.store.search("   ")

        self.assertEqual(results, [])

    def test_data_is_saved_and_reloaded(self):
        self.store.add_conversation(
            customer_name="Lukas",
            topic="Subscription cancellation",
            message="Customer asked how to cancel a monthly subscription.",
        )

        reloaded_store = ConversationStore(self.file_path)

        self.assertEqual(len(reloaded_store.list_conversations()), 1)
        self.assertEqual(
            reloaded_store.list_conversations()[0].topic,
            "Subscription cancellation",
        )

    def test_get_conversation_returns_correct_item(self):
        conversation = self.store.add_conversation(
            customer_name="Nina",
            topic="Account access",
            message="Customer needs help accessing the account.",
        )

        found = self.store.get_conversation(conversation.id)

        self.assertIsNotNone(found)
        self.assertEqual(found.customer_name, "Nina")

    def test_search_respects_limit(self):
        self.store.add_conversation("A", "Refund one", "Customer asked about refund one.")
        self.store.add_conversation("B", "Refund two", "Customer asked about refund two.")
        self.store.add_conversation("C", "Refund three", "Customer asked about refund three.")

        results = self.store.search("refund", limit=2)

        self.assertEqual(len(results), 2)

    def test_search_returns_empty_when_limit_is_zero(self):
        self.store.add_conversation(
            customer_name="Omar",
            topic="Refund request",
            message="Customer asked about a refund.",
        )

        results = self.store.search("refund", limit=0)

        self.assertEqual(results, [])

    def test_tokenize_handles_none(self):
        self.assertEqual(tokenize(None), [])


if __name__ == "__main__":
    unittest.main()
