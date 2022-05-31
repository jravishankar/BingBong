import pyrebase, os

## Initialization


# A Sample class with init method
class FirebaseLink:
   
    # init method or constructor 
    def __init__(self):
        config = {
            "apiKey": "AIzaSyDsuqIErWhkKb3gPa1RkAITyaVmaIF1XeQ",
            "authDomain": "bingbong-7edf4.firebaseapp.com",
            "databaseURL": "",
            "projectId": "bingbong-7edf4",
            "storageBucket": "bingbong-7edf4.appspot.com",
            "serviceAccount": "./bingbong_firebase_key.json"
        }
        firebase = pyrebase.initialize_app(config)
        print(firebase.credentials)
        self.storage = firebase.storage()
        self.db = firebase.database()

    def get_all_files(self):
        return self.storage.list_files()

    def put_file(self, localPath, firebasePath):
        self.storage.child(firebasePath).put(localPath)

    def download_file(self, localPath, firebasePath):
        self.storage.child(firebasePath).download(firebasePath, localPath)
        #self.storage.child(firebasePath).download(localPath)