import speech_recognition as sr

def speech_to_text():

    r = sr.Recognizer()

    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    try:
        voice_data = r.recognize_google(audio, language="en-IN")
        print("You said:", voice_data)
        return voice_data

    except sr.UnknownValueError:
        print("Could not understand.")
        return ""

    except sr.RequestError as e:
        print("Speech service error:", e)
        return ""