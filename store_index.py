from src.helper import repo_ingestion, load_repo, text_splitter, load_embedding
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["HUGGINGFACE_API_KEY"] = HUGGINGFACE_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Load and process repository data
documents = load_repo("repo/")
text_chunks = text_splitter(documents)
embeddings = load_embedding()

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define index name for the GitInsight project
index_name = "gitinsight"

# Check if index exists, if not create it
existing_indexes = [index.name for index in pc.list_indexes()]
if index_name not in existing_indexes:
    # Create Pinecone index
    pc.create_index(
        name=index_name,
        dimension=768,  # Adjust dimension based on your embedding model
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print(f"Created new Pinecone index: {index_name}")
else:
    print(f"Using existing Pinecone index: {index_name}")

# Store document embeddings in Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)

print(f"Successfully stored {len(text_chunks)} document chunks in Pinecone index: {index_name}")