#!/usr/bin/python3
import requests
import time
import openai
import random
import json
from pydub import AudioSegment
from moviepy.editor import *

# Set your OpenAI API key
openai.api_key = 'example' #Change to your openai api key
# List of 30 League of Legends champions
champions = [
    'Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios',
    'Ashe', 'Aurelion Sol', 'Azir', 'Bard', 'Blitzcrank', 'Brand', 'Braum',
    'Caitlyn', 'Camille', 'Cassiopeia', 'ChoGath', 'Corki', 'Darius', 'Diana',
    'Draven', 'Dr Mundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks',
    'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves',
    'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'Jarvan IV',
    'Jax', 'Jayce', 'Jhin', 'Jinx', 'KaiSa', 'Kalista', 'Karma', 'Karthus', 'Kassadin',
    'Katarina', 'Kayle', 'Kayn', 'Kennen', 'KhaZix', 'Kindred', 'Kled', 'KogMaw',
    'LeBlanc', 'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux',
    'Malphite', 'Malzahar', 'Maokai', 'Master Yi', 'Miss Fortune', 'Mordekaiser',
    'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nocturne', 'Nunu and Willump',
    'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn',
    'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renekton', 'Rengar', 'Riven', 'Rumble',
    'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen',
    'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain',
    'Sylas', 'Syndra', 'Tahm Kench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh',
    'Tristana', 'Trundle', 'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 'Urgot',
    'Varus', 'Vayne', 'Veigar', 'VelKoz', 'Viktor', 'Vladimir', 'Volibear', 'Warwick',
    'Wukong', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi',
    'Zac', 'Zed', 'Ziggs', 'Zilean', 'Zoe', 'Zyra'
]

# Pick a random champion
random_champion = random.choice(champions)

chosen_prompt = "Give a summary of what items and runes to build on " + random_champion + " that is around 70 seconds when spoken"

# Use the OpenAI API to generate the script
response = openai.Completion.create(
  engine="text-davinci-003",
  prompt=chosen_prompt,
  temperature=0.8,
  max_tokens=750
)

# Print the generated script
print(response.choices[0].text.strip())
script = (response.choices[0].text.strip())


url = "https://api.d-id.com/talks"


payload = {
    "script": {
        "type": "text",
        "provider": {
            "type": "microsoft",
            "voice_id": "en-US-JennyNeural"
        },
        "input": script
    },
    "source_url": "https://e0.pxfuel.com/wallpapers/595/614/desktop-wallpaper-irelia-fantasy-face-lol-foritis-wong-girl.jpg"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "example" #change to your D-ID API key
}
# Old API-key: YWRhbWNoZW4xNTFAZ21haWwuY29t:Di-noSF-d8ylB3Z-UbbPf

response = requests.post(url, json=payload, headers=headers)

print(response.text)

print("\n\n\n")


#So that the json contains result_url instead of pending_url
time.sleep(20) 

url = "https://api.d-id.com/talks?limit=1"
headers = {
    "accept": "application/json",
    "authorization": "example" #change to your D-ID API key
}
response = requests.get(url, headers=headers)
print(response.text)

# Parse JSON string into a Python dictionary
data = json.loads(response.text)

# Extract value from the "result_url" key
result_url = data['talks'][0]['result_url'] #data['talks'][0]['user']['result_url']

print(result_url)


# Load audio file (Change to an audio file that you want)
audio = AudioSegment.from_file("Sneaky-Snitch.mp3")

#Lower the volume
audio = audio - 7

# Save the result
audio.export("music.mp3", format="mp3")



# Load video (with sound)
video = VideoFileClip(result_url)

# Load additional audio
additional_audio = AudioFileClip("music.mp3")

# Make sure additional audio is not longer than the video
if additional_audio.duration > video.duration:
    additional_audio = additional_audio.subclip(0, video.duration)

# Combine audio: original audio and additional audio
audio = CompositeAudioClip([video.audio, additional_audio])

# Set the audio to the video
video = video.set_audio(audio)

# Write the result to a file (with audio codec)
video.write_videofile(f"{random_champion}.mp4", codec='libx264', audio_codec='aac')
