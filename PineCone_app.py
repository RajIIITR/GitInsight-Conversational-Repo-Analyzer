import streamlit as st
import os
import shutil
import stat
import time
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from pinecone import Pinecone
from dotenv import load_dotenv

# Import helper functions
from src.helper import load_embedding, repo_ingestion

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["HUGGINGFACE_API_KEY"] = HUGGINGFACE_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Set page configuration
st.set_page_config(
    page_title="GitHub Repository QA Bot",
    page_icon="💬",
    layout="wide"
)

# Initialize session state to store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "db_initialized" not in st.session_state:
    st.session_state.db_initialized = False

if "index_name" not in st.session_state:
    st.session_state.index_name = "gitinsight"

# Function to initialize the LLM and database
def initialize_qa_system():
    embeddings = load_embedding()
    index_name = st.session_state.index_name
    
    try:
        # Connect to existing Pinecone index
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        
        # Initialize LLM and memory
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        memory = ConversationSummaryMemory(
            llm=llm, 
            memory_key="chat_history", 
            return_messages=True
        )
        
        # Create the conversational chain
        qa = ConversationalRetrievalChain.from_llm(
            llm, 
            retriever=docsearch.as_retriever(search_type="mmr", search_kwargs={"k": 8}),
            memory=memory
        )
        
        st.session_state.db_initialized = True
        return qa
    except Exception as e:
        st.error(f"Error connecting to Pinecone: {str(e)}")
        st.session_state.db_initialized = False
        return None

# Function to process repository ingestion
def process_repo(repo_url):
    if not repo_url:
        st.error("Please enter a GitHub repository URL")
        return
    
    with st.spinner("Processing repository... This may take a moment."):
        try:
            # Step 1: Clone/download the repository
            repo_ingestion(repo_url)
            
            # Step 2: Process and store in Pinecone
            os.system("python store_index.py")
            
            st.success(f"Repository processed: {repo_url}")
            st.session_state.db_initialized = True
            st.session_state.qa_chain = initialize_qa_system()
        except Exception as e:
            st.error(f"Error processing repository: {str(e)}")

# Function to handle permission errors on Windows
def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.unlink, os.rmdir) and excvalue.winerror == 5:  # Access is denied
        try:
            os.chmod(path, stat.S_IWRITE)
            time.sleep(0.1)  # Small delay to let the system release any locks
            func(path)
        except Exception as e:
            st.warning(f"Could not remove {path}: {str(e)}")

# Function to clear repository data with improved Windows handling
def clear_repo():
    try:
        # Clean local files
        if os.path.exists("repo"):
            st.info("Removing repository files...")
            # Try the Windows rd command first
            if os.name == 'nt':  # Windows
                os.system("rd /s /q repo 2>nul")
                # If directory still exists, try rmtree with error handler
                if os.path.exists("repo"):
                    shutil.rmtree("repo", onerror=handle_remove_readonly)
            else:  # Unix-like systems
                shutil.rmtree("repo")
        
        # Delete Pinecone index
        try:
            pc = Pinecone(api_key=PINECONE_API_KEY)
            index_name = st.session_state.index_name
            existing_indexes = [index.name for index in pc.list_indexes()]
            
            if index_name in existing_indexes:
                st.info(f"Deleting Pinecone index: {index_name}...")
                pc.delete_index(index_name)
                st.success(f"Pinecone index '{index_name}' deleted successfully")
        except Exception as e:
            st.error(f"Error deleting Pinecone index: {str(e)}")
        
        st.session_state.db_initialized = False
        st.session_state.messages = []
        st.success("Repository data cleared successfully!")
    except Exception as e:
        st.error(f"Error while clearing data: {str(e)}")
        st.info("Alternative method: Try closing VS Code or other programs that might be accessing these files, then restart the Streamlit app.")

# App UI
st.title("🤖 GitInsight: Conversational Repo Analyzer")
st.markdown("Ask questions about any GitHub repository and get intelligent answers based on its content.")
st.markdown("**Note:** Our project extracts and processes only Python (.py) files for question answering. Other file types such as C, C++, HTML, etc., are not supported.")
st.markdown("**Note:** Once you process a repository, please clear this data via the 'Clear Data' button.")

# Sidebar for repository input
with st.sidebar:
    st.header("Repository Settings")
    repo_url = st.text_input("Enter GitHub Repository URL", placeholder="https://github.com/username/repo")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Process Repository", key="process", use_container_width=True):
            process_repo(repo_url)
    with col2:
        if st.button("Clear Data", key="clear", use_container_width=True):
            clear_repo()
    
    st.divider()
    st.markdown("### How to use")
    st.markdown("""
    1. Enter a GitHub repository URL
    2. Click 'Process Repository'
    3. Ask questions about the repository
    4. Use 'Clear Data' to remove repository data
    """)
    
    st.divider()
    st.markdown("""
    ### Examples
    - "What are the main features of this project?"
    - "Explain the structure of this codebase"
    - "How does the authentication system work?"
    - "Are there any known issues or bugs?"
    - "You can also ask question related to the codebase"
    - "You can ask question regarding the function or any python file role in the given repository"
    """)

# Main area
if not st.session_state.db_initialized:
    st.info("👆 Enter a GitHub repository URL in the sidebar and click 'Process Repository' to begin.")

# Try to initialize QA system if database exists but QA chain not initialized
if st.session_state.db_initialized and not hasattr(st.session_state, 'qa_chain'):
    try:
        st.session_state.qa_chain = initialize_qa_system()
    except Exception as e:
        st.error(f"Error initializing QA system: {str(e)}")
        st.session_state.db_initialized = False

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Ask a question about the repository..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Check if repository has been processed
    if not st.session_state.db_initialized:
        with st.chat_message("assistant"):
            st.markdown("Please process a GitHub repository first by entering a URL in the sidebar.")
        st.session_state.messages.append({"role": "assistant", "content": "Please process a GitHub repository first by entering a URL in the sidebar."})
    else:
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if user_input.lower() == "clear":
                    clear_repo()
                    response = "Repository data cleared!"
                else:
                    try:
                        result = st.session_state.qa_chain(user_input)
                        response = result["answer"]
                    except Exception as e:
                        response = f"Error processing your question: {str(e)}"
                
                st.markdown(response)
        
        # Add assistant message to chat
        st.session_state.messages.append({"role": "assistant", "content": response})