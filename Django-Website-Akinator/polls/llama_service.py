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
                    'content': """You are playing a game where you must guess a character I am thinking of. The character could be real or fictional, famous or obscure.

                                    Your task is to ask a yes or no question that helps you narrow down the possibilities. Only ask one question at a time, and the question must be highly relevant based off a history list.
                                    Rules:

                                    1. Begin with broad, general questions to narrow the category (e.g., "Is the character real?" or "Is the character male?").
                                    2. As you gather information, gradually transition to more specific questions that will help you narrow down the character.
                                    3. Avoid overly specific questions (e.g., "Is your character from Star Wars?") unless prior answers strongly suggest that level of detail.
                                    4. Do not repeat or rephrase any previous questions from the history. Ensure your question is unique and distinct.
                                    5. Ask questions that are strategic and logical, aimed at eliminating the largest number of possibilities.
                                    6. Your response should be a single sentence containing only the question.
                                    7. If they're not real, then they must be from a work of fiction.
                                    Based on this history, what is your next yes or no question? History of Questions and Answers:
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
                    'content': """Based on the conversation history, your task is to guess the character I am thinking of. The character could be real or fictional, famous or obscure.

                                    Rules:

                                    1. Make one confident guess about the character based solely on the information provided in the history.
                                    2. Your response should only include the name of the character and nothing else. Avoid any additional context, reasoning, or commentary.
                                    3. If the history doesn't provide enough information for a confident guess, make your best attempt while accounting for slight ambiguities in the answers.
                                    What is your guess? Here is the conversation history: """ + history_prompt
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
