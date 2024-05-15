# Local_LLM_Chatbot
This solution needs internet access to use api calls through the ollama software, similar to how you need access for ChatGPT, but nonetheless, it is still a very effective and powerful alternative and takes away the monopoly from ChatGPT. 

A Chatbot application that uses open-source LLMs for chatting that can be used for General Chat, Code Generation, and all other use cases of Chatbots like ChatGPT. The response is very fast on a local PC with 16gb DDR4 Ram and an RTX 3060m with Microsoft Phi3 model.

## Prerequisites
### This repo assumes you already have Ollama and a model installed.
1. You have to go to https://ollama.com/ and download and install ollama software on your local machine.
2. Once it is installed you need to select a model to install from the following url on your local machine: https://ollama.com/library.

To get started with this project:  
1. Have python installed on your machine (version 3.6 or above).
2. Install the necessary packages by running the following in a virtual environment preferably:
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
git clone https://github.com/thatwonguy/Local_LLM_Chatbot.git
```

Then navigate into the project directory:
```
cd Local_LLM_Chatbot
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
