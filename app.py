import sys
import os
from telethon.sync import TelegramClient
from tqdm import tqdm
from telethon.tl.types import InputMessagesFilterVideo
from telethon.tl.types import InputPeerChannel
import asyncio
import re

# Your Telegram API credentials
api_id = ''
api_hash = ''

# Initialize the Telegram client
client = TelegramClient('teleMasterSession', api_id, api_hash)


# Function to display menu and get user choice
def display_menu():
    print("Choose an action:")
    print("1. DOWNLOAD")
    print("2. POST")
    print("3. FORWARD")

    choice = input("Enter your choice (1/2/3): ")
    return choice

# Main function to handle CLI interface
async def main():
    choice = display_menu()

    if choice == '1':
        await download_videos()
    elif choice == '2':
        await post_videos()
    elif choice == '3':
        await forward_messages()
    else:
        print("Invalid choice. Please choose 1, 2, or 3.")
        return

# Function to handle the download functionality
async def download_videos():
    source_channel = input("Enter source channel: ")
    num_videos = int(input("Enter number of videos: "))
    await client.start()

    try:
        async with client:
            channel_entity = await client.get_entity(source_channel)
            messages = await client.get_messages(channel_entity, limit=num_videos, filter=InputMessagesFilterVideo())

            for message in tqdm(messages, desc="Downloading videos", total=num_videos):
                if message.media and hasattr(message.media, 'video'):
                    # Define the progress callback function within the loop to ensure the progress bar is unique for each file
                    def progress_callback(current, total):
                        # This updates the progress bar for each chunk
                        tqdm.write(f'Downloading {current} out of {total} bytes: {current / total:.1%}', end='\r')

                    # Pass the progress_callback function to download_media
                    video_file = await message.download_media(progress_callback=progress_callback)
                    print(f"\nVideo downloaded: {video_file}")  # Newline for cleaner output after download

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.disconnect()

# Function to handle the post functionality
    # Implement post functionality
async def post_videos():
    target_channel_input = input("Enter target channel username or ID: ").strip()

    # Extract username from URL or direct input
    match = re.search(r"(?:https?://)?t.me/([\w\d_]+)", target_channel_input)
    if match:
        target_channel = '@' + match.group(1)  # Append '@' if extracted from URL
    else:
        target_channel = target_channel_input  # Use direct input

    folder_path = input('Enter the folder path containing videos: ').strip().strip('"')  # Remove extra quotes

    await client.start()

    try:
        async with client:
            channel = await client.get_entity(target_channel)

            video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
            if not video_files:
                print("No video files found in the specified folder.")
                return

            for video in video_files:
                video_path = os.path.join(folder_path, video)
                print(f"Posting video: {video}")
                await client.send_file(channel, video_path)
                print(f"Video posted: {video}")

    except Exception as e:
        print(f"Error: {e}")

# Function to handle the forward functionality
async def forward_messages():
    source_channel = input("Enter the source channel (username or ID): ")
    target_channel = input("Enter the target channel (username or ID): ")
    num_messages = int(input("Enter the number of messages to forward: "))

    await client.start()

    try:
        # Getting entity for the source channel
        source_entity = await client.get_entity(source_channel)
        
        # Getting entity for the target channel
        target_entity = await client.get_entity(target_channel)

        # Fetching messages from the source channel
        messages = await client.get_messages(source_entity, limit=num_messages)

        # Forwarding messages to the target channel
        for message in messages:
            await client.forward_messages(entity=target_entity, messages=message)
            print(f"Forwarded message ID {message.id} to {target_channel}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await client.disconnect()


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())