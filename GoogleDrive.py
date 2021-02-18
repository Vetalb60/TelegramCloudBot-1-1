from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from Variables import *
import pprint
import io
import datetime
import urllib.request

SCOPES = [SCOPE_]
SERVICE_ACCOUNT_FILE = serviceKey_

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes = SCOPES)
service = build('drive', 'v3', credentials = credentials)

def createFolder():
    name = str(datetime.date.today())
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [folder_id]
    }
    return service.files().create(body=file_metadata,fields='id').execute()['id']

def uploadFile(file_info,name):
    results = service.files().list(pageSize=10,
                                   fields="nextPageToken,"
                                          "files(id, name, mimeType, parents, createdTime)",
                                   q="mimeType contains 'application/vnd.google-apps.folder'").execute()
    for i in range(len(results['files'])):
        if str(results['files'][i]['name']) == str(datetime.date.today()):
            break;
        else:
            global new_folder
            new_folder = createFolder()
    file_metadata = {
        'name': name,
        'parents': [new_folder]
    }
    logo = urllib.request.urlopen(file_path_ + file_info.file_path).read()
    f = open(name, 'wb')
    f.write(logo)
    f.close()
    media = MediaFileUpload(name)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()