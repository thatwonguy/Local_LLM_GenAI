[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Local Large Language Model Generative AI ChatBot

[ ] - Don't feel like retraining the outer hidden layers of a pretrained nueral network model?  
[ ] - Want to train a nueral network model but simply don't have any additional data?  
[ ] - Have the data but dont have the resources to perform the computations?  
[ ] - **No matter what, you simply want to have an alternative solution to chatgpt that no one can take away from you once you have it!**  

If you answered yes to the questions above, you are in luck! Keep reading!

This is a localized solution. Once you have downloaded Ollama and the Phi3 model, you no longer need internet access and can always run your very own LLM-ChatGPT-level interactive GenAI ChatBot and get your answers in a localized and isolated manner. This is one unique approach for a Chatbot application that uses open-source LLMs for chatting that can be used for General Chat, Code Generation, and all other use cases of Chatbots like ChatGPT. The response is very fast on a local PC with 16gb DDR4 Ram and an RTX 3060m with Microsoft **Phi3** model.

## Prerequisites
### This repo assumes you already have Ollama and a model installed.
1. You have to go to https://ollama.com/ and download and install ollama software on your local machine.
2. Once it is installed you need to select a model to install from the following url on your local machine: https://ollama.com/library. From this location pick Phi 3, a pretrained model by Microsoft, or feel free to test the other models.
   - Once Ollama is installed on your local machine, obtain the phi 3 model with the following:
     ```
     ollama run phi3
     ```

To get started with this project:  
1. Have python installed on your machine (version 3.6 or above).
2. Install the necessary packages by running the following in a virtual environment preferably.
     - To create a virtual environment with conda type the following:
          ```
          conda create -n venv python=3.11
          ```
       The above will create a new virtual environment using -named 'venv' and this environment will be python version 3.11.
      - Next you need to install the required python libraries with the following:
         ```
         pip install -r requirements.txt
         ```
         or
         ```
         pip install streamlit ollama
         ```

### Setup Instructions  
Follow these steps to set up and run the chatbot locally:

### Clone Repository  
Clone this repo to your local machine.
```
git clone https://github.com/thatwonguy/Local_LLM_GenAI
``` 

Then navigate into the project directory:
```
cd Local_LLM_GenAI
```
Execute the following command to start the Chatbot:
```
streamlit run app.py
```  
## Features Overview 

Our chatbot provides various features for an engaging user experience, including:

- **Selecting Models**: Choose from multiple pre-trained OLLAMA models to customize the conversation's tone and style.
- **Chat History**: View past conversations with options to edit or delete entries.
- **Saving Chats**: Save individual chat sessions for future reference, allowing users to revisit their interactions.
- **New Chat**: Initiate fresh conversations with the selected model and save the conversation if desired.

## Contributing  
Feel free to contribute to this repository by forking and by a pull request.

For any issues, suggestions, or feature requests, please open an issue in the repository.
