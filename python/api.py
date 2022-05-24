import flask
from flask import request, jsonify
from firebaseLink import FirebaseLink
from embedder import FullBodyPoseEmbedder
from bingbongcore import PoseDifferenceEstimator
from videoToCsv import generate_csv_and_anns

app = flask.Flask(__name__)
app.config["DEBUG"] = True
linker = FirebaseLink()
currDir = os.path.dirname(os.path.realpath(__file__))
proVideoDir = os.path.join(currDir, 'proVideos')
userVideoDir = os.path.join(currDir, 'userVideos')


@app.route('/', methods=['GET'])
def home():
    return '''<h1>BingBong API</h1>
<p>You can be amazed or choose to look away.</p>'''


@app.route('/api/', methods=['GET'])
def main():
    """
    For API request, need user_id + video_id (storage/userFiles/user_id/video_id), and technique_id (storage/proVideos/technique_id/technique_id.csv)

    1. Download corresponding user video
    2. Retrieve pro data (from csv, we have both local and firebase copies, just do local for now)
    3. Process user video into landmark data and align frames with pro data based on distance measure
    4. Do pose difference estimation
    5. Send relevant data back to firebase under user folder 
    6. Return relevant Firebase location so that Flutter app can send a request the data from Firebase

    """

    ## Get user and video id to find corresponding video in database
    if 'user_id' in request.args:
       user_id = request.args['user_id']
    else:
       return "Error: No user id field provided. Please specify a user id."

    if 'video_id' in request.args:
      video_id = request.args['video_id']
    else:
       return "Error: No video id field provided. Please specify a video id."

    ## Get technique id to find corresponding csv file (assume preprocessed) in database
    if 'technique_id' in request.args:
      video_id = request.args['technique_id']
    else:
       return "Error: No technique id field provided. Please specify a technique id."


    # all_files = linker.get_all_files()
    # for file in all_files:
    # 	print(file.name)

    ## Download specific video from Firebase
    firebase_user_video_src = 'userFiles/{}/{}'.format(user_id, video_id + '.mp4')
    local_user_video_dir = os.path.join(userVideoDir, user_id, video_id)
    os.makedirs(local_user_video_dir, exist_ok=False)
    local_user_video_dest = os.path.join(local_user_video_dir, video_id + '.mp4')
    linker.download_file(firebase_user_video_src, local_user_video_dest)

    ## Preprocess user data
    user_landmarks_array = generate_csv_and_anns('user', local_user_video_dest)

    ## Access to pro data (doing locally for now, eventually can consider a fully firebase solution)
    pro_data_csv_path = os.path.join(proVideoDir, technique_id, technique_id + '.csv')

    ## Processing
    pose_embedder = FullBodyPoseEmbedder()
    difference_estimator = PoseDifferenceEstimator(embedder, pro_data_csv_path)
    difference_estimator(user_landmarks_array) #this calls our estimator object on user data, does the actual core processing for BingBong



    ## Post processing (i.e. what do we want to send back to the user)
    # difference_estimator.scores is good for now? can just write this as a number to a text file for initial testing purposes

    firebase_upload_dest = 'userFiles/{}/{}'.format(user_id, video_id + '_response.mp4') # this should eventually be a .mp4 file for user to see, more illustrative of errors
    


    results = [{'dest':firebase_upload_dest}] # specifies the pickup point for Flutter
    return jsonify(results)


app.run()