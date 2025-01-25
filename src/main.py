import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from src.scraper import scrape_faq_data
from src.embeddings import load_model, generate_embeddings
from src.database import upsert_data
from src.chatbot import chatbot_response

def main():
    load_dotenv()

    api_key = os.getenv("PINECONE_API_KEY")
    environment = os.getenv("PINECONE_ENVIRONMENT")
    index_name = os.getenv("INDEX_NAME")

    if not api_key or not environment or not index_name:
        print("Please ensure all necessary information is filled in the .env file.")
        return

    # Step 1: Scrape FAQ Data
    url = "https://www.booking.com/tpi_faq.de.html"
    try:
        faq_data = scrape_faq_data(url)
        print("FAQ data successfully scraped.")
    except Exception as e:
        print(f"Error occurred while scraping data: {e}")
        return

    # Step 2: Load Embedding Model
    print("Loading embedding model...")
    model = load_model()

    # Step 3: Generate Embeddings
    faq_data = generate_embeddings(faq_data, model)

    # Step 4: Initialize Pinecone and Upload Data
    print("Initializing Pinecone...")
    pc = Pinecone(api_key=api_key)

    # Check if the index exists
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,  # Adjust dimension based on the model
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",  # Update based on Pinecone environment
                region=environment
            )
        )

    # Retrieve the index
    index = pc.Index(index_name)

    # Upload data to Pinecone
    upsert_data(faq_data, index)
    print("Data successfully uploaded to Pinecone.")

    # Step 5: Start Chatbot
    print("Chatbot started. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Shutting down the chatbot. Goodbye!")
            break
        response = chatbot_response(user_input, model, index)
        print(f"Bot: {response}")


if __name__ == "__main__":
    main()
