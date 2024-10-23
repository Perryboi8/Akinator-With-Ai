import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

KEY1 = os.getenv("OPENAI_KEY1")
KEY2 = os.getenv("OPENAI_KEY2")
KEY = str(KEY1) + str(KEY2)

client = OpenAI(api_key=KEY)
MODEL = "gpt-4o-mini"


def Genre():
    confidence = 0
    iteration = 0
    indefinite = 0
    initial = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are trying to guess whatever character the user is thinking of based on user's answer to your (y)es or (n)o questions."},
            {"role": "user", "content": "Start with your first question."}
        ],
        temperature=0.5,
    )
    question = initial.choices[0].message.content

    iteration += 1
    print("\n" + question)
    answer = input("Your Answer: ")
    if (answer != 'y') and (answer != 'n'):
            indefinite += 1
    bglog = f"Question {iteration} : {question}, User answer {iteration} : {answer}; \n"
    print(bglog)
    ############# first question should be real person or not, base on first question, decide which tree to use (genre, or origin?), or, split

    while (confidence < 85) and (iteration < 10) and (indefinite < 15):
    
        loop = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": bglog},
                {"role": "system", "content": "You are trying to narrow down the guess of whatever character the user is thinking of based on user's answer to your questions from the log above."},
                {"role": "user", "content": "Based on the log above with answers to previous questions, proceed with more specific question to narrow down the guess, don't repeat questions that have already been asked, don't say anything other than the question itself, don't ask if it's a specific named character"}
            ],
            temperature=0.5,
        )
        question = loop.choices[0].message.content

        iteration += 1
        print(question)
        answer = input("Your Answer: ")

        if (answer != 'y') and (answer != 'n'):
            indefinite += 1
        bglog += f"Question {iteration} : {question}, User answer {iteration} : {answer}; \n"
        print(bglog)

        if (iteration >= 4): # after certain iteration, starting to confirm genre confidence
    
            genreConfidence = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "Based on the log of answers provided by the user, you are making a guess of genre now."},
                    {"role": "user", "content": bglog},
                    {"role": "user", "content": "Answer only in number from 0 to 100, with 0 being the lowest, how confident are you making an accurate genre guess based on the log?"}
                ],
                temperature=0.4,
            )
            confidence = int(genreConfidence.choices[0].message.content)
            print(confidence)


    if (confidence >= 85) or (iteration >= 10) or (indefinite >= 15):
    
        betaGuess = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Based on the log of answers provided by the user, you are making a guess of genre now."},
                {"role": "user", "content": bglog},
                {"role": "user", "content": "What genre/setting you think of? Don't say anything other than detailed description of genre/setting."}
            ],
            temperature=0.5,
        )
        bgGuess = betaGuess.choices[0].message.content
        print(bgGuess)

    
        genre = str(bglog + "\nGenre description: " + bgGuess + "\n") # local? test output
    
        return genre
        


### returned genre = none, randomly?

########################


def Guess():
    bglog = Genre()
    confidence = 0
    iteration = 0
    indefinite = 0

    while (confidence < 90) and (iteration < 10) and (indefinite < 15):
    
        loop = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": bglog},
                {"role": "system", "content": "You are trying to narrow down the guess of whatever character the user is thinking of based on user's answer to your questions from the log above."},
                {"role": "user", "content": "Based on the log above with answers to previous questions, proceed with more specific question to narrow down the guess, don't repeat questions that have already been asked, don't say anything other than the question itself, don't ask if it's a specific named character"}
            ],
            temperature=0.6,
        )
        question = loop.choices[0].message.content

        iteration += 1
        print(question)
        answer = input("Your Answer: ")
        if (answer != 'y') and (answer != 'n'):
            indefinite += 1
        bglog += f"Question {iteration} : {question}, User answer {iteration} : {answer}; \n"
        print(bglog)

        if (iteration >= 4): # after certain iteration, starting to confirm chara confidence
    
            genreConfidence = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "Based on the log of answers provided by the user, you are making a guess of character now."},
                    {"role": "user", "content": bglog},
                    {"role": "user", "content": "Answer only in number from 0 to 100, with 0 being the lowest, how confident are you making an accurate genre guess based on the log?"}
                ],
                temperature=0.45,
            )
            confidence = int(genreConfidence.choices[0].message.content)
            print(confidence)


    if (confidence >= 90) or (iteration >= 10) or (indefinite >= 15): 
    
        betaGuess = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Based on the log of answers provided by the user, you are making a guess of character now."},
                {"role": "user", "content": bglog},
                {"role": "user", "content": "What character you think of? Don't say anything other than character name."}
            ],
            temperature=0.6,
        )
        bgGuess = betaGuess.choices[0].message.content
        print("Guess: " + bgGuess)
    
        return 0
    
Guess()
