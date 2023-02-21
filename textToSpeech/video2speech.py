
import moviepy
import moviepy.editor

from textToSpeech import testWhisper

def convert(path):
    video = moviepy.editor.VideoFileClip(path)    # Put your file path in here
    
    # Convert video to audio
    audio = video.audio
    audio.write_audiofile("newaud.wav")
    transcript = testWhisper.transcribe_audio("newaud.wav")

    with open('transcript.txt', 'w') as f:

        try:
            f.write(transcript)
        except:
            f.write("Error")

    return transcript



