import os
import json

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    def __init__(self, channel_id: str):
        self.id = channel_id
        self.title = None
        self.description = None
        self.custom_url = None
        self.view_count = None
        self.subscriber_count = None
        self.video_count = None
        self.url = f'https://www.youtube.com/channel/{channel_id}'

        request = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        )
        response = request.execute()

        if response['pageInfo']['totalResults'] == 0:
            raise ValueError(f'Channel with ID "{channel_id}" not found.')
        elif response['pageInfo']['totalResults'] > 1:
            raise ValueError(f'Multiple channels found with ID "{channel_id}".')
        else:
            channel = response['items'][0]

            self.title = channel['snippet']['title']
            self.description = channel['snippet']['description']
            self.custom_url = channel['snippet']['customUrl'] if 'customUrl' in channel['snippet'] else None
            self.view_count = channel['statistics']['viewCount']
            self.subscriber_count = channel['statistics']['subscriberCount']
            self.video_count = channel['statistics']['videoCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def print_info(self):
        info = f'Название канала: {self.title}\nОписание: {self.description}\nПользовательский URL: {self.custom_url}\n' \
               f'Количество просмотров: {self.view_count}\nКоличество подписчиков: {self.subscriber_count}\n' \
               f'Количество видео: {self.video_count}'
        return info

    @classmethod
    def get_service(cls):
        return youtube

    def to_json(self, filename: str):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'custom_url': self.custom_url,
            'view_count': self.view_count,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'url': self.url
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
