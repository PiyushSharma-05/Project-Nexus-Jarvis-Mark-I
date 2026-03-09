import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import sys
from groq import Groq as genai
import os
import requests
import time
import json
import pygame
import datetime
from dotenv import load_dotenv

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
news_key = os.getenv("NEWS_API_KEY")

MEMORY_FILE = "jarvis_memory.json"

def load_history():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history[-10:], f)

chat_history = load_history()


def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    time.sleep(11)
    
    # Stop the music immediately
    pygame.mixer.music.stop()
    
    # # Optional: Keep the script running until music finishes
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)  

client = genai(api_key=groq_key)

def ask_jarvis(command):
    global chat_history
    try:
        chat_history.append({"role": "user", "content": command})
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis.your operator is piyush a 20 year old boy pursuing btech in IT branch , Your goal is to be helpful but brief. "
                                "CRITICAL RULE: Never exceed 3 sentences per response. "
                                "Use simple, direct language suitable for voice interaction. "
                                "If the user needs more detail, wait for them to ask. "
                                "Always address the user as Sir but only once in starting. make yourself perform like the real JARVIS as that of MCU"
                }
            ] + chat_history,
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
            stream=False
        )

        jarvis_reply = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": jarvis_reply})
        save_history(chat_history)
        return jarvis_reply
        
    except Exception as e:
        print(f"DEBUG: Groq Error - {e}")
        return "Sir, I am having trouble reaching my neural network at the moment."

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 190)
    engine.say(text)
    engine.runAndWait()
 
def get_news():
    # api_key = "news_key"
    url = f"https://newsapi.org/v2/everything?q=India&language=en&sortBy=publishedAt&apiKey={news_key}" 
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            if not articles:
                speak("Sir, I couldn't find any recent news articles for India.")
                return

            speak("Fetching the latest updates...")
            news_to_say = "Here are the recent updates from India. "
            for i, article in enumerate(articles[:3]):
                news_to_say += f"Headline {i+1}: {article['title']}. "
            
            speak(news_to_say)
        else:
            output = ask_jarvis("What is the latest news in India?")
            speak(output)
            
    except Exception as e:
        print(f"DEBUG: Critical Error - {e}")
        speak("I am unable to connect to the news server.")

def processCommand(c):
    print(c)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")   
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")   
    # elif "open linkedin" in c.lower():
    #     webbrowser.open("https://linkedin.com")   
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")   
    elif "open chrome" in c.lower():
        webbrowser.open("https://chrome.com") 
    elif "open linked in" in c.lower():
              webbrowser.open("https://www.linkedin.com/in/piyush-sharma-163aa8328/")

    elif c.lower().startswith("play"):
        try:
            parts = c.lower().split(" ")
            if len(parts) > 1:
                song = parts[1]
                if song in musicLibrary.music:
                    link = musicLibrary.music[song]
                    speak(f"Playing {song}")
                    webbrowser.open(link)
                else:
                    speak("Song not found in library.") 
        except Exception as e:
            speak("I couldn't process the music request.") 

    elif "go to sleep" in c.lower() or "stop listening" in c.lower() or "stop yourself" in c.lower():
                    speak("Stopping Jarvis... Goodbye sir")
                    print("Stopping Jarvis... Goodbye sir!")
                    sys.exit(0)  
    elif "news" in c.lower():
         get_news() 
    elif "the time" in c.lower():
    # Fixed the spelling of strftime
        strTime = datetime.datetime.now().strftime("%H:%M:%S")  
        speak(f"Sir, the time is {strTime}")  
    elif "open vs code" in c.lower():
        codePath = "C:\\Users\\Asus\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"   
        os.startfile(codePath)
    else:
        ai_reply = ask_jarvis(c)
        print(f"Jarvis: {ai_reply}")
        speak(ai_reply)                     
        
if __name__ == "__main__":
   
    speak("Initializing Jarvis....")
    play_sound("Jarvis_StartUp.wav")
    
    while True:
        r = sr.Recognizer()
        r.pause_threshold = 1.5
        try:
            with sr.Microphone() as source:
                print("\n[Status: Sleeping] Listening for wake word 'Jarvis'...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=7, phrase_time_limit=13)
            
            word = r.recognize_google(audio)
            
            if word.lower() == "jarvis":
                print("Jarvis: Yes Sir, I'm here. How can I help?")
                speak("Yes Sir...  I'm here... How can I help?")
                
                conversation_active = True
                while conversation_active:
                    with sr.Microphone() as source:
                        print("[Status: Active] Listening for your command...")
                        try:
                            audio = r.listen(source, timeout=7, phrase_time_limit=5)
                            command = r.recognize_google(audio)
                            print(f"You: {command}")

                            if any(x in command.lower() for x in ["stop", "goodbye", "sleep", "that's all"]):
                                speak("Understood. I'll be here if you need me again.")
                                conversation_active = False
                            elif "shutdown yourself" in command.lower():    
                                speak("Stopping Jarvis... Goodbye sir!")
                                sys.exit(0)
                            else:
                                processCommand(command)
                                
                        except sr.WaitTimeoutError:
                            print("Jarvis: You've been quiet for a while. Going to sleep.")
                            conversation_active = False
                        except sr.UnknownValueError:
                            print("Jarvis: I didn't catch that. Could you repeat?")

        except Exception as e:
            pass
        except KeyboardInterrupt:
            speak("Stopping Jarvis... Goodbye sir!")
            sys.exit(0)