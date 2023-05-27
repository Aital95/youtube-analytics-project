import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        try:
            api_key = os.getenv('YT_API_KEY')
            youtube = build('youtube', 'v3', developerKey=api_key)
            video_response = youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            ).execute()

            video_result = video_response.get('items')[0]

            self.id = video_id
            self.title = video_result['snippet']['title']
            self.url = f'https://www.youtube.com/watch?v={video_id}'
            self.view_count = video_result['statistics']['viewCount']
            self.like_count = video_result['statistics']['likeCount']
        except:
            self.id = video_id
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        try:
            api_key = os.getenv('YT_API_KEY')
            youtube = build('youtube', 'v3', developerKey=api_key)
            video_response = youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            ).execute()

            video_result = video_response.get('items')[0]

            super().__init__(video_id)
            self.playlist_id = playlist_id
        except:
            super().__init__(video_id)
            self.playlist_id = None
