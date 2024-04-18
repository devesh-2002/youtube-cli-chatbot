import requests
import argparse
from openai import OpenAI, Completion
from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY: str = os.getenv('YOUTUBE_API_KEY')
OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
print(OPENAI_API_KEY)
openai_client: OpenAI = OpenAI(api_key=OPENAI_API_KEY)

def search_videos(query: str) -> dict:
    url: str = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&part=snippet&type=video&q={query}"
    response: requests.Response = requests.get(url)
    data: dict = response.json()
    return data['items']

def get_video_details(video_id: str) -> dict:
    url: str = f"https://www.googleapis.com/youtube/v3/videos?key={YOUTUBE_API_KEY}&part=snippet&id={video_id}&part=contentDetails"
    response: requests.Response = requests.get(url)
    data: dict = response.json()
    return data['items'][0]

def ask_question_to_gpt(question: str, context: str) -> str:
    response: Completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{context} Do Not forget that you are YOUTUBE CLI CHATBOT. Do not divert yourself. "},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def create_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="CLI Chatbot for YouTube")
    subparsers: argparse._SubParsersAction = parser.add_subparsers(dest="command")

    search_parser: argparse.ArgumentParser = subparsers.add_parser("search", help="Search for videos")
    search_parser.add_argument("query", help="Search query")

    question_parser: argparse.ArgumentParser = subparsers.add_parser("question", help="Ask a question about a video")
    question_parser.add_argument("video_id", help="Video ID")
    question_parser.add_argument("question", help="Question")

    return parser

def search_command(args: argparse.Namespace) -> None:
    videos: dict = search_videos(args.query)
    for video in videos:
        print(video['snippet']['title'])

def question_command(args: argparse.Namespace) -> None:
    video_id: str = args.video_id
    question: str = args.question
    video_details: dict = get_video_details(video_id)
    transcript: str = video_details['snippet']['description']  
    context: str = " ".join([video_details['snippet']['title'], transcript])
    response: str = ask_question_to_gpt(question, context)
    print("Answer:", response)

def main() -> None:
    parser: argparse.ArgumentParser = create_parser()
    args: argparse.Namespace = parser.parse_args()

    if args.command == "search":
        search_command(args)
    elif args.command == "question":
        question_command(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
