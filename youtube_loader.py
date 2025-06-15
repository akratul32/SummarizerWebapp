# youtube_loader.py

from langchain_core.documents import Document
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

class CustomYouTubeTranscriptLoader:
    def __init__(self, video_url):
        self.video_url = video_url

    def extract_video_id(self):
        parsed_url = urlparse(self.video_url)
        if "youtube.com" in parsed_url.netloc:
            return parse_qs(parsed_url.query).get("v", [None])[0]
        elif "youtu.be" in parsed_url.netloc:
            return parsed_url.path.lstrip("/")
        return None

    def load(self):
        video_id = self.extract_video_id()
        if not video_id:
            raise ValueError("Invalid YouTube URL format.")
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = "\n".join([entry["text"] for entry in transcript])
        return [Document(page_content=full_text, metadata={"source": self.video_url})]
