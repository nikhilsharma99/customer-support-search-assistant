from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Dict, List, Optional

from support_search.models import Conversation
from support_search.search import (
    calculate_document_frequency,
    cosine_similarity,
    tf_idf_vector,
    tokenize,
)


class ConversationStore:
    """
    Stores conversations in a JSON file.

    This is the project database layer. It can later be replaced by SQLite,
    PostgreSQL, or a backend API without changing the whole application.
    """

    def __init__(self, file_path: str = "data/support_conversations.json"):
        self.file_path = file_path
        self.conversations: List[Conversation] = []
        self._load()

    def _load(self) -> None:
        """Load conversations from disk if the JSON file exists."""
        if not os.path.exists(self.file_path):
            self.conversations = []
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                raw_items = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON database file: {self.file_path}") from error

        self.conversations = [Conversation(**item) for item in raw_items]

    def _save(self) -> None:
        """Save all conversations to disk."""
        folder = os.path.dirname(self.file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [asdict(conversation) for conversation in self.conversations],
                file,
                indent=2,
            )

    def add_conversation(self, customer_name: str, topic: str, message: str) -> Conversation:
        """Validate and store a new support conversation."""
        self._validate_input(customer_name, topic, message)

        conversation = Conversation(
            id=self._next_id(),
            customer_name=customer_name.strip(),
            topic=topic.strip(),
            message=message.strip(),
        )

        self.conversations.append(conversation)
        self._save()
        return conversation

    def list_conversations(self) -> List[Conversation]:
        """Return all stored conversations."""
        return list(self.conversations)

    def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """Find one conversation by ID."""
        for conversation in self.conversations:
            if conversation.id == conversation_id:
                return conversation
        return None

    def search(self, query: str, limit: int = 5) -> List[Dict[str, object]]:
        """
        Search conversations using a simple TF-IDF style ranking.

        This is not full semantic AI search. It is a clear baseline algorithm
        that is easy to explain in an interview.
        """
        if limit <= 0:
            return []

        query_tokens = tokenize(query)
        if not query_tokens or not self.conversations:
            return []

        document_tokens = [
            tokenize(conversation.searchable_text())
            for conversation in self.conversations
        ]

        document_frequency = calculate_document_frequency(document_tokens)
        total_documents = len(document_tokens)
        query_vector = tf_idf_vector(
            query_tokens,
            document_frequency,
            total_documents,
        )

        ranked_results: List[Dict[str, object]] = []

        for conversation, tokens in zip(self.conversations, document_tokens):
            document_vector = tf_idf_vector(
                tokens,
                document_frequency,
                total_documents,
            )
            score = cosine_similarity(query_vector, document_vector)

            if score > 0:
                ranked_results.append(
                    {
                        "id": conversation.id,
                        "customer_name": conversation.customer_name,
                        "topic": conversation.topic,
                        "message": conversation.message,
                        "score": round(score, 4),
                    }
                )

        ranked_results.sort(key=lambda item: item["score"], reverse=True)
        return ranked_results[:limit]

    def _next_id(self) -> int:
        """Generate the next conversation ID."""
        if not self.conversations:
            return 1
        return max(conversation.id for conversation in self.conversations) + 1

    @staticmethod
    def _validate_input(customer_name: str, topic: str, message: str) -> None:
        """Validate required fields before storing a conversation."""
        if not isinstance(customer_name, str) or not customer_name.strip():
            raise ValueError("customer_name is required")
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("topic is required")
        if not isinstance(message, str) or len(message.strip()) < 5:
            raise ValueError("message must contain at least 5 characters")
