import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

KEY1 = os.getenv("OPENAI_KEY1")
KEY2 = os.getenv("OPENAI_KEY2")
KEY = str(KEY1) + str(KEY2)

client = OpenAI(api_key=KEY)
MODEL = "gpt-4o-mini"


confidence = 0
iteration = 0

initial = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are trying to guess whatever character the user is thinking of based on user's answer to your (y)es or (n)o questions."},
        {"role": "user", "content": "Start with your first question."}
    ]
)
question = initial.choices[0].message.content

print(question)
answer = input("Your Answer: ")

if answer.lower() == "yes" or answer.lower() == "no":
    confidence += 6  # Sample confidence increment, 10 successful input = enough confidence for a guess 

iteration += 1
log = f"Question {iteration} : {question}, User answer {iteration} : {answer}; \n"
print(log)

while confidence < 60 and iteration < 10: # Sample confidence threshold
    
    loop = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": log},
            {"role": "system", "content": "You are trying to narrow down the guess of whatever character the user is thinking of based on user's answer to your questions from the log above."},
            {"role": "user", "content": "Based on the log above with answers to previous questions, proceed with more specific question to narrow down the guess, don't repeat questions that have already been asked."}
        ]
    )
    question = loop.choices[0].message.content

    iteration += 1
    print(question)
    answer = input("Your Answer: ")

    if answer.lower() == "yes" or answer.lower() == "no":
        confidence += 10

    log += f"Question {iteration} : {question}, User answer {iteration} : {answer}; \n"
    print(log)

if confidence >= 60 or iteration >= 10:
    
    guess = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Based on the log of answers provided by the user, you are making a guess now."},
            {"role": "user", "content": log},
            {"role": "user", "content": "What character do you think of?"}
        ]
    )
    print(f"Guess: {guess.choices[0].message.content}")
