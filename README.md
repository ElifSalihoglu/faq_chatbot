# FAQ Chatbot Project

A chatbot application that retrieves answers to user queries using embeddings and Pinecone for vector search.

---

## Features
- Scrapes FAQ data from a specified URL.
- Generates embeddings using SentenceTransformer.
- Stores embeddings in a Pinecone vector database.
- Matches user queries with FAQ entries.

---

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ElifSalihoglu/faq_chatbot.git
   cd faq_chatbot
   ```

2. **Install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set environment variables**:
   Create a `.env` file:
   ```env
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   INDEX_NAME=faq_index
   ```

4. **Create a data folder**:
   ```bash
   mkdir data
   ```

---

## Usage

1. **Run the chatbot**:
   ```bash
   python main.py
   ```

2. **Interact**:
   - Enter your queries in the terminal.
   - Type `exit` to quit.

---

## Project Structure

```plaintext
src/
├── scraper.py       # Scrapes FAQ data
├── embeddings.py    # Generates embeddings
├── database.py      # Handles Pinecone operations
├── chatbot.py       # Chatbot logic
```

---

## Example

```plaintext
$ python main.py
Chatbot started.

You: How do I confirm my booking?
Bot: Please follow the steps in your confirmation email.

You: exit
Chatbot shutting down.
```

