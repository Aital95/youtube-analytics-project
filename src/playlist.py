import datetime
import requests


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None

        self._fetch_playlist_info()

    def _fetch_playlist_info(self):
        api_url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={self.playlist_id}&key=YT_API_KEY"
        response = requests.get(api_url)
        data = response.json()

        if "items" in data and len(data["items"]) > 0:
            playlist_data = data["items"][0]
            self.title = playlist_data["snippet"]["title"]
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        else:
            raise ValueError("Invalid playlist ID")

    @property
    def total_duration(self):
        api_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={self.playlist_id}&key=YT_API_KEY"
        response = requests.get(api_url)
        data = response.json()

        total_duration = datetime.timedelta()

        if "items" in data:
            for item in data["items"]:
                duration = item["contentDetails"]["duration"]
                parsed_duration = self._parse_duration(duration)
                total_duration += parsed_duration

        return total_duration

    def _parse_duration(self, duration):
        time_values = duration.split("T")[-1]
        hours, minutes, seconds = map(int, time_values[:-1].split(":"))
        return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def show_best_video(self):
        api_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={self.playlist_id}&key=YT_API_KEY"
        response = requests.get(api_url)
        data = response.json()

        best_video = None
        max_likes = 0

        if "items" in data:
            for item in data["items"]:
                likes = int(item["snippet"]["statistics"]["likeCount"])
                if likes > max_likes:
                    max_likes = likes
                    best_video = item["snippet"]["resourceId"]["videoId"]

        if best_video is not None:
            return f"https://youtu.be/{best_video}"
        else:
            return None
