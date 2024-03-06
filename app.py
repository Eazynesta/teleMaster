import sys
from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterVideo

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
def main():
    choice = display_menu()

    if choice == '1':
        download_videos()
    elif choice == '2':
        post_videos()
    elif choice == '3':
        forward_messages()
    else:
        print("Invalid choice. Please choose 1, 2, or 3.")
        return

# Function to handle the download functionality
def download_videos():
    source_channel = input("Enter source channel: ")
    num_videos = int(input("Enter number of videos: "))
    # Implement download functionality
    client.start()

    try:
        with client:
            channel_entity = client.get_entity(source_channel)
            messages = client.get_messages(channel_entity, limit=num_videos, filter=InputMessagesFilterVideo())
            
            for message in messages:
                if message.media and hasattr(message.media, 'video'):
                    video_file = message.download_media()
                    print(f"Video downloaded: {video_file}")
    
    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.disconnect()

# Function to handle the post functionality
def post_videos():
    target_channel = input("Enter target channel: ")
    num_videos = int(input("Enter number of videos: "))
    # Implement post functionality

# Function to handle the forward functionality
def forward_messages():
    target_channel = input("Enter target channel: ")
    num_messages = int(input("Enter number of messages to forward: "))
    # Implement forward functionality

# Run the main function
if __name__ == "__main__":
    main()