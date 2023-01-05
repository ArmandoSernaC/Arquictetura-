import speech_recognition as sr
def move(player):        
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Indica la dirección de movimiento ahora...")
        audio = r.listen(source)        
        try:                
            text = r.recognize_google(audio, language='en-US')
            if text == "right":
                player.move_to_right()
            elif text == "shoot":
                player.player_shoot()
            elif text == "left":
                player.move_to_left()

        except:
            print("Prueba de nuevo")
            audio = r.listen(source)