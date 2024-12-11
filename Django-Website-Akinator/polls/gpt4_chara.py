import os
from dotenv import load_dotenv
import openai

load_dotenv()

KEY1 = os.getenv("OPENAI_KEY1")
KEY2 = os.getenv("OPENAI_KEY2")
KEY = str(KEY1) + str(KEY2)

openai.api_key = KEY
MODEL = "gpt-4o-mini"

def get_initial_question():
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are trying to guess a character/person's name based on the user's answers to yes or no questions."},
            {"role": "user", "content": "Start with your first question."}
        ],
        temperature=0.7,
        frequency_penalty=0.8,
        presence_penalty=0.7,
    )
    return response['choices'][0]['message']['content']

def get_next_question(log, previous_questions):
    try:
        previous_questions_str = "\n".join([f"- {q}" for q in previous_questions])
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": (
                    "You are a character/person-guessing assistant. Based on the user's answers, "
                    "generate a new, specific, and relevant question to narrow down the user's choice. "
                    "Avoid repeating previous questions."
                )},
                {"role": "user", "content": f"Answers so far:\n{log}\n\nPrevious questions:\n{previous_questions_str}"},
                {"role": "user", "content": "Generate a new question based on the answers and avoid repeating previous questions. Do not ask about specific named entities. Only provide the question."}
            ],
            temperature=0.7,
            presence_penalty=0.8,
            frequency_penalty=0.8,
        )
        new_question = response['choices'][0]['message']['content'].strip()
        if new_question and new_question not in previous_questions:
            return new_question
        else:
            return None
    except Exception as e:
        print(f"Error in get_next_question: {e}")
        return None

def evaluate_genre_confidence(log):
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are evaluating the confidence level for identifying the character genre or person background information based on the user's answers."},
                {"role": "user", "content": log},
                {"role": "user", "content": "Respond with a number between 0 and 100 indicating your confidence level. Answer only in digits."}
            ],
            temperature=0.3,
        )
        confidence = int(response['choices'][0]['message']['content'].strip())
        return confidence
    except Exception as e:
        print(f"Error in evaluate_genre_confidence: {e}")
        return 0  # Default to 0 confidence in case of an error

def evaluate_name_confidence(log):
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Evaluate confidence level for the final character/person name based on the user's answers."},
                {"role": "user", "content": log},
                {"role": "user", "content": "Respond with a number between 0 and 100 indicating your confidence level. Answer only in digits."}
            ],
            temperature=0.3,
        )
        confidence = int(response['choices'][0]['message']['content'].strip())
        return confidence
    except Exception as e:
        print(f"Error in evaluate_name_confidence: {e}")
        return 0

def identify_genre(log):
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Identify the genre of a character or background information of a person based on the user's answers provided in the log."},
                {"role": "user", "content": log},
                {"role": "user", "content": "Provide the genre or background information as a concise description."}
            ],
            temperature=0.4,
        )
        genre = response['choices'][0]['message']['content'].strip()
        return genre
    except Exception as e:
        print(f"Error in identify_genre: {e}")
        return "Unknown Genre"  # Default in case of an error

def make_final_guess(log):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Based on the log of answers, make your final guess of character/person name."},
            {"role": "user", "content": log},
            {"role": "user", "content": "Provide only the character/person name of the final guess."}
        ],
        temperature=0.6,
        presence_penalty=0.6,
        frequency_penalty=0.5,
    )
    return response['choices'][0]['message']['content']
