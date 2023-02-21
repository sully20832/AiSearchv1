import cv2
import requests
import json
from unittest import result
import os, io
import requests
from bs4 import BeautifulSoup
from requests_html import HTML
from requests_html import HTMLSession
from PIL import Image




def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def parse_results(response):
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    for result in results:
        text = ""
        if (result.find(css_identifier_text, first=True)):
            text = result.find(css_identifier_text, first=True).text
        else:
            text = "" 


        # Load the image from file or any other source
        with open("search/frame.jpg", "rb") as f:
            image_bytes = f.read()

        
        
        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            'text': text,
            'thumbnail': io.BytesIO(image_bytes)
        }
        
        output.append(item)
        
    return output

def reverseVideoSearch(videoPath):
    mainResult = []
    titleText = ""

    # Open the video using OpenCV
    cap = cv2.VideoCapture(videoPath)
    
    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(total_frames)
    # Get the frames per second of the video
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print(fps)

    

    # Calculate the number of frames to skip
    skip_frames = int((total_frames / fps) / 1.2)

    print(skip_frames)
    count = 0

    ret, frame = cap.read()
    frameFile = 'search/frame.jpg'
    cv2.imwrite(frameFile, frame)
    
    while True:
        # Read the next frame from the video
        ret, frame = cap.read()
        
        # Break the loop if there are no more frames
        if not ret:
            break

        # Write the current frame to the image file
        cv2.imwrite(frameFile, frame)
        
        # Use the saved frame in the reverse image search
        searchUrl = 'http://www.google.com/searchbyimage/upload'
        multipart = {'encoded_image': (frameFile, open(frameFile, 'rb')), 'image_content': ''}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers['Location']

        source =  get_source(fetchUrl)
        results = parse_results(source)

        if (len(results) >= 2):
            for result in results[2:]:
                if (result not in mainResult):
                    mainResult.append(result)
                    titleText += result['title']




        count += skip_frames # i.e. at 30 fps, this advances one second
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)

    
    # with open('search/theResult.json', 'w') as file:
    #     json.dump(mainResult, file, indent=4)

    print(titleText)
    
    with open('search/titles.txt','w', encoding="utf-8") as file:
        # Write a string to the file
        file.write(titleText)

    

    return mainResult



