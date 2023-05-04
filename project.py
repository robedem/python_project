import speech_recognition as sr
import pyttsx3
import pygame
import openai
import os
import datetime

openai.api_keys = "get the api key from me before running"
# Initialize the speech recognizer
r = sr.Recognizer()

# Initialize the speech synthesizer
engine = pyttsx3.init()

engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Initialize the music player
pygame.init()
pygame.mixer.init()

def get_time():
    now = datetime.datetime.now()
    speak(f"Current time is {now.strftime('%I:%M %p')}")

# Define a function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return None
    except sr.RequestError:
        print("Sorry, there was an error processing your request.")
        return None

def get_weather(city):
    weather_api_keys = "get the api key from me before running"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
    res = requests.get(url)
    data = res.json()
    try:
        temperature = round(data["main"]["temp"] - 273.15, 1)
        weather = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius and the weather is {weather}")
    except:
        speak("Sorry, I couldn't get the weather for that city.")

def get_date():
    now = datetime.datetime.now()
    speak(f"Today's date is {now.strftime('%A, %B %d, %Y')}")

def play_song(song):
    speak(f"Playing {song}")
    pywhatkit.playonyt(song)



def check_diabetes(age, bmi, fasting_blood_sugar):
    if age >= 45 and bmi >= 25 and fasting_blood_sugar >= 126:
        return "You have diabetes"
    else:
        return "You don't have diabetes"

def get_openai_answer(question):
    prompt = f"Answer the following question: {question}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=70,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    return answer

# Define a function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define the wake word
wake_word = "but"

# Define the music directory
music_dir = "C:/Users/roberto/Desktop/music" #make sure to add your own music directory

# Load the music playlist
playlist = []
for file in os.listdir(music_dir):
    if file.endswith(".mp3"):
        playlist.append(os.path.join(music_dir, file))

# Start the virtual assistant
while True:
    # Listen for the wake word
    with sr.Microphone() as source:
        print("Say", wake_word, "to activate the assistant...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        if wake_word in text.lower():
            hour = datetime.datetime.now().hour
            if hour >= 0 and hour < 12:
                speak('Good morning!, I am your virtual assistant . How can I help you?')
            elif hour >= 12 and hour < 18:
                speak('Good afternoon!, I am your virtual assistant . How can I help you?' )
            else:
                speak('Good evening!, I am your virtual assistant . How can I help you?')
                speak('I am your virtual assistant . How can I help you?')
            # Once the wake word is detected, start the speech recognition process
            
                    
        elif "play music" in text.lower():
            speak("Sure, which song would you like to play?")
            # Wait for the user to specify the song
            while True:
                text = recognize_speech()
                if text is not None:
                    found_song = False
                    for song in playlist:
                        if text.lower() in song.lower():
                            pygame.mixer.music.load(song)
                            pygame.mixer.music.play()
                            speak(f"Now playing {os.path.basename(song)}.")
                            found_song = True
                            break
                    if not found_song:
                        speak("Sorry, I couldn't find that song in your playlist.")
                    break
        elif 'time' in text.lower():
            get_time()
        elif "do i have diabaties" in text.lower():
            speak("i can help you check the possibility")
            speak("Please tell me your age")
            age = int(recognize_speech())
            speak("Please tell me your curent Body mass index")
            bmi = float(recognize_speech())
            speak("Please tell me your current blood sugar level")
            fasting_blood_sugar = int(recognize_speech())
            result = check_diabetes(age, bmi, fasting_blood_sugar)
            speak(result)
        elif "weather" in text.lower():
            city = text.split()[-1]
            get_weather(city)


        elif 'date' in text.lower():
            get_date()
        elif 'play {song}' + 'on youtube' in text.lower():
            play_song(song)
        
        elif "stop music" in text.lower():
            pygame.mixer.music.stop()
            speak("Stopping music playback.")
        elif "goodbye" in text.lower():
            speak("Goodbye!")
            break                    
        elif "set alarm" in text.lower():
            speak("Sure, at what time would you like to set the alarm?")
            while True:
                text = recognize_speech()
                if text is not None:
                    if any(char.isdigit() for char in text):
                        hour, minute = None, None
                        for word in text.split():
                            if word.isdigit():
                                if hour is None:
                                    hour = int(word)
                                else:
                                    minute = int(word)
                        if hour is None or minute is None:
                            speak("I'm sorry, I didn't understand the time you specified.")
                        else:
                            speak(f"Setting alarm for {hour} {minute}")
                            # code to set alarm goes here
                            break
                    else:
                        break 
                        speak("I'm sorry, I didn't understand the time you specified.")
                            
        else:
            answer = get_openai_answer(text)
            speak(answer)
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        print("Sorry, there was an error processing your request.")
        break

# Clean up the music player
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()