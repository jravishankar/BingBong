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
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.


    ## Get user and video id to find corresponding video in database
    if 'user_id' in request.args:
       user_id = request.args['user_id']
    else:
       return "Error: No id field provided. Please specify an id."

   if 'video_id' in request.args:
      video_id = request.args['video_id']
   else:
       return "Error: No id field provided. Please specify an id."

    ## Download specific video from Firebase

    all_files = linker.get_all_files()
    for file in all_files:
    	print(file.name)


    ## 

    results = [{}]
    return jsonify(results)


app.run()