import ollama
import logging
import openai
import os

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_next_question(context, model="llama3.2"):
    """
    Generate the next question using the AI model.
    Build history from the context list and ask relevant questions.
    """
    try:
        history_prompt = "\n".join(context)
        response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': """reply without any extraneous action. ask a yes or no question to try to get clues as to what person I am thinking of.
                                only ask the question. only one sentence. try to ask questions that help narrow down the answer based off the list.
                                the list will be in the format: question followed by the answer to that question. the person can be famous, or they can be not that famous.
                                the answers to the question might not be exactly true, keep a slight variance in mind. if there are no questions about if the person is real life person or not, ask that first.
                                only ask relevant questions. do not ask similar questions to what is already on the list:
                                """ + history_prompt
                }
            ],
        )
        question = response['message']['content']
        logger.debug(f"Generated question: {question}")
        return question.strip()
    except Exception as e:
        logger.error(f"Error generating question: {e}")
        return "An error occurred while generating the question."

def make_guess(context, model="llama3.2"):
    """
    Make a final guess using the AI model.
    """
    try:
        history_prompt = "\n".join(context)
        response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': 'reply without any extraneous action. only say the person you are thinking of. do not say anything other than that. guess who I am thinking of based off clues I gave you. the format of the clue will be "question" followed by "answer to the question". '
                               'If the character is from a movie, do not say their actor name but the character they play. My person is ' + history_prompt
                },
            ],
        )
        guess = response['message']['content']
        logger.debug(f"Generated guess: {guess}")
        return guess.strip()
    except Exception as e:
        logger.error(f"Error making a guess: {e}")
        return "An error occurred while making the guess."

def evaluate_confidence(context, model="llama3.2"):
    """
    Get confidence level for the AI's guess.
    """
    try:
        history_prompt = "\n".join(context)
        response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': 'reply without any extraneous action. Based on the conversation history, if you were to make an attempt to guess the character/person, what is the likelihood of you being correct, on a scale of 0-10? Only say the number and nothing else. Here is the history: ' + history_prompt
                },
            ],
        )
        confidence = response['message']['content']
        logger.debug(f"Generated confidence: {confidence}")
        return confidence.strip()
    except Exception as e:
        logger.error(f"Error evaluating confidence: {e}")
        return "0"
    

def generate_image(prompt):
    """
    Generate an image using OpenAI's DALL-E based on a prompt.
    """
    try:
        print("Attempting to generate an image with the prompt:", prompt)
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Number of images to generate
            size="512x512"  # Image resolution
        )
        print("openai.Image.create response:", response)
        image_url = response["data"][0]["url"]
        print("Image URL:", image_url)
        return image_url
    except Exception as e:
        print("Error generating image:", e)
        logger.error(f"Error generating image: {e}")
        return None
