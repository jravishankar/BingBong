import flask
from flask import request, jsonify
from firebaseLink import FirebaseLink

app = flask.Flask(__name__)
app.config["DEBUG"] = True
linker = FirebaseLink()



@app.route('/', methods=['GET'])
def home():
    return '''<h1>BingBong API</h1>
<p>You can be amazed or choose to look away.</p>'''


@app.route('/api/', methods=['GET'])
def main():
    """
    For API request, need user_id + video_id (storage/userFiles/user_id/video_id), and technique_id (storage/proVideos/technique_id/technique_id.mp4)

    1. Download corresponding user video
    2. Retrieve pro data (from csv)
    3. Process user video into landmark data and align frames with pro data based on distance measure
    4. Do pose difference estimation
    5. Send relevant data back to firebase under user folder 
    6. Return relevant Firebase location so that Flutter app can send a request the data from Firebase

    """



    ## Get user and video id to find corresponding video in database
    if 'user_id' in request.args:
       user_id = request.args['user_id']
    else:
       return "Error: No id field provided. Please specify an id."

    if 'video_id' in request.args:
      video_id = request.args['video_id']
    else:
       return "Error: No id field provided. Please specify an id."

   #if 'pro_id'

    ## Download specific video from Firebase

    all_files = linker.get_all_files()
    for file in all_files:
    	print(file.name)


    ## 

    results = [{}]
    return jsonify(results)


app.run()