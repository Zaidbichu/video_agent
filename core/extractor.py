## actionable items (if we want to perform action son videos like if in the video we have told what we need to do it will help us to make decison and on which question we are performing the decison)
# actionableitems decisons questions
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda

import os

def get_llm():
    return ChatMistralAI(model="mistral-small-latest",mistral_api_key=os.getenv("MISTRAL_API_KEY"),temperature=0.3)

def build_chain(system_prompt: str):
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{text}")
    ])

    return prompt | llm | StrOutputParser()


def extract_action_items(transcript:str)->str:
    chain=build_chain(
        "You are an expert meeting analyst from the meeting transcript"
        "extract all action items.for each provide:\n"
        "task description"
        "owner(who is responsible)"
        "-deadline (if mentioned else write not specified)\n\n"
        "-format as a numbered list.if none found say no actions items found"
    )

    return chain.invoke({'text':transcript})

def extract_key_decisions(transcript:str)->str:
    chain=build_chain(
        "you are an exper meeting analyst.from the meeting transcript"
        "extract all the key decisions made. fromat as numbered list"
        "if none found sat no key decisons found"
    )

    return chain.invoke({'text':transcript})

def extract_questions(transcript:str)->str:
    chain=build_chain(
        "from the meeting transcript extract all unresolved questions"
        "or topics needing foolow-up.format as a numbered list."
        "if none found say no open question found"
    )

    return chain.invoke({'text':transcript})

    












