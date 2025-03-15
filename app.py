from src import st
from src.helper import extract_transcript_details, generate_gemini_content
from src.prompt import prompt



st.title("Youtube Video Summarizer")
youtube_link = st.text_input("Enter Youtube Video Link: ")

if youtube_link:
    video_id = youtube_link.split("v=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width = True)

if st.button("Get Detailed Summary"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("** Detailed Summary: **")
        st.write(summary)