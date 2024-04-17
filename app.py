import requests
import argparse
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai_client = OpenAI(OPENAI_API_KEY)

def search_videos(query):
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&part=snippet&type=video&q={query}"
    response = requests.get(url)
    data = response.json()
    return data['items']

def get_video_details(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?key={YOUTUBE_API_KEY}&part=snippet&id={video_id}&part=contentDetails"
    response = requests.get(url)
    data = response.json()
    return data['items'][0]

def ask_question_to_gpt(question, context):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0]['message']['content']

def create_parser():
    parser = argparse.ArgumentParser(description="CLI Chatbot for YouTube")
    subparsers = parser.add_subparsers(dest="command")

    search_parser = subparsers.add_parser("search", help="Search for videos")
    search_parser.add_argument("query", help="Search query")

    question_parser = subparsers.add_parser("question", help="Ask a question about a video")
    question_parser.add_argument("video_id", help="Video ID")
    question_parser.add_argument("question", help="Question")

    return parser

def search_command(args):
    videos = search_videos(args.query)
    for video in videos:
        print(video['snippet']['title'])

def question_command(args):
    video_id = args.video_id
    question = args.question
    video_details = get_video_details(video_id)
    transcript = "Replace this with actual transcript"  # Extract transcript from video details
    answer = ask_question_to_gpt(question, transcript)
    print("Answer:", answer)

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "search":
        search_command(args)
    elif args.command == "question":
        question_command(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
