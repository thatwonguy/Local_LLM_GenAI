[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Local Large Language Model Generative AI ChatBot

1. - [X] Don't feel like retraining the outer hidden layers of a pretrained nueral network model?  
2. - [X] Want to train a nueral network model but simply don't have any additional data?  
3. - [X] Have the data but dont have the resources to perform the computations?  
4. - [X] **No matter what, you simply want to have an alternative solution to chatgpt that no one can take away from you once you have it!**  

*If you answered yes to the questions above, you are in luck! Keep reading!*

This is a localized solution with a streamlit UI wrapped around it. Once you have downloaded Ollama and the Phi3 model, you no longer need internet access and can always run your very own LLM-ChatGPT-level interactive GenAI ChatBot and get your answers in a localized and isolated manner. This is one unique approach for a Chatbot application that uses open-source LLMs for chatting that can be used for General Chat, Code Generation, and all other use cases of Chatbots like ChatGPT. The response is very fast on a local PC with 16gb DDR4 Ram and an RTX 3060m with Microsoft **Phi3** model. The dolphin model, as of 2023, is the most uncensored version available and will more likely answer questions that other models won't answer. If you are reading this in the future, be aware that even better models are likely available now!

Type the following in terminal to get this running:

```
ollama run CognitiveComputations/dolphin-mistral-nemo
```


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


### Interactive Chat Interface
- Provides a user-friendly interface to interact with a custom GPT model.
- Users can input their queries and receive real-time responses from the model.

### Text-to-Speech Integration
- Converts model responses to speech using the TTSService.
- Plays audio responses directly within the app for an enhanced user experience.
- Functionality that allows end-user to select different audio generation for both input text and output text.

### Real-time Response Generation
- Displays model responses in real-time as they are generated.
- Allows users to stop response generation at any time with a stop button.

### Chat History Management
- Save and archive chat sessions for future reference.
- Load previous chats from the sidebar, including text and audio responses.
- Clearly indicates that archived chats can be loaded by double-clicking.

### Session State Management
- Utilizes Streamlit's session state to manage chat messages, model selection, and other stateful information.
- Ensures continuity of the chat session across different interactions.

### Model Selection
- Allows users to select from a list of available GPT models to interact with.
- Dynamically loads the selected model for generating responses.

### Stop Button for Response Generation
- Positioned near the chat input box for easy access.
- Provides the ability to halt ongoing response generation promptly.

### Audio Playback for Archived Chats
- Ensures that text-to-speech audio remains available for playback when loading archived chats.
- Stores audio responses alongside text messages for comprehensive chat history.

### Dynamic UI Updates
- Uses Streamlit's real-time update capabilities to reflect changes in the chat and UI elements dynamically.
- Ensures a smooth and interactive user experience without needing to refresh the page.
- ADA disability and accessibility compliant attempted use of color and modified UI experience. (work in progress for continued improvments)

# How to Use

### Start a Chat
- Enter your query in the input box and press Enter.
- The model will generate a response, which will be displayed and spoken aloud.

### Stop Response Generation
- Press the "Stop Generation" button next to the input box to halt the model's response.

### Save and Load Chats
- Save the current chat by clicking the "Save Chat" button and entering a name for the chat.
- Load a saved chat by double-clicking on the chat name in the sidebar.

### Switch Models
- Select a different GPT model from the dropdown to use a different model for generating responses.

## Contributing  
Feel free to contribute to this repository by forking and by a pull request.

For any issues, suggestions, or feature requests, please open an issue in the repository.
