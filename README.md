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
8. For testing the evaluation script, go to app.py and uncomment ```evaluate_chatbot()``` in the line 174.


## Assumptions:
1. **User Intent Recognition** : The chatbot assumes that it can accurately recognize user intents based on the provided input. It relies on a language model (GPT-3.5) to determine whether the user's message indicates a search intent or a request for video summarization.

2. **Valid YouTube URLs**: The chatbot assumes that users will provide valid YouTube video URLs when requesting video summarization. It uses a regex pattern to validate the URLs.

3. **Search Query Handling:** When the chatbot detects a search intent, it processes the entire message following the search keywords as the search query. However, it may struggle to differentiate between the search query and other content in the message, especially in complex or ambiguous scenarios.

4. **Video Summarization:** For video summarization, the chatbot assumes that it can access the necessary data about the video (e.g., title, publication date, view count) using the YouTube Data API. It assumes that the API response will contain the required information in the expected format.

## Potential Issues:
1. **Accuracy of Intent Recognition:** The accuracy of recognizing user intents heavily depends on the language model's performance. If the model misinterprets the user's message, it may lead to incorrect actions or responses by the chatbot.

2. **Parsing YouTube URLs:** The regex pattern used to validate YouTube video URLs may not cover all possible variations of valid URLs. This could result in false negatives or false positives when validating user input.

3. **Search Query Ambiguity:** Since the chatbot treats the entire message following the search keywords as the search query, it may misinterpret complex or ambiguous queries. This could lead to irrelevant search results or misunderstandings of user intent

4. **API Rate Limits and Quotas:** The chatbot relies on the YouTube Data API to fetch video details and search results. There's a risk of hitting API rate limits or quotas, especially if the chatbot experiences heavy usage or if the API usage is not properly managed.

5. **Handling of Non-YouTube URLs:** The chatbot currently assumes that any URL provided by the user is a YouTube video URL. If users provide URLs to other websites or resources, the chatbot may not handle them correctly or may fail to recognize them as invalid input.
