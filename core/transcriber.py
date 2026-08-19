import whisper 
import os
 

WHISPER_MODEL=os.getenv('WHISPER_MODEL',"small")

#currentl we dont have the model
_model=None

def load_model():

    global _model ## we can use it in funcion
    if _model is None:
        print(f"loading model ....")
        _model=whisper.load_model(WHISPER_MODEL)
        print("whisper model loaded succesfully")

    return _model
## our wisper model does two thinks first transcribe the video into text and the next think it can translate the hindi audio to english  we will use tranlate when we want to change the language
def transcribe_chunk(chunk_path:str,translate:bool=False)->str:
    model=load_model()

    ## if translate is false keep the original language else change the language to english
    task="translate" if translate else "transcribe"

    ##the model.trancribe is a fuction 

    result=model.transcribe(chunk_path,task=task)



    return result['text']

def transcribe_all(chunks:list,translate:bool=False)->str:


    full_transcript=""
    for  i,chunk in enumerate(chunks):
        print(f"transcribing chunk{i+1}")
        text=transcribe_chunk(chunk,translate=translate)
        full_transcript += text + " "
    print("transcription commpleted")

    return full_transcript


 



