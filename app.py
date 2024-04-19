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

    
def chatbot():
    messages = [
        {"role": "system", "content": "You are a helpful Youtube chatbot. You have to only and only answer on the youtube related questions. Please it is very important to not divert."},
    ]

    while True:
        message = input("User: ")

        if contains_valid_youtube_id(message):
            video_details = contains_valid_youtube_id(message)
            messages.append({"role": "user", "content": str(video_details)})
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Give answer based on the Message : {message} and Video Details : {video_details}. Be to the point and do not exaggerate."},
                    {"role": "user", "content": f"Give answer based on the Message : {message} and Video Details : {video_details}. Be to the point and do not exaggerate"}
                ]
            )
            chat_message = response.choices[0].message.content
            print(chat_message)
            messages.append({"role": "user", "content": chat_message})
            continue

        if message.lower() == "quit":
            break

        if message.lower().startswith("search"):
            query = message[7:].strip()
            videos = search_videos(query)
            if videos:
                search_results = "\n".join([f"{i+1}. {video['snippet']['title']}: https://www.youtube.com/watch?v={video['id']['videoId']}" for i, video in enumerate(videos)])
                print("Search Results:")
                print(search_results)
            else:
                print("No search results found.")
            continue

        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        chat_message = response.choices[0].message.content
        print(f"Bot: {chat_message}")
        messages.append({"role": "assistant", "content": chat_message})

if __name__ == "__main__":
    print("Start chatting with the bot (type 'quit' to stop)!")
    chatbot()
