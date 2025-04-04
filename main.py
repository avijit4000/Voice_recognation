from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import speech_recognition as sr
import pyttsx3
import uvicorn

app = FastAPI()

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Speech-to-Text Function
def transform_audio_into_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        print("You can now speak...")
        audio = r.listen(source)
        try:
            request = r.recognize_google(audio, language="en-gb")
            print("You said: " + request)
            return request
        except sr.UnknownValueError:
            return "I couldn't understand, please try again."
        except sr.RequestError:
            return "There seems to be an issue with the service."
        except Exception as e:
            print(f"Error: {e}")
            return "Something went wrong."

# Text-to-Speech Function
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recognize-audio")
async def recognize_audio():
    text = transform_audio_into_text()
    return {"recognized_text": text}

@app.post("/speak-text")
async def speak_recognized_text(request: Request):
    data = await request.json()
    text = data.get("text", "No text provided")
    speak_text(text)
    return {"message": "Text spoken aloud"}
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)