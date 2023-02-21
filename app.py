
import streamlit as st
from pytube import YouTube
import random, json, re
from textToSpeech import video2speech
from search import testRV
import requests
from PIL import Image





st.markdown('<h1>AI Video Search Engine (Beta) 👁️<h1>', unsafe_allow_html=True)
st.markdown('<h4>Check out my <a href="https://www.youtube.com/channel/UCPUeiYgLjhnJ7yzWydZKOBg"> Youtube </a> and <a href="https://twitter.com/SullyBillions" > Twitter</a>. Hope you enjoy :)<h4>', unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["Input", "Transcription", "Results"])

theTranscriptResult = ""
theResults = {}




def shortsSearch(text):
    yt = YouTube(text)
   
    #Download Scraped Video
    video = yt.streams.get_highest_resolution()
    video.download(filename="video.mp4")
    print("Yayyy!! Download Completed!!!")




# input tab
with tab1:

    st.header("Input your video")

    # Create sidebar with mini navigation bar
    # Using "with" notation

    
    nav_option = st.radio(
        "Choose Input method:",
        ("Youtube Shorts", "Video File")
    )

    #Youtube Shorts
    if nav_option == "Youtube Shorts":

        # Create a text input for the user to enter the link
        youtube_link = st.text_input("Enter YouTube Shorts link")

        # If the user has entered a link, display it and convert the video to a transcript
        if youtube_link:
            st.write("You entered:", youtube_link)

            shortsSearch(youtube_link)
            theTranscriptResult = video2speech.convert('video.mp4')

            with st.spinner('Processing Results...'):
                theResults = testRV.reverseVideoSearch('video.mp4')




            st.write("Check Results!")
            
    else:
        # Create a file uploader for the user to upload a video file
        video_file = st.file_uploader("Upload a video file", type=["mp4"], accept_multiple_files=False)

        # If the user has uploaded a file, display its name and convert the video to a transcript
        if video_file is not None:
            st.write("You uploaded:", video_file.name)

            # Write the file to disk
            with open("video.mp4", "wb") as f:
                f.write(video_file.read())
            

            theTranscriptResult = video2speech.convert('video.mp4')

            with st.spinner('Processing Results...'):
                theResults = testRV.reverseVideoSearch('video.mp4')
        
                
            st.write("Check Results!")
            


    start_button = st.button("Start Search")

with tab2:
    st.header("Transcription")

    #Check if there is a transcript
    if len(theTranscriptResult) < 5:
        st.markdown("No Transcription yet ...")

    else:
        st.text_area("", value=theTranscriptResult, height=150, disabled=True)


with tab3:
    st.header("Results")

    # Check if there are any results to show
    if len(theResults) == 0:
        st.markdown("No results ...")
    else:
        
        for result in theResults:


            # Create a container for each result
            container = st.container()

            # Create two columns within the container
            col1, col2 = container.columns([1, 3])
            
            # Get the thumbnail image
            
            thumbnail = Image.open(result['thumbnail'])
            
            # Display the thumbnail in the first column
            col1.image(thumbnail, use_column_width=True, clamp=True)
    
            

            # Show the title as a clickable link
            col2.markdown(f"<a href='{result['link']}' target='_blank'>{result['title']}</a>", unsafe_allow_html=True)

            # Remove first pixel information from the text
            text = re.sub(r'\d+\s*[×x]\s*\d+\s*\s*', '', result['text'])

            col2.write(text + "\n")
            col2.write("\n")






