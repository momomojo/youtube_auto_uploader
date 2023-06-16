from instagram_api import InstagramAPI  # This would be the Instagram API library
from google_api import fetch_data_from_google_sheets

def post_to_instagram(unique_id, description, title, schedule, tags):
    # Use Instagram API to post video
    video_file = f"C:/Users/Momo Mojo/Desktop/youtube shorts/EmpoweringSage/{unique_id}.mp4"
    # This is a two-step process: creating a container and then publishing it
    container_id = InstagramAPI.create_container(video_file, title, description, tags)
    InstagramAPI.publish_container(container_id)

def main():
    # Fetch data from Google Sheets
    data = fetch_data_from_google_sheets()

    for row in data:
        unique_id, description, title, schedule, tags = row
        post_to_instagram(unique_id, description, title, schedule, tags)

if __name__ == "__main__":
    main()
