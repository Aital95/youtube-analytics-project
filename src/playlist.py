import datetime
import requests

class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None

        self._fetch_playlist_info()

    def _fetch_playlist_info(self):
        api_key = '<YOTUBE_API_KEY>'
        playlist_url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={self.playlist_id}&key={api_key}"

        response = requests.get(playlist_url)
        data = response.json()

        if 'items' in data:
            playlist_info = data['items'][0]['snippet']
            self.title = playlist_info['title']
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        api_key = '<YOTUBE_API_KEY>'
        videos_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={self.playlist_id}&key={api_key}"

        response = requests.get(videos_url)
        data = response.json()

        total_duration = datetime.timedelta()

        if 'items' in data:
            for item in data['items']:
                duration = item['contentDetails']['duration']
                video_duration = datetime.timedelta()
                for time_unit in ['H', 'M', 'S']:
                    if time_unit in duration:
                        time_value = int(duration.split(time_unit)[0])
                        if time_unit == 'H':
                            video_duration += datetime.timedelta(hours=time_value)
                        elif time_unit == 'M':
                            video_duration += datetime.timedelta(minutes=time_value)
                        elif time_unit == 'S':
                            video_duration += datetime.timedelta(seconds=time_value)
                total_duration += video_duration

        return total_duration

    def show_best_video(self):
        api_key = '<YOTUBE_API_KEY>'
        videos_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={self.playlist_id}&key={api_key}"

        response = requests.get(videos_url)
        data = response.json()

        best_video = None
        max_likes = 0

        if 'items' in data:
            for item in data['items']:
                likes = item['snippet']['statistics']['likeCount']
                if likes > max_likes:
                    max_likes = likes
                    best_video = item['snippet']['resourceId']['videoId']

        if best_video:
            return f"https://youtu.be/{best_video}"

        return None