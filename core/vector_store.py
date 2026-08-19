import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR="vector_db"
COLLECTION_NAME="meeting_transcript"##were we want to store data

EMBEDDING_MODEL="all-MiniLM-L6-V2"

def get_embbeding():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL,model_kwargs={"device":'cpu'})



def build_vector_tore(transcript:str)->Chroma:
    print("Building vector store")

    spliiter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=200)## why overlap because the content may lost
    chunks=spliiter.split_text(transcript)

    docs=[
        Document(page_content=chunk,metadata={'chunk_index':i})
        for i,chunk in enumerate(chunks)
    ]

    embeddings=get_embbeding()
    vector_store=Chroma.from_documents(
        documents=docs,embedding=embeddings,collection_name=COLLECTION_NAME,persist_directory=CHROMA_DIR#3were we want to store perist direc
    )

    return vector_store

def load_vector_store()->Chroma:
    embeddings=get_embbeding()
    vector_store=Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )

    return vector_store

def get_retriever(vector_store:Chroma,k:int=4):
    return vector_store.as_retriever(search_type='similarity',search_kwargs={"k":k})




