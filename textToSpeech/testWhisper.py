import requests

def transcribe_audio(audio_url):
    
    with open(audio_url, 'rb') as file:
        audio_data = file.read()

    headers = {
            'Content-Type': 'audio/wav',
        }

    response = requests.post(
        'https://api.deepgram.com/v1/listen?model=whisper',
        headers=headers,
        data=audio_data
    )
    

    transcription = response.json()['results']['channels'][0]['alternatives'][0]['transcript']
    
    return transcription


