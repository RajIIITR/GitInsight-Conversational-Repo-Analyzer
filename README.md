# GitInsight: Conversational Repository Analyzer

**AI-powered tool to analyze Python files in Git repositories and provide conversational code insights.**

![GitInsight Banner](https://via.placeholder.com/1200x300?text=GitInsight)  
*(Replace the URL with your project banner image)*

---

## Overview

GitInsight is designed to empower developers by enabling natural language queries about Python code within public Git repositories. The tool performs the following steps:
- **Clones a given public repository.**
- **Extracts only `.py` files.**
- **Chunks and stores the code in a vector database (Pinecone) for efficient retrieval.**
- **Leverages a large language model (Gemini 2.0 Flash) to answer any questions about the Python codebase.**

---

## Features

- **Repository Analysis:** Clone public Git repos and focus on Python files.
- **Conversational Insights:** Ask any questions regarding the code; get contextual, accurate responses.
- **Vector Storage:** Uses Pinecone to store code embeddings for quick similarity search.
- **LLM Integration:** Powered by advanced LLM (Gemini 2.0 Flash) for code understanding.
- **User-Friendly Interface:** Built with Streamlit for an interactive and seamless user experience.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/GitInsight.git
   cd GitInsight

