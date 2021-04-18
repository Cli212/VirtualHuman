import requests
import pyaudio
from deepspeech import Model
import scipy.io.wavfile as wav
import wave
from TTS.utils.io import load_config
import speech_recognition as sr
from TTS.utils.synthesizer import Synthesizer
from playsound import playsound
import string
# Set constants
MODEL_PATH = './voice/models/glow-tts/best_model.pth.tar'
CONFIG_PATH = './voice/models/glow-tts/config.json'
OUT_FILE = 'tts_out.wav'
CONFIG = load_config(CONFIG_PATH)
use_cuda = False


def tts(text):
    synthesizer = Synthesizer(MODEL_PATH, CONFIG_PATH, use_cuda)
    wav = synthesizer.tts(text)
    # save the results
    file_name = text.replace(" ", "_")[0:20]
    file_name = file_name.translate(
        str.maketrans('', '', string.punctuation.replace('_', ''))) + '.wav'
    out_path = OUT_FILE
    print(" > Saving output to {}".format(out_path))
    synthesizer.save_wav(wav, out_path)
    playsound(out_path)


if __name__ == "__main__":
    r = sr.Recognizer()
    bot_message = ''
    while bot_message != "Bye" or bot_message != 'thanks':
        with sr.Microphone() as source:
            print("Speak Anything")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print("You said: ")
                print(text)
            except Exception as e:
                print(e)
        if len(text) == 0:
            continue
        r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={'message':text})
        print("Bot says, ", end=' ')
        for i in r.json():
            bot_message = i['text']
            print(bot_message)
            tts(bot_message)
