from sqlalchemy import true
import yt_dlp
import os
from pydub import AudioSegment
DOWNLOAD_DIR="downloads"
os.makedirs(DOWNLOAD_DIR,exist_ok=True)

def downloads_youtube_url(url:str)->str:
    output_path=os.path.join(DOWNLOAD_DIR,"%(title)s.%(ext)s")
    ydl_opts={
        "format":"bestaudio/best",
        "outtmpl": output_path,
        "postprocessors":[
            {
                'key':'FFmpegExtractAudio',
                'preferredcodec':'mp3',
                'preferredquality':'192',
            }
        ],
        "quiet":True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info=ydl.extract_info(url,download=True)
        filename = ( os.path.splitext( ydl.prepare_filename(info) )[0] + ".mp3" )
    return filename


def convert_to_wav(input_path:str)->str:
    """convet the audio/video file to wav format"""
    output_path=os.path.splitext(input_path)[0]+"_converted.wav"
    audio=AudioSegment.from_file(input_path)##it basically helps us to identify the type of file mp4 or mp3 or anything
    audio=audio.set_channels(1).set_frame_rate(16000)#16000khz
    audio.export(output_path,format="wav")
    return output_path

## if giving a huge audio file then it will take time to convert it into wav format so we use chunking method to convert it into wav format
def chunk_audio(wav_path:str,chunk_minutes:int=10)->list:
    """chunk the audio file into smaller chunks.the chunking process basically works on milliseconds the chunkminutes will be multipy by 60 and multiply bt 1000"""
    audio=AudioSegment.from_wav(wav_path)
    chunk_ms=chunk_minutes*60*1000
    chunks=[]
    for i,start in enumerate(range(0,len(audio),chunk_ms)):
        chunk=audio[start:start+chunk_ms]
        chunk_path=f"{wav_path}_chunk{i}.wav"
        chunk.export(chunk_path,format='wav')
        chunks.append(chunk_path)
    return chunks
def process_input(source:str)->list:
    if source.startswith("http://") or source.startswith("https://"):
        audio_path=downloads_youtube_url(source)
        wave_path=convert_to_wav(audio_path)
    else:
        print("local file has detected converting to wav format")
        wave_path=convert_to_wav(source)
    print("chunking audio")
    chunks=chunk_audio(wave_path)
    print(f"total len of video {len(chunks)}")
    return chunks




