import datetime
import json
import os

from googleapiclient.discovery import build
import isodate


api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


def printj(dict_to_print: dict) -> None:
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class PlayList:
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.title = ""
        self.url = ""
        self._fetch_playlist_data()

    def _fetch_playlist_data(self):
        playlist_response = youtube.playlists().list(
            id=self.playlist_id,
            part='snippet'
        ).execute()
        playlist = playlist_response['items'][0]['snippet']
        self.title = playlist['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self) -> datetime.timedelta:
        playlist_videos = youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50
        ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(
            part='contentDetails',
            id=','.join(video_ids)
        ).execute()

        total_duration = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self) -> str:
        playlist_videos = youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50
        ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(
            part='statistics',
            id=','.join(video_ids)
        ).execute()

        best_video = max(video_response['items'], key=lambda x: int(x['statistics']['likeCount']))
        best_video_id = best_video['id']
        best_video_url = f"https://youtu.be/{best_video_id}"

        return best_video_url
