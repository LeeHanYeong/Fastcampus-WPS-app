from apiclient import discovery
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

API_KEY = 'AIzaSyDiarbwPOxSkXmNPfdv8UtHcZM6KySpk34'
SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def youtube_search_list(keyword):
    youtube = build(SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    search_response = youtube.search().list(
        q=keyword,
        part='id',
        maxResults=50,
    ).execute()
    video_id_list = [item['id'].get('videoId', '') for item in search_response['items']]

    detail_list_response = youtube.videos().list(
        part='id,snippet,statistics',
        id=','.join(video_id_list)
    ).execute()

    ret = {
        'prevPageToken': search_response.get('prevPageToken'),
        'nextPageToken': search_response.get('nextPageToken'),
        'pageInfo': search_response.get('pageInfo'),
        'items': detail_list_response['items'],
    }
    return ret


def youtube_search_detail(video_id):
    youtube = build(SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    detail_response = youtube.videos().list(
        part='id,snippet,statistics',
        id=video_id,
    ).execute()

    return detail_response
