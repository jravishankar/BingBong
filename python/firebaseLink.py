import pyrebase

## Initialization

firebaseConfig = {
  "apiKey": "AIzaSyDsuqIErWhkKb3gPa1RkAITyaVmaIF1XeQ",
  "authDomain": "bingbong-7edf4.firebaseapp.com",
  "databaseURL": "",
  "projectId": "bingbong-7edf4",
  "storageBucket": "bingbong-7edf4.appspot.com",
  "serviceAccount": "./bingbong_firebase_key.json"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
all_files = storage.list_files()

for file in all_files:
	file.download_to_filename(file.name.split('/')[-1])