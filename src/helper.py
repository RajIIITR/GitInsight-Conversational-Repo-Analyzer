from src import os, genai, YouTubeTranscriptApi

#Getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        #Since the output of transcript_text might be in the form of list hence we need to write all together in one string
        #Hence we will append it in a string in ordered/sequential way.
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# Configure the API
def configure_genai():
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    genai.configure(api_key=GOOGLE_API_KEY)


#Getting the summary based on Prompt from Google Gemini 1.5 flash
def generate_gemini_content(transcript_text, prompt):
    # Ensure API is configured
    configure_genai()
    
    # Load the generative model
    llm = genai.GenerativeModel('gemini-1.5-flash')
    response = llm.generate_content(prompt + transcript_text)
    return response.text