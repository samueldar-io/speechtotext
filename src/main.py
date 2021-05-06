import speech_recognition as sr 
import os
import pydub
from pydub import AudioSegment
from pydub.silence import split_on_silence
import PySimpleGUI as sg
import os.path

path = os.getcwd()
pydub.AudioSegment.converter = r"C:\\ffmpeg\\ffmpeg.exe"

re = sr.Recognizer()

def match_target_amplitude(aChunk, target_dBFS):
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

folder = path + "\static"
filename = "audio.wav"
filepath = folder + '\\' + filename

audio = AudioSegment.from_wav(filepath)

thresh = int(audio.dBFS + (-14))

chunks = split_on_silence (audio, min_silence_len = 1000, silence_thresh = thresh)

for i, chunk in enumerate(chunks):

    silence_chunk = AudioSegment.silent(duration=500)
    audio_chunk = silence_chunk + chunk + silence_chunk
    normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
    
    normalized_chunk.export(".\static\chunk{0}.wav".format(i), bitrate = "192k", format = "wav")
    chunkname = "chunk{0}.wav".format(i)
    chunkpath = folder + '\\' + chunkname

    with sr.AudioFile(chunkpath) as source:
        try:
            info_audio = re.record(source)
            texto = re.recognize_google(info_audio, language = "es-ES")
        
            with open(".\static\\texto.txt", "a+") as file:
                file.write(texto)
                file.write("\n")
        except:
            pass
    os.remove(chunkpath)

print("ya hizo el beta")