import speech_recognition as sr
import pyttsx3
import webbrowser
import openai
import wikipedia
import sys

openai.api_key = 'sk-LdQXxyE0pPK8cOoL0P1XT3BlbkFJ8jd8h2qRCE4VPWEg8wu'

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user's voice command
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("User: " + text)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return ""
    except sr.RequestError as e:
        print(f"Request error: {e}")
        return ""

# Function to search Google
def search_google(query):
    search_query = 'https://www.google.com/search?q=' + query.replace(' ', '+')
    webbrowser.open_new_tab(search_query)

# Function to search and retrieve information from Wikipedia
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        print("Wikipedia: " + result.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        print("Wikipedia: There are multiple results. Please provide a more specific query.")
        speak("There are multiple results. Please provide a more specific query.")
    except wikipedia.exceptions.PageError as e:
        print("Wikipedia: Sorry, I couldn't find any information on that topic.")
        speak("Sorry, I couldn't find any information on that topic.")

# Function to generate response using ChatGPT
def generate_response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Function to process user's voice command and provide a response
def process_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you?")
    elif "goodbye" in command:
        speak("Goodbye!")
        exit()
    elif "chat" in command:
        prompt = command.replace("chat", "").strip()
        response = generate_response(prompt)
        speak(response)
    elif "google" in command:
        query = command.replace("google", "").strip()
        search_google(query)
    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        search_wikipedia(query)
    else:
        speak("I'm sorry, I can't help with that.")
        # Function to convert text to speech and print the text
def speak(text):
    print("Assistant: " + text)
    engine.say(text)
    engine.runAndWait()
# Main loop
speak("Welcome! How can I assist you?")
while True:
    command = listen()
    process_command(command)
