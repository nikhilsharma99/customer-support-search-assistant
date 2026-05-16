from __future__ import annotations

from support_search.sample_data import seed_sample_data
from support_search.store import ConversationStore


def print_menu() -> None:
    print("\nCustomer Support Search Assistant")
    print("1. Search conversations")
    print("2. Add a new conversation")
    print("3. Show all conversations")
    print("4. Exit")


def search_conversations(store: ConversationStore) -> None:
    query = input("Search query: ").strip()
    results = store.search(query)

    if not results:
        print("No matching conversations found.")
        return

    print("\nSearch results:")
    for result in results:
        print(
            f"[score: {result['score']}] "
            f"#{result['id']} {result['topic']} - {result['customer_name']}"
        )
        print(f"  {result['message']}")


def add_conversation(store: ConversationStore) -> None:
    customer_name = input("Customer name: ").strip()
    topic = input("Topic: ").strip()
    message = input("Message: ").strip()

    try:
        conversation = store.add_conversation(customer_name, topic, message)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"Conversation added with ID #{conversation.id}.")


def show_all_conversations(store: ConversationStore) -> None:
    conversations = store.list_conversations()

    if not conversations:
        print("No conversations saved yet.")
        return

    print("\nSaved conversations:")
    for conversation in conversations:
        print(f"#{conversation.id} {conversation.topic} - {conversation.customer_name}")
        print(f"  {conversation.message}")


def main() -> None:
    store = ConversationStore()
    seed_sample_data(store)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            search_conversations(store)
        elif choice == "2":
            add_conversation(store)
        elif choice == "3":
            show_all_conversations(store)
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
