# GitInsight: Conversational Repository Analyzer
GitInsight is an AI-powered tool to analyze Python files in Git repositories and provide conversational code insights.

## 🔍 Overview
GitInsight is designed to empower developers by enabling natural language queries about Python code within public Git repositories. The tool performs the following steps:
- **Clones a given public repository.**
- **Extracts only `.py` files.**
- **Chunks and stores the code in a vector database (Pinecone) for efficient retrieval.**
- **Leverages a large language model (Gemini 2.0 Flash) to answer any questions about the Python codebase.**

## 🚀 Features
- 📊 **Repository Analysis**: Clone public Git repos and focus on Python files.
- 💬 **Conversational Insights**: Ask any questions regarding the code; get contextual, accurate responses.
- 🔄 **Vector Storage**: Uses Pinecone to store code embeddings for quick similarity search.
- 🧠 **LLM Integration**: Powered by advanced LLM (Gemini 2.0 Flash) for code understanding.
- 🖥️ **User-Friendly Interface**: Built with Streamlit for an interactive and seamless user experience.

## 🛠️ Technologies Used
- **Python** 🐍
- **Streamlit** (for deployment and user interface)
- **Google Generative AI** (Using Gemini-2.0-Flash model)
- **Pinecone** (vector database for embeddings storage)
- **GitPython** (for repository cloning and management)
- **Langchain** (for text chunking and processing)
- **python-dotenv** (for environment variable management)

## 🔄 Workflow
1. **Repository Input**: User provides a public GitHub repository URL.
2. **Code Extraction**: GitPython clones the repo and extracts Python files.
3. **Processing Pipeline**: 
   - Text extraction from Python files
   - Code chunking with appropriate context
   - Embedding generation and storage in Pinecone
4. **User Queries**: Users can ask questions about the code in natural language.
5. **AI-Generated Responses**: Gemini model analyzes relevant code chunks and provides detailed answers.

## 📌 How to Run Locally
### Installation Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/RajIIITR/GitInsight-Conversational-Repo-Analyzer.git
   cd GitInsight-Conversational-Repo-Analyzer
   ```
2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up API Keys**
   - Create a `.env` file in the project root.
   - Add your API keys:
     ```env
     GOOGLE_API_KEY=your_gemini_api_key_here
     PINECONE_API_KEY=your_pinecone_api_key_here
     PINECONE_ENVIRONMENT=your_pinecone_environment
     ```
5. **Run the Application**
   ```bash
   streamlit run app.py
   ```
6. **Access the Web App**
   - Open `http://localhost:8501` in your browser.

## 📋 Requirements
- Python>=3.8
- streamlit
- google-generativeai
- pinecone-client
- gitpython
- langchain
- python-dotenv

## 📄 Project Structure
```
GitInsight/
├── app.py                 # Main Streamlit application
├── src/
│   └── helper.py          # Helper functions for embeddings and repo processing
├── store_index.py         # Script to process and store code in Pinecone
├── requirements.txt       # Dependencies
└── .env                   # Environment variables (not tracked)
```

---
⭐ **Star this repository** if you find it useful!
