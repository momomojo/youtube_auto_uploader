import sys
sys.path.append('C:\\Users\\Momo Mojo\\PycharmProjects\\pythonProject5\\TikTokUploder')  # replace with the actual path to the TikTokUploder directory
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from TikTokUploder.uploader import uploadVideo

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def fetch_data_from_google_sheets():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId='14RA6O9-C--gAxM5eQebCo8s9SMRiLqyn_oOXIAARSoQ',
                                range='zap input!A2:E11').execute()
    values = result.get('values', [])
    return values

def post_to_tiktok(unique_id, description, title, schedule, tags):
    # Use TikTok API to post video
    video_file = f"C:/Users/Momo Mojo/Desktop/youtube shorts/EmpoweringSage/{unique_id}.mp4"

    # Combine the title and tags
    full_title = f"{title}\n{tags}"

    # Your TikTok sessionid cookie
    session_id = "32707f2a4bbda9795f9150ff8abaae1e"  # replace with your TikTok sessionid cookie

    # Publish the video
    uploadVideo(session_id, video_file, full_title, tags.split(), [])

    print(f"Posted video with unique_id {unique_id} to TikTok")

def main():
    # Fetch data from Google Sheets
    data = fetch_data_from_google_sheets()

    # Only process the first row of data
    if data:
        unique_id, description, title, schedule, tags = data[0]
        post_to_tiktok(unique_id, description, title, schedule, tags)
    else:
        print("No data found in the Google Sheets document.")

if __name__ == "__main__":
    main()
