import os
from dotenv import load_dotenv
import openai

load_dotenv()

KEY1 = os.getenv("OPENAI_KEY1")
KEY2 = os.getenv("OPENAI_KEY2")
KEY = str(KEY1) + str(KEY2)

openai.api_key = KEY
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
        iteration -= 1
    bglog = f"Question {iteration} : {question}, User answer {iteration} : {answer}; \n"
    # print(bglog)
    ############# first question should be real person or not, base on first question, decide which tree to use (genre, or origin?), or, split

    while (confidence < 85) and (iteration < 10) and (indefinite < 12):
    
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
            iteration -= 1
        bglog += f"Question {iteration} : {question}, User answer {iteration} : {answer}; \n"
        # print(bglog)

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
            # print(confidence)


    if (confidence >= 85) or (iteration >= 10) or (indefinite >= 12):
    
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
        # print(bgGuess)

    
        genre = str(bglog + "\nGenre description: " + bgGuess + "\n")
    
        return genre
        


def get_initial_question():
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are trying to guess whatever character the user is thinking of based on user's answer to your (y)es or (n)o questions."},
            {"role": "user", "content": "Start with your first question."}
        ],
        temperature=0.7,
        frequency_penalty=0.5,  #Makes it less likely for questions to repeat
        presence_penalty=0.6,   #Added to encourage asking new prompts/questions
    )
    return response['choices'][0]['message']['content']

# Function to get the next question based on the conversation history
def get_next_question(log):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are trying to narrow down the guess of whatever character the user is thinking of based on the user's answers. The log contains previous questions and answers. DO NOT repeat any questions that have already been asked or similar types of questions."},
            {"role": "user", "content": log},
            {"role": "user", "content": "Based on the log above with answers to previous questions, proceed with more specific question to narrow down the guess, don't repeat questions that have already been asked, don't say anything other than the question itself, don't ask if it's a specific named character."}
        ],
        temperature=0.7,
        presence_penalty=0.8,
        frequency_penalty = 0.8,
    )
    return response['choices'][0]['message']['content']

# Optional: Function to make a final guess based on the conversation log
def make_final_guess(log):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Based on the log of answers provided by the user, you are now making a guess of the character that you believe to be atleast 30 percent correct or after asking 25 questions."},
            {"role": "user", "content": log},
            {"role": "user", "content": "What character do you think of? Don't say anything other than the character name."}
        ],
        temperature=0.7,
        presence_penalty=0.6,
        frequency_penalty = 0.5,
    )
    return response['choices'][0]['message']['content']

### returned genre = none, randomly?

########################
