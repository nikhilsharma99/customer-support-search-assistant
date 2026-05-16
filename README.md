# Customer Support Search Assistant

A small Python backend-style portfolio project that stores customer-support conversations and lets users search them by relevance.

This project demonstrates backend, data modeling, persistence, search logic, validation, and automated testing.

## Problem It Solves

Support teams often need to find useful information from many old customer conversations. Manually reading through previous messages is slow.

This project solves a simplified version of that problem by storing customer conversations and ranking the most relevant ones for a search query.

Example:

```text
Search: refund order
```

Result:

```text
Refund request - Maya
Customer asked how to get a refund after cancelling an order.
```

## Features

- Store customer-support conversations
- Search conversations by relevance
- Add new conversations from the terminal
- Show all saved conversations
- Save data into a JSON file
- Use a small TF-IDF style ranking algorithm
- Unit tests for the core logic

## Tech Stack

- Python
- Standard library only
- JSON persistence
- unittest

No external installation is required.

## Project Structure

```text
customer_support_search_assistant/
├── main.py
├── README.md
├── support_search/
│   ├── __init__.py
│   ├── models.py
│   ├── sample_data.py
│   ├── search.py
│   └── store.py
├── tests/
│   └── test_store.py
└── data/
    └── sample_conversations.json
```

## How to Run the Project

Open terminal inside the project folder and run:

```bash
python main.py
```

You will see:

```text
Customer Support Search Assistant
1. Search conversations
2. Add a new conversation
3. Show all conversations
4. Exit
```

Choose option `1` and try:

```text
refund order
```

Choose option `2` to add a new support conversation.

Choose option `3` to see all saved conversations.

## How to Run Tests

From the project folder, run:

```bash
python -m unittest discover tests
```

Expected result:

```text
Ran 9 tests

OK
```





