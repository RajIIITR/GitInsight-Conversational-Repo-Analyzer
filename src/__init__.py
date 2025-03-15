import os
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()