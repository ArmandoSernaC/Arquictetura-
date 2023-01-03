import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Puedes hablar ahora...")
    audio = r.listen(source)
    
    try:                
        text = r.recognize_google(audio, language='en-US')
        if text == "right":
            self.move_to_right()
        elif text == "shoot":
            self.player_shoot()
        elif text == "left":
            self.move_to_left()

    except:
        print("Prueba de nuevo")
        audio = r.listen(source)