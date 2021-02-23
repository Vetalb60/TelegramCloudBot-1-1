#
#   GoogleDrive.py
#
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from Variables import *
import urllib.request
import datetime

SCOPES = [SCOPE_]
SERVICE_ACCOUNT_FILE = serviceKey_

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes = SCOPES)
service = build('drive', 'v3', credentials = credentials)

def createFolder():
    name = str(datetime.date.today())
    folder_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [folder_id_]
    }
    return service.files().create(body=folder_metadata,fields='id').execute()['id']


def uploadFile(file_info,name,type):
    results = service.files().list(pageSize = 10,fields = "nextPageToken, files(id, name)").execute()
    global new_folder
    for i in range(len(results['files'])):
        if str(results['files'][i]['name']) == str(datetime.date.today()):
            new_folder = str(results['files'][i]['id'])
            break;
        else:
            if i == len(results):
                new_folder = createFolder()
                break;

    file_metadata = {
        'name': name,
        'parents': [new_folder]
    }
    urllib.request.urlretrieve(file_path_ + file_info.file_path, str(name))
    media = MediaFileUpload(str(name))
    if service.files().create(body=file_metadata, media_body=media, fields='id').execute():
        return successMessage_
    else:
        return faliMessage_