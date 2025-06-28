# Code written by SayyadN
# Date: 2025-6-28
# Purpose: Download YouTube videos using Python
# Version: 2.0
# Code Starts here

# Importing the required libraries
from pytube import YouTube , Playlist
import os
import yt_dlp

# Function to download the video
def download_video():
    video_url = input("Enter Your YouTube Video URL: ").strip()
    vid_save_path = input("Enter Your Path to Save the Video: ").strip()

    if not video_url and not vid_save_path:
        print("Error: Please enter both the URL and the save path.")
        return

    if not os.path.exists(vid_save_path):
        try:
            os.makedirs(vid_save_path)
            print(f"Created directory: {vid_save_path}")
        except Exception as e:
            print(f"Error: Could not create directory. {e}")
            return

    try:
        yt = YouTube(video_url)

        # Display title and options
        print(f"Video Title: {yt.title}")
        print("""
1. High Resolution
2. Low Resolution
""")
        try:
            resolution_choice = int(input("Enter your choice number: ").strip())
        except ValueError:
            print("Error: Invalid input. Please enter a number.")
            return

        if resolution_choice == 1:
            video = yt.streams.get_highest_resolution()
        elif resolution_choice == 2:
            video = yt.streams.get_lowest_resolution()
        else:
            print("Error: Invalid option selected. Please choose 1 or 2.")
            return

        print(f"Downloading '{yt.title}'...")
        video.download(vid_save_path)
        print(f"Success: Video '{yt.title}' downloaded successfully at '{vid_save_path}'.")
    except Exception as e:
        print(f"Error: An error occurred while downloading the video.\nDetails: {str(e)}")


# Function to download a YouTube playlist
def download_yt_playlist():
    plst_path = input("Enter Your Playlist Save Path: ").strip()
    if not os.path.exists(plst_path):
        try:
            os.makedirs(plst_path)
            print(f"Created directory: {plst_path}")
        except Exception as e:
            print(f"Error: Could not create directory. {e}")
            return

    playlist_url = input("Enter Your Playlist URL: ").strip()
    try:
        play_list_yt = Playlist(playlist_url)
        video_urls = play_list_yt.video_urls
    except Exception as e:
        print(f"Error: Failed to fetch playlist. {e}")
        return

    print(f"{len(video_urls)} videos in this playlist.")

    res_input = input("Would you download the playlist in High (H) or Low (L) resolution? ").lower().strip()
    if res_input not in ['h', 'l']:
        print("Error: Invalid resolution choice.")
        return

    for url in video_urls:
        try:
            yt = YouTube(url)
            print(f"Downloading Video: {yt.title}")
            if res_input == 'h':
                stream = yt.streams.get_highest_resolution()
            else:
                stream = yt.streams.get_lowest_resolution()
            
            stream.download(plst_path)
            print(f"Downloaded: {yt.title}")
        except Exception as e:
            print(f"Connection error or download failed for video: {url}. Error: {e}")

def download_facebook_tiktok_insta_x():
    url = input("Enter Your  Video URL: ")
    save_fc_vid = input("Please Enter Path ")

    if not url and not save_fc_vid:
        print("Error: Please enter both the URL and the save path.")
        return

    if not os.path.exists(save_fc_vid):
        try:
            os.makedirs(save_fc_vid)
            print(f"Created directory: {save_fc_vid}")
        except Exception as e:
            print(f"Error: Could not create directory. {e}")
            return

    res_input = input("Would you download the Video in High (H) or Low (L) resolution? ").lower().strip()
    if res_input not in ['h', 'l']:
        print("Error: Invalid resolution choice.")
        return    
    if res_input == "h":
            ydl_opts = {
        'outtmpl': f'{save_fc_vid}/%(title)s.%(ext)s',
        'format': 'best',  
        }
    else:
            ydl_opts = {
        'outtmpl': f'{save_fc_vid}/%(title)s.%(ext)s',
        'format': 'worst',  
        }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed successfully.")
    except Exception as e:
        print(f"Error: Failed to download the video. Details: {e}")

def main():
    print("===== Ndwon By SayyadN=====")
    print("""
    1.Download YT Videos 
    2.Download YT. PlayList
    3. Download Facebook / Tiktok / X / Instagram
    """)

    user_o = input("Enter Your Opion :")
    if user_o == 1:
        download_video()
    elif user_o == 2:
        download_yt_playlist()
    elif user_o == 3:
        download_facebook_tiktok_insta_x()
    else:
        print("Invaild Input")
    

main()
