import streamlit as st
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=st.secrets["YOUTUBE_API_KEY"])


def channel_searcher(channel_name: str) -> dict:
    # Search channel
    try:
        search_channel = youtube.search().list(q=channel_name, type="channel", part="snippet", maxResults=1).execute()
    except IndexError:
        st.warning("Channel not found")
        return {}
    if search_channel.get("items"):
        channel_id = search_channel["items"][0]['id']['channelId']
        response = youtube.channels().list(id=channel_id, part="contentDetails,statistics").execute()
    else:
        st.warning("Channel not found")
        return {}
    return response


def high_viral_min_views(n_subs: str) -> int:
    n_subs = int(n_subs)
    if n_subs <= 1000:
        return 10000
    elif n_subs <= 5000:
        return 20000
    elif n_subs <= 50000:
        return 50000
    elif n_subs <= 500000:
        return 1000000
    elif n_subs <= 5000000:
        return 2000000
    else:
        return 5000000


def short_high_viral_min_views(n_subs: str) -> int:
    n_subs = int(n_subs)
    if n_subs <= 1000:
        return 50000
    elif n_subs <= 5000:
        return 100000
    elif n_subs <= 50000:
        return 500000
    elif n_subs <= 500000:
        return 1000000
    elif n_subs <= 5000000:
        return 5000000
    else:
        return 10000000


def continue_to_search(videos_list: list[dict], min_viral_views: int, videos_limit: int) -> bool:
    if len(videos_list) > videos_limit:
        for i in range(-1, -50, -1):
            if int(videos_list[i]["statistics"]["viewCount"]) >= min_viral_views:
                videos_limit += 500
                return True
        return False
    return True


def channel_viral_videos(playlist_id: str, min_viral_views: int):
    videos_list = []
    next_page_token = None
    limit = 1000
    while True:
        # Obtaining 50 videos of the channel
        all_videos = youtube.playlistItems().list(playlistId=playlist_id, part="contentDetails", maxResults=50,
                                                  pageToken=next_page_token).execute()
        # String of the 50 videos id
        ids_string = ",".join(item["contentDetails"]["videoId"] for item in all_videos["items"])
        # If there is no id, end the search
        if not ids_string:
            break
        # For each id search the snippet, statistics and the contentDetails
        popular_videos = youtube.videos().list(id=ids_string, part="snippet,statistics,contentDetails").execute()
        # Adding the item part into the list
        videos_list.extend(popular_videos.get("items", []))

        # If already check 1000 videos and there is no viral video in the last 50 we end the search
        if not continue_to_search(videos_list, min_viral_views, limit):
            print("No more viral videos")
            break

        next_page_token = all_videos.get("nextPageToken")

        # if not more videos stop
        if not next_page_token:
            print("No next token")
            break
    st.write("processed videos:")
    st.write(len(videos_list))
    # Sort the videos in order to process only the most viral ones
    return sorted(videos_list, key=lambda video: int(video.get('statistics', {}).get('viewCount', '0')), reverse=True)


def most_view_videos(channel_name: str) -> (str, list[dict]):
    st.write(f"Searching channel: **{channel_name}** ...")
    # obtain the statistic info of a chanel name/query
    search_channel = channel_searcher(channel_name)
    if not search_channel:
        return {}
    # channel_id = search_channel["items"][0]["id"]  # obtaining only the channelId
    upload_playlist_id = search_channel["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    channel_subs = search_channel["items"][0]["statistics"]["subscriberCount"]
    # Calculate the min views for video
    min_views = high_viral_min_views(channel_subs)

    return channel_subs, channel_viral_videos(upload_playlist_id, min_views)


def videos_info(videos: (str, list[dict]), video_info: list[list]):  # -> list[list]:
    st.write("Extracting data...")
    # Lists to add in a dictionary
    # sheets = []
    count = 0
    # Scroll through the dictionary videos.list
    for video in videos[1]:
        duration = pt_to_seconds(video["contentDetails"]["duration"])
        if duration == -1:
            continue
        category = video_type(duration)
        video_views = int(video["statistics"]["viewCount"])
        video_min_viral_views = high_viral_min_views(videos[0])
        if video_views < video_min_viral_views:
            break
        if category == "SHORT":
            min_viral_views = short_high_viral_min_views(videos[0])
            if video_views < min_viral_views:
                continue
        row = [
            video["snippet"]["title"],
            video["snippet"]["channelTitle"],
            video_views,
            video["statistics"].get('likeCount', '-1'),
            category,
            f"https://www.youtube.com/watch?v={video['id']}"
        ]
        # sheets.append(row)
        video_info.append(row)
        count += 1
    # Returning a bidimensional list with the lists made
    st.write(f"Extracting data of {count} videos")
    print("todo bien con el video info")
    # return sheets


def pt_to_seconds(pt: str) -> int:
    seconds = 0
    add = 0
    for character in pt[2:]:
        if character == "H":
            seconds += add * (60 ** 2)
            add = 0
        elif character == "M":
            seconds += add * 60
            add = 0
        elif character == "S":
            seconds += add
            add = 0
        else:
            add *= 10
            try:
                add += int(character)
            except ValueError:
                return -1
    return seconds


def video_type(duration: int) -> str:
    if duration <= 61:
        return "SHORT"
    else:
        return "VIDEO"


# In case I need something less precise but less expensive in YouTube tokens
def channel_viral_videos2(channel_id: str, min_viral_views: int) -> list[dict]:
    videos_chunk_list = []
    next_page_token = None
    results_number = 0
    while True:
        # Obtaining the most popular videos of the channel
        popular_videos = youtube.search().list(channelId=channel_id, part="snippet", maxResults=50, order="viewCount",
                                               type="video", pageToken=next_page_token).execute()
        results_number += 50
        # Obtaining the videos id for the info
        ids_string = ",".join(item["id"]["videoId"] for item in popular_videos["items"])
        # Video information dictionary
        popular_videos_info = youtube.videos().list(id=ids_string, part="snippet,statistics,contentDetails").execute()
        # List of dictionaries
        videos_chunk_list.append(popular_videos_info)

        # Get the next page token
        next_page_token = popular_videos.get("nextPageToken")
        # Views data of the las dictionary item
        last_video_views = popular_videos_info["items"][-1]["statistics"]["viewCount"]
        last_video_views = int(last_video_views)
        # conditions to stop
        if results_number == 500:
            print("500")
            break
        if not next_page_token:
            print("No hubo next token")
            break
        if last_video_views < min_viral_views:
            print("Se break por minimo de vistas")
            break
    return videos_chunk_list
