import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from core.vector_store import build_vector_tore,load_vector_store,get_retriever

def get_llm():
    return ChatMistralAI(model="mistral-small-latest",mistral_api_key=os.getenv("MISTRAL_API_KEY"),temperature=0.3)

def format_docs(docs):
    return "\n\n".join([doc.page_content() for doc in docs])

def build_rag_chain(transcript:str):
    vector_store=build_vector_tore(transcript)
    retriever=get_retriever(vector_store,k=4)

    llm=get_llm()

    prompt=ChatPromptTemplate.from_messages([
        ("system","""you are an expert meeting assistant.answer the isers questions based only on the meeting traanscript context provided below.
        if the answer is not found in context say:i could not found the context information in transcript.
        always be concise and precie if quoting someone mention it clearly.
        context from meeting transciprt{context}"""),
        ('human',"{question}")
        
    ])

    ## full lcel rag pipeline
    rag_chain=(
        {"context":retriever|RunnableLambda(format_docs),
         "question":RunnablePassthrough()}
         |prompt|llm|StrOutputParser()
    )

    return rag_chain

def load_rag_chain():
    vector_store=load_vector_store()
    retriever=get_retriever()
    llm=get_llm()
    prompt=ChatPromptTemplate.from_messages([
            ("system","""you are an expert meeting assistant.answer the isers questions based only on the meeting traanscript context provided below.
            if the answer is not found in context say:i could not found the context information in transcript.
            always be concise and precie if quoting someone mention it clearly.
            context from meeting transciprt{context}"""),
            ('human',"{question}")
            
        ])
    rag_chain=(
            {"context":retriever|RunnableLambda(format_docs),
             "question":RunnablePassthrough()}
             |prompt|llm|StrOutputParser()
        )
    
    return rag_chain

def ask_question(rag_chain,question:str)->str:
    print(f"question:{question}")
    answer=rag_chain.invoke(question)
    print(f"answer:{answer}")

    return answer

