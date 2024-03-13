from googleapiclient.discovery import build
import random
from flask import Flask, render_template, request

# Set up YouTube API service
youtube = build("youtube", "v3", developerKey="AIzaSyAU2FyR1mDn7dLiJoM9LT6YnDO3lzdH4K0")

def get_channel_id(channel_name):
    search_response = youtube.search().list(
        q=channel_name,
        part="id",
        type="channel"
    ).execute()

    # Assuming the first result is the correct channel
    if 'items' in search_response and len(search_response['items']) > 0:
        return search_response['items'][0]['id']['channelId']
    else:
        return None


def get_video_ids_for_channel(channel_name, max_results=100):
    channel_id = get_channel_id(channel_name)
    if not channel_id:
        return None

    video_ids = []
    next_page_token = None

    while True:
        playlist_items_response = youtube.channels().list(
            part="contentDetails",
            id=channel_id,
            maxResults=max_results,
            pageToken=next_page_token
        ).execute()

        for channel in playlist_items_response["items"]:
            uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

            playlist_items = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=max_results,
                pageToken=next_page_token
            ).execute()

            for playlist_item in playlist_items["items"]:
                video_ids.append(playlist_item["contentDetails"]["videoId"])

            next_page_token = playlist_items.get("nextPageToken")

        if not next_page_token:
            break

    return video_ids

def get_random_video_info(channel_name):
    video_ids = get_video_ids_for_channel(channel_name)
    if video_ids:
        random_video_id = random.choice(video_ids)
        video_url = f"https://www.youtube.com/watch?v={random_video_id}"
        return random_video_id, video_url
    else:
        return None, None


def main():
    channel_name = input("Enter the name of the YouTube channel: ")
    random_video_id = get_random_video_info(channel_name)
    if random_video_id:
        print(f"Random video for '{channel_name}': {random_video_id}")
    else:
        print(f"No videos found for the channel '{channel_name}'.")

if __name__ == "__main__":
    main()
