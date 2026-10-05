import pyttsx3


def text_to_speech(text):

    engine = pyttsx3.init("sapi5")

    
    engine.setProperty("rate", 120)

    
    engine.setProperty("volume", 1.0)

    
    voices = engine.getProperty("voices")

    
    for i, voice in enumerate(voices):
        print(i, voice.name)

    if voices:
        engine.setProperty("voice", voices[0].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()