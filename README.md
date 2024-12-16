A remake of the popular Akinator web based game using artificial intelligence to respond and further pinpoint the character that the user is thinking. 
CURRENTLY WIP

# REQUIREMENTS
1. Python
2. Python Django
3. Python OpenAi
4. Ollama and Llama 3.2 Model
   
# Django Installation:
1. Go to the following link and download Django https://docs.djangoproject.com/en/5.1/topics/install/  Django is used as a Web Framework using Python. Alternatively, in terminal use "python -m pip install django"
2.  After Installing Django you will also need to install the debug tool bar to install that please run this command "python -m pip install django-debug-toolbar"
# OpenAI Installation:
1. Go into your terminal and type the following, "pip install openai == 0.28" this will install openai which lets you use their chatbots on their platform.
2. In terminal, use the command "export OPENAI_API_KEY="your_api_key_here". replace your openai key with the "your_api_key_here" (may be provided).
# Ollama/Llama3.2 Installation:
1. Go to the following link and download Ollama for the respective OS [https://ollama.com/download/windows]. Ollama is an open source tool used to run Large Language Models (allows us to run Llama 3.2)
2. After installing Ollama, make sure Ollama is running (Check in taskbar).
3. Go to terminal and run "ollama pull llama3.2"
4. Once done, Ollama and the Llama3.2 model will be successfully installed!

# How to Run:
1. Navigate to the Django-Website-Akinator directory in terminal.
2. Run "python runserver manage.py"
3. Make sure Ollama is running via opening the application.
4. Visit the website with the given link (default https://127.0.0.1:8000)

# How to Play
1. Press the play button.
2. To play with OpenAI model, skip step 3 and go to step 4.
3. To play with Llama3.2 model, press the Llama button in the top left.
4. Think of a character or person in your head.
5. After deciding a character or person, answer the questions based off of your character. Ex: If you are thinking of Joe Biden and the prompt asks "Is your Character a Male", press the green "Yes" button.
6. If you are unsure about the question, press "I don't know". If you're unsure but want to add additional information, type it in the textbox and press Enter on your keyboard. Ex: If the question is "Is your character from literature", you can type "They're from a comic book".
7. After a certain amount of guesses, the AI will guess your character. If it is correct hit, "Yes". If it is incorrect, hit "No"
