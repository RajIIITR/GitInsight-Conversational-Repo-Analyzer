import os
from git import Repo
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
import os

# Use a powerful Hugging Face embedding model.
# For example, you can configure HuggingFaceEmbeddings with "sentence-transformers/all-mpnet-base-v2"
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

from langchain.vectorstores import Chroma

from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain

#clone any github repositories 
def repo_ingestion(repo_url):
    os.makedirs("repo", exist_ok=True)
    repo_path = "repo/"
    Repo.clone_from(repo_url, to_path=repo_path)




#Loading repositories as documents
def load_repo(repo_path):
    loader = GenericLoader.from_filesystem(repo_path,
                                        glob = "**/*",
                                       suffixes=[".py"],
                                       parser = LanguageParser(language=Language.PYTHON, parser_threshold=500)
                                        )
    
    documents = loader.load()

    return documents




#Creating text chunks 
def text_splitter(documents):
    documents_splitter = RecursiveCharacterTextSplitter.from_language(language = Language.PYTHON,
                                                             chunk_size = 2000,
                                                             chunk_overlap = 200)
    
    text_chunks = documents_splitter.split_documents(documents)

    return text_chunks



#loading embeddings model
def load_embedding():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return embeddings