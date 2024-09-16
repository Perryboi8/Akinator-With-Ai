import ollama
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import json

template = """""
Answer the question below.
Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model='llama3.1')
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def conversation():
    context = ""
    while True:
        user_input = input("You: ")
        result = chain.invoke({"context": context, "question": user_input})
        print("Akinator: ", result)
        context += f"\nUser: {user_input}\nAkinator: {result}"

def test():
    list = []
    dictionary = {}
    for x in range(20):
        response = ollama.chat(model='llama3.1', messages= [
        {
            'role': 'user',
            'content': 'reply without any extraneous action. ask a yes or no question to try to get clues as to what person i am thinking of. only ask the question. only one sentence. try to ask questions that help narrow down the answer based off the list. the list will be in the format: question followed by the answer to that question. do not ask similar questions already on the list: ' + json.dumps(dictionary)
        },
        ])
        print(response['message']['content'])
        input1 = input()
        dictionary.update({response['message']['content']: input1})
    response = ollama.chat(model='llama3.1', messages= [
        {
            'role': 'user',
            'content': 'reply without any extraneous action. only say the person you are thinking of. do not say anything other than that. guess who i am thinking of based off clues i gave you. the format of the clue will be "question" followed by "answer to the question" for example, only say "Gordon Ramsey". if the character is from a movie, do not say their actor name but the character they play. my person is ' + json.dumps(dictionary)
        },
    ])
    print(response['message']['content'])

def answer():
    response = ollama.chat(model='llama3.1', messages= [
        {
            'role': 'user',
            'content': 'reply without any extraneous action. only say the person you are thinking of. do not say anything other than that. guess who i am thinking of based off clues i gave you. the format of the clue will be "question" followed by "answer to the question" for example, only say "Gordon Ramsey". if the character is from a movie, do not say their actor name but the character they play. my person is ' + context
        },
    ])
    print(response['message']['content'])

os.system('clear')
print("Welcome to Akinator! I am the best at guessing characters you are thinking of. Please think of a character!")
print("Please type 'ready' when you got it!")
ready = input().strip().lower()
while ready != "ready":
    print("Please type 'ready' when you got it!")
    ready = input().strip().lower()
print("Alright! Here goes. My first question is")
conversation()
answer()
