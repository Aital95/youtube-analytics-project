from googleapiclient.discovery import build


class Channel:
    def __init__(self, channel_id: str, api_key: str):
        self.id = channel_id
        self.title = None
        self.description = None
        self.custom_url = None
        self.view_count = None
        self.subscriber_count = None
        self.video_count = None

        youtube = build('youtube', 'v3', developerKey=api_key)
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

    def print_info(self):
        print(f'Название канала: {self.title}')
        print(f'Описание канала: {self.description}')
        print(f'Пользовательский URL: {self.custom_url}')
        print(f'Количество просмотров: {self.view_count}')
        print(f'Количество подписчиков: {self.subscriber_count}')
        print(f'Количество видео: {self.video_count}')