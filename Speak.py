import pyttsx3
import speech_recognition as sr
# import pyaudio 
# import wikipedia
# import webbrowser
# import os
# import datetime
import subprocess as sp
import pyautogui
import HandTrackingModule as ht
import cv2

def spk():
    def getNumber(fingers):
        s = ""
        for i in fingers:
            s += str(i)

        if(s == "00000"):
            return 0
        elif(s == "01000"):
            return pyautogui.press('F12')
        elif(s == "01100"):
            return "V"
        elif(s == "01110"):
            return 3
        elif(s == "01111"):
            return 4
        elif(s == "11111"):
            return 5
        elif(s == "10000"):
            return 6
        elif(s == "11000"):
            return 7
        elif(s == "11100"):
            return 8
        elif(s == "10111"):
            return 9
        elif(s == "10001"):
            return 10
        elif(s == "11001"):
            return 20
        elif(s == "01001"):
            return 30

    engine = pyttsx3.init('sapi5')

    voices = engine.getProperty('voices')

    print(voices[0].id)
    engine.setProperty('voice' , voices[0].id)

    def takeCommand():
        # It takes microphone input and returns string output

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening.....")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing.....")
            query = r.recognize_google(audio , language = 'en-in')
            print(f"User said : {query} \n")

        except Exception as e:
            print(e)
            print("Say that again please....")
            return "None"

        return query

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    if __name__ == "__main__":
        if 1:
            query = takeCommand().lower()
            # Logic for executing tasks based on query

            programName = "Winword.exe"
            fileName = "demofile2.txt"
            str = query.replace("full stop" , ".")
            str = query.replace("fullstop" , ".")
            f = open( fileName , "w")
            f.write(str)
            f.close()

            sp.Popen([programName, fileName])

            # if 'wikipedia' in query :
            #     speak("Searching Wikipedia.....")
            #     query = query.replace("wikipedia" , "")
            #     results = wikipedia.summary(query , sentences = 2)
            #     speak("According to Wikipedia ")
            #     print(results)
            #     speak(results)

            # elif 'open youtube' in query:
            #     webbrowser.open("youtube.come")

            # elif 'open google' in query:
            #     webbrowser.open("google.com")

            # elif 'open stackoverflow' in query:
            #     webbrowser.open("stackoverflow.com")

            # elif 'play music' in query:
            #     music_dir = 'C:\\Users\\HP\\Desktop\\Songs'
            #     songs = os.listdir(music_dir)
            #     print(songs)
            #     os.startfile(os.path.join(music_dir , songs[0]))

            # elif 'the time' in query:
            #     strTime = datetime.datetime.now().strftime("%H : %M : %S")
            #     speak(f"Sir , the time is {strTime}")


        cap = cv2.VideoCapture(0 , cv2.CAP_DSHOW)
        cap.set(3 , 700)
        cap.set(4 , 600)

        detector  = ht.HandDetector()
        while(True):
            _ , img = cap.read()

            img = cv2.flip(img , 1)
            # Bilateral shift

            img = detector.findHands(img)

            idList = detector.findPosition(img , False)
            tipId = [4 , 8 , 12 , 16 , 20]

            if(len(idList)!=0):
                fingers = []
                if(idList[tipId[0]][1] < idList[tipId[0]-2][1]):
                    fingers.append(1)
                else:
                    fingers.append(0)

                for id in range(1 , len(tipId)):
                    if(idList[tipId[id]][2] < idList[tipId[id]-2][2]):
                        fingers.append(1)
                    else:
                        fingers.append(0) 

                cv2.putText(img , str(getNumber(fingers)) , (45 , 375) , cv2.FONT_HERSHEY_PLAIN , 10 , (255 , 0 , 255) , 20)

            if cv2.waitKey(25) & 0xFF == ord("q"):
               break

            cv2.imshow("Result" , img)
            cv2.waitKey(1)