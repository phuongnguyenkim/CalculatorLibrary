from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import googleapiclient
import sys

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.appdata',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata',
    'https://www.googleapis.com/auth/drive.photos.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
    ]

MIME_TYPE = {
    "docs": "application/vnd.google-apps.document",
    "sheets": "application/vnd.google-apps.spreadsheet",
    "slides": "application/vnd.google-apps.presentation",
    "forms": "application/vnd.google-apps.form",
    "folder": "application/vnd.google-apps.folder"
}

dict_FileCreate = {}
dict_FolderCreate = {}

def verify_FolderID(idFolder):
    if (len(idFolder) <= 33):
        try:
            _folderId = service.files().get(fileId=idFolder, fields='id').execute()
        except Exception:
            print("Fail to get Folder ID")
        else:
            listchild_FolderID(str(_folderId.get('id')))
    else:
        sys.exit("Wrong form Folder ID")

def listchild_FolderID(idFolder):
    key = 0
    resultsId = service.files().list(
        q="mimeType='application/vnd.google-apps.folder' and '{}' in parents".format(idFolder),
        fields="files(id, name, parents, mimeType)").execute()
    if resultsId:
        print(resultsId)
        list_temp = resultsId['files']
        while list_temp:
            for i in range(len(list_temp)):
                dict_temp = list_temp[i]
                dict_FolderCreate[key] = {"id": dict_temp['id'],
                                        "name": dict_temp['name'],
                                        "mimeType": dict_temp['mimeType'],
                                        "parents": dict_temp['parents']}
                print("Folder: {}".format(dict_FolderCreate[key]['name']))
                list_FileID(dict_FolderCreate[key]['id'])
                key += 1
                list_temp.remove(list_temp[0])

#Support Google offices extensions
def list_FileID(idFolder):
    key = 0
    resultsId = service.files().list(
        q="'{}' in parents \
        and (mimeType contains '/vnd.google-apps.document' \
        or mimeType contains '/vnd.google-apps.spreadsheet' \
        or mimeType contains '/vnd.google-apps.presentation' \
        or mimeType contains '/vnd.google-apps.form')".format(idFolder),
        pageSize=10,
        fields="files(id, name, mimeType, parents)").execute()
    if resultsId:
        list_temp = resultsId['files']
        for i in range(len(list_temp)):
            dict_temp = list_temp[i]
            dict_FileCreate[key] = {"id": dict_temp['id'],
                                    "name": dict_temp['name'],
                                    "mimeType": dict_temp['mimeType'],
                                    "parents": dict_temp['parents']}
            print("Name: {}".format(dict_FileCreate[key]['name']))
            key += 1
            
if __name__ == "__main__":
    try:
        id = '1k872-nrq8jjICyGyYTNeWbhHBBFaU6Yn'
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('drive', 'v3', http=creds.authorize(Http()))
    except Exception:
        sys.exit("Please check credentials file again")
       
verify_FolderID(id)
    
