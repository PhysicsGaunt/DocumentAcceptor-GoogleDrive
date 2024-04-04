#written by gaunt

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import pickle
import sys

# The scopes determine what permissions you request from the user
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_credentials():
    """Log in to Google API and save the session for later use."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle') and len(sys.argv)==1:
        with open('token.pickle', 'rb') as token:
            creds, mail = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    else:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            mail = input("mailAdress: ")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump([creds, mail], token)
    return creds, mail

def main():
    creds, mail = get_credentials()

    # Build the Drive service
    drive_service = build('drive', 'v3', credentials=creds)

    # List files shared with you (this is just an example query)
    results = drive_service.files().list(orderBy= "sharedWithMeTime desc,modifiedTime desc",
      pageSize= 100, q="'me' in writers and not 'me' in owners", fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # Now, for each item, check the permissions to see if there's a pending ownership transfer
    for item in items:
        permissions = drive_service.permissions().list(fileId=item['id'], fields="permissions(id, emailAddress, role)").execute().get('permissions', [])
        #print(permissions)
        for permission in permissions:
            if permission['id']=='anyoneWithLink':
                continue
            elif permission['emailAddress'] != mail:
                continue
            else:
                try:
                    drive_service.permissions().update(fileId= item['id'],
                        permissionId= permission['id'],
                        transferOwnership= True,
                        body= {
                            'role': 'owner'
                        }
                        ).execute()
                    print("'"+item['name']+"' transfered.")
                    break
                except Exception:
                    print("'"+item['name']+"' could not be transfered.")
                    break

if __name__ == '__main__':
    main()
