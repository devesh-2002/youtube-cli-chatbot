import os
import openai
import requests
import re
from typing import List, Union, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_video_details(video_id: str) -> Optional[Dict[str, Any]]:
    url = f"https://www.googleapis.com/youtube/v3/videos?key={YOUTUBE_API_KEY}&part=snippet&id={video_id}&part=contentDetails,statistics"
    response = requests.get(url)
    data = response.json()
    if 'items' in data and data['items']:
        return data['items'][0]
    else:
        return None

def contains_valid_youtube_id(message: str) -> Union[Dict[str, Any], bool]:
    pattern = r'[a-zA-Z0-9_-]{11}'
    match = re.search(pattern, message)
    if match:
        video_id = match.group(0)
        return get_video_details(video_id)
    else:
        return False

def search_videos(query: str, max_results: int = 5) -> Optional[List[Dict[str, Any]]]:
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&part=snippet&q={query}&maxResults={max_results}&type=video"
    response = requests.get(url)
    data = response.json()
    if 'items' in data and data['items']:
        return data['items']
    else:
        return None

def call_language_model(messages: List[Dict[str, Any]], model: str = "gpt-3.5-turbo") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

def generate_search_message(message: str) -> str:
    return call_language_model([
        {"role": "system", "content": "You are a specialized YouTube Summarize and Search assistant. You can have access to a particular video. Your primary role is to help users find relevant videos on YouTube. Your responses should be concise and directly address the user's query. Remember, you're here to assist with summarizing videos and searching for new ones. Don't go off-topic."},
        {"role": "user", "content": f"""Based on the {message}, determine if the user's intent is to search for a video. Respond with 'Yes' only when you are certain the user wants to search for a new video. Do not unnecessarily respond 'Yes' even if the user asks questions regarding the previous video.
        
        Say Yes only if the user really wants to search for a new video. Here are some examples:
        
        Examples for 'Yes' Response:
        1. User: "Can you recommend some videos about cooking?"
        Bot: "Yes"
        
        2. User: "I'm looking for tutorials on digital marketing."
        Bot: "Yes"
        
        3. User: "Do you have any suggestions for workout routines?"
        Bot: "Yes"
        4. User : "Some Videos on ML"
        Bot : "Yes"
        5. User : Search for Hyperledger 
        Bot : "Yes"
        Examples for 'No' Response:
        1. User: "Summarize this video about machine learning."
        Bot: "No"
        
        2. User: "What's the length of the video 'How to bake a cake'?"
        Bot: "No"
        
        3. User: "How many views does the video 'Python tutorial' have?"
        Bot: "No"
        
        Don't forget, you're a YouTube chatbot focused on searching and summarizing YouTube videos. Only respond with 'Yes' or 'No'."""},
    ])

def chatbot() -> None:
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": "You are a helpful Youtube search and summarize chatbot. You have to only and only answer on the youtube related questions. Please it is very important to not divert."},
    ]

    while True:
        message: str = input("User: ")

        if contains_valid_youtube_id(message):
            video_details: Union[Dict[str, Any], bool] = contains_valid_youtube_id(message)
            if isinstance(video_details, dict):
                messages.append({"role": "user", "content": str(video_details)})
                chat_message: str = call_language_model([
                    {"role": "system", "content": f"Give answer based on the Message : {message} and Video Details : {video_details}. Be to the point and do not exaggerate."},
                    {"role": "user", "content": f"Give answer based on the Message : {message} and Video Details : {video_details}. Be to the point and do not exaggerate"}
                ])
                print(chat_message)
                messages.append({"role": "user", "content": chat_message})
            continue

        if message.lower() == "quit":
            break
            
        search_message: str = generate_search_message(message)

        if search_message.lower().startswith("yes"):
            query: str = message.strip()
            videos: Optional[List[Dict[str, Any]]] = search_videos(query)
            if videos:
                search_results: str = "\n".join([f"{i+1}. {video['snippet']['title']}: https://www.youtube.com/watch?v={video['id']['videoId']}" for i, video in enumerate(videos)])
                print("Search Results:")
                print(search_results)
                messages.append({"role": "user", "content": search_results})
            else:
                print("No search results found.")
            continue

        messages.append({"role": "user", "content": message})

        chat_message: str = call_language_model(messages)
        print(f"Bot: {chat_message}")
        messages.append({"role": "assistant", "content": chat_message})

def evaluate_search_message(message: str) -> str:
    return generate_search_message(message)

def evaluate_chatbot() -> None:
    test_cases: List[Dict[str, str]] = [
        {
            "message": "Can you recommend some videos about cooking?",
            "expected_output": "Yes"
        },
        {
            "message": "Summarize this video : https://www.youtube.com/watch?v=O71vKZ6WBf8",
            "expected_output": "No"
        },
        {
            "message": "Do you have any suggestions for workout routines?",
            "expected_output": "Yes"
        },
        {
            "message": "Some Videos on ML",
            "expected_output": "Yes"
        },
        {
            "message": "What's the length of the video 'How to bake a cake'?",
            "expected_output": "No"
        },
        {
            "message": "How many views does the video 'Python tutorial' have?",
            "expected_output": "No"
        }
    ]
    
    total_tests: int = len(test_cases)
    passed_tests: int = 0
    
    for test_case in test_cases:
        print("Test Case:", test_case["message"])
        actual_output: str = evaluate_search_message(test_case["message"])
        expected_output: str = test_case["expected_output"]
        print("Expected Output:", expected_output)
        print("Actual Output:", actual_output)
        if actual_output.lower().strip() == expected_output.lower().strip():
            print("Test Passed")
            passed_tests += 1
        else:
            print("Test Failed")
        print("="*50)
    
    accuracy: float = (passed_tests / total_tests) * 100
    print(f"Accuracy: {accuracy}%")

if __name__ == "__main__":
    print("Start chatting with the bot (type 'quit' to stop)!")
    chatbot()
    # evaluate_chatbot()
