from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/youtube.upload']

def main():
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

    youtube = build('youtube', 'v3', credentials=creds)

    if not values:
        print('No data found.')
    else:
        for row in values:
            unique_id, description, title, schedule, tags = row

            request = youtube.videos().insert(
                part="snippet,status",
                body={
                  "snippet": {
                    "categoryId": "22",
                    "description": description,
                    "title": title,
                    "tags": tags.split(",")  # Assuming the tags are comma-separated
                  },
                  "status": {
                    "privacyStatus": "private",
                    "publishAt": schedule,
                    "madeForKids": False
                  }
                },
                media_body=MediaFileUpload(fr"C:\Users\Momo Mojo\Desktop\youtube shorts\EmpoweringSage\{unique_id}.mp4")  # Assuming the video file name is the same as the unique ID
            )
            response = request.execute()

            print(response)

if __name__ == '__main__':
    main()