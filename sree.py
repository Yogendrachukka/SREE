import os
import time
import datetime
import webbrowser
import pyautogui
import pyttsx3
import speech_recognition as sr
import pywhatkit

# ---------------- PASSWORD ----------------
try:
    from pass_key import key
    PASSWORD = key
except Exception:
    PASSWORD = "chukkayogendra@2007"  # fallback

# ---------------- AI (OPTIONAL) ----------------
# If you want ChatGPT mode:
# pip install openai
USE_AI = False  # make True if you want AI mode
OPENAI_API_KEY = ""  # paste your API key here

# ---------------- VOICE ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty("rate", 175)


def speak(text: str):
    print("SREE:", text)
    engine.say(text)
    engine.runAndWait()


def listen(timeout=6, phrase_time_limit=6):
    """Listen and return text OR None"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print("User:", query)
        return query
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        speak("Network issue with speech recognition.")
        return None


def wish():
    hour = datetime.datetime.now().hour
    t = datetime.datetime.now().strftime("%I:%M %p")

    if 0 <= hour < 12:
        speak("Good morning sir. I am SREE your virtual assistant.")
    elif 12 <= hour < 16:
        speak("Good afternoon sir. I am SREE your virtual assistant.")
    elif 16 <= hour < 19:
        speak("Good evening sir. I am SREE your virtual assistant.")
    else:
        speak("Hello sir. I am SREE your virtual assistant.")

    speak(f"Sir, current time is {t}")


# ---------------- SYSTEM FUNCTIONS ----------------
def take_screenshot():
    folder = "SREE_Screenshots"
    os.makedirs(folder, exist_ok=True)
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    path = os.path.join(folder, filename)
    pyautogui.screenshot(path)
    speak("Screenshot taken sir")
    print("Saved at:", path)


def volume_up():
    for _ in range(5):
        pyautogui.press("volumeup")
    speak("Volume increased sir")


def volume_down():
    for _ in range(5):
        pyautogui.press("volumedown")
    speak("Volume decreased sir")


def mute_volume():
    pyautogui.press("volumemute")
    speak("Volume muted sir")


def shutdown_pc():
    speak("Sir, are you sure you want to shutdown? Say yes to confirm.")
    ans = listen(timeout=6, phrase_time_limit=4)
    if ans and "yes" in ans.lower():
        speak("Shutting down sir")
        os.system("shutdown /s /t 3")
    else:
        speak("Shutdown cancelled sir")


def restart_pc():
    speak("Sir, are you sure you want to restart? Say yes to confirm.")
    ans = listen(timeout=6, phrase_time_limit=4)
    if ans and "yes" in ans.lower():
        speak("Restarting sir")
        os.system("shutdown /r /t 3")
    else:
        speak("Restart cancelled sir")


def lock_pc():
    speak("Locking screen sir")
    os.system("rundll32.exe user32.dll,LockWorkStation")


# ---------------- OPEN APPS ----------------
def open_app(query):
    q = query.lower()

    if "chrome" in q:
        speak("Opening Chrome sir")
        os.startfile("chrome.exe")

    elif "notepad" in q:
        speak("Opening Notepad sir")
        os.startfile("notepad.exe")

    elif "calculator" in q:
        speak("Opening Calculator sir")
        os.startfile("calc.exe")

    elif "command prompt" in q or "cmd" in q:
        speak("Opening command prompt sir")
        os.system("start cmd")

    elif "vs code" in q or "visual studio code" in q:
        speak("Opening VS Code sir")
        os.system("code")

    else:
        speak("Sir app not found. Tell me exact app name.")


# ---------------- WEB FUNCTIONS ----------------
def open_youtube():
    speak("Opening youtube sir")
    webbrowser.open("https://www.youtube.com")


def open_google():
    speak("Opening google sir")
    webbrowser.open("https://www.google.com")


def open_website(query):
    site = query.lower().replace("open", "").replace("website", "").strip()
    site = site.replace(" ", "")

    if not site:
        speak("Please tell the website name sir.")
        return

    url = f"https://www.{site}.com"
    speak(f"Opening {site} sir")
    webbrowser.open(url)


def google_search(query):
    search_text = query.lower().replace("search", "").replace("google", "").strip()
    if not search_text:
        speak("What should I search sir?")
        search_text = listen(timeout=6, phrase_time_limit=5)
    if search_text:
        speak(f"Searching {search_text} on google")
        pywhatkit.search(search_text)
    else:
        speak("Search cancelled sir")


def youtube_search(query):
    search_text = query.lower().replace("search", "").replace("youtube", "").strip()
    if not search_text:
        speak("What should I search on youtube sir?")
        search_text = listen(timeout=6, phrase_time_limit=5)

    if search_text:
        speak(f"Searching {search_text} on youtube")
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_text}")
    else:
        speak("Search cancelled sir")


def play_song(query):
    song = query.lower().replace("play", "").replace("song", "").replace("music", "").strip()
    if not song:
        speak("Which song should I play sir?")
        song = listen(timeout=6, phrase_time_limit=5)
    if song:
        speak(f"Playing {song} on youtube")
        pywhatkit.playonyt(song)
    else:
        speak("Cancelled sir")


# ---------------- NOTEPAD TYPE MODE ----------------
def typing_mode():
    speak("Opening Notepad sir")
    os.startfile("notepad.exe")
    time.sleep(1)

    speak("Start speaking sir. I will type. Say stop writing to exit.")
    while True:
        text = listen(timeout=10, phrase_time_limit=10)
        if not text:
            continue

        text_low = text.lower()
        if "stop writing" in text_low or "exit writing" in text_low or "stop" in text_low:
            speak("Ok sir, typing stopped.")
            break

        pyautogui.write(text)
        pyautogui.press("enter")


# ---------------- WHATSAPP ----------------
def send_whatsapp_message():
    speak("Tell phone number with country code. Example +91xxxxxxxxxx")
    num = input("Enter WhatsApp number (example +919999999999): ").strip()

    speak("Tell your message sir")
    msg = listen(timeout=8, phrase_time_limit=6)
    if not msg:
        speak("Message not received. Cancelled.")
        return

    speak("Tell minutes from now to send message. Example 1, 2, 3")
    mins = input("Enter minutes from now to send (1/2/3): ").strip()
    if not mins.isdigit():
        mins = "1"
    mins = int(mins)

    now = datetime.datetime.now() + datetime.timedelta(minutes=mins)
    hour = now.hour
    minute = now.minute

    speak("Sending whatsapp message sir. Please keep WhatsApp Web logged in.")
    pywhatkit.sendwhatmsg(num, msg, hour, minute)
    speak("Message scheduled sir")


# ---------------- AI MODE (OPTIONAL) ----------------
def ai_reply(user_text):
    """
    If you want ChatGPT responses:
    - pip install openai
    - add API key
    - set USE_AI = True
    """
    if not USE_AI:
        return "AI mode is disabled sir."

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are SREE, a helpful virtual assistant."},
                {"role": "user", "content": user_text},
            ],
            temperature=0.7,
        )
        return res.choices[0].message.content.strip()

    except Exception as e:
        return f"AI error sir: {e}"


# ---------------- WAKE WORD MODE ----------------
def wait_for_wake_word():
    speak("Sir, I am in sleep mode. Say 'hey sree' to wake me up.")
    while True:
        q = listen(timeout=8, phrase_time_limit=4)
        if q and "hey sree" in q.lower():
            speak("Yes sir, I am ready.")
            return


# ---------------- MAIN LOOP ----------------
def main():
    speak("This file is password protected sir. Please enter the password.")
    pass_in = input("Enter the password sir:\n").strip()

    if pass_in != PASSWORD:
        speak("Wrong password sir. Access denied.")
        return

    speak("Access granted sir.")
    wish()

    active_mode = True

    while True:
        if not active_mode:
            wait_for_wake_word()
            active_mode = True

        speak("Tell your command sir.")
        query = listen(timeout=10, phrase_time_limit=6)

        if not query:
            continue

        query = query.lower()

        # -------- BASIC --------
        if "time" in query:
            t = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir current time is {t}")

        elif "date" in query:
            d = datetime.datetime.now().strftime("%d %B %Y")
            speak(f"Sir today's date is {d}")

        # -------- WAKE/SLEEP --------
        elif "sleep mode" in query or "go to sleep" in query:
            speak("Ok sir. Going to sleep mode.")
            active_mode = False

        # -------- APPS --------
        elif "open" in query and ("chrome" in query or "notepad" in query or "calculator" in query or "cmd" in query or "vs code" in query):
            open_app(query)

        # -------- WEB --------
        elif "youtube" in query and "search" not in query:
            open_youtube()

        elif "google" in query and "search" not in query:
            open_google()

        elif "website" in query:
            open_website(query)

        elif "search google" in query or ("google" in query and "search" in query):
            google_search(query)

        elif "search youtube" in query or ("youtube" in query and "search" in query):
            youtube_search(query)

        elif "play" in query and ("song" in query or "music" in query):
            play_song(query)

        # -------- TYPE MODE --------
        elif "type" in query or "write" in query:
            typing_mode()

        # -------- WHATSAPP --------
        elif "whatsapp" in query and ("message" in query or "send" in query):
            send_whatsapp_message()

        # -------- SCREENSHOT --------
        elif "screenshot" in query:
            take_screenshot()

        # -------- VOLUME --------
        elif "volume up" in query:
            volume_up()

        elif "volume down" in query:
            volume_down()

        elif "mute" in query:
            mute_volume()

        # -------- PC CONTROL --------
        elif "shutdown" in query:
            shutdown_pc()

        elif "restart" in query:
            restart_pc()

        elif "lock" in query:
            lock_pc()

        # -------- AI CHAT --------
        elif "ai mode" in query or "chat mode" in query:
            speak("AI chat mode started sir. Say exit ai mode to stop.")
            while True:
                speak("Ask me anything sir.")
                q = listen(timeout=10, phrase_time_limit=8)
                if not q:
                    continue
                if "exit ai mode" in q.lower() or "stop ai" in q.lower():
                    speak("AI mode stopped sir.")
                    break

                reply = ai_reply(q)
                speak(reply)

        # -------- EXIT --------
        elif "exit" in query or "quit" in query or "stop assistant" in query:
            speak("Goodbye sir. Have a nice day.")
            break

        else:
            speak("Sir I did not understand. Please try again.")


if __name__ == "__main__":
    main()
