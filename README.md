# youtube-cli-chatbot
This is a Youtube Summarizer and Search based CLI Chatbot.

## Setup and Usage Instructions
1. Fork and Clone the repository.
2. Make sure to have Python installed in the local system.
3. Create a .env file in the folder with OPENAI_KEY and YOUTUBE_API_KEY in it.
```
YOUTUBE_API_KEY = 
OPENAI_API_KEY = 
```
4. Create a virtual environment
```
virtualenv env
```
5. Activate the environment :
On Bash
```
source env/Scripts/activate
```
Windows : 
```
env/Scripts/activate
```
6. Install the packages from requirements.txt
```
pip install -r requirements.txt
```
7. Run ```python app.py``` in the terminal
8. For testing the evaluation script, go to app.py and uncomment ```evaluate_chatbot()```.
