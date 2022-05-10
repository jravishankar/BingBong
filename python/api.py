import flask
from flask import request, jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True

user_videos = {
	'BingBong':
		{
			'video_01': 'https://www.google.com/maps'
		},
	
	'jash': {
			'video_01': 'https://www.google.com'
			}
}

@app.route('/', methods=['GET'])
def home():
    return '''<h1>BingBong API</h1>
<p>You can be amazed or choose to look away.</p>'''


@app.route('/api/user_videos', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'user_id' in request.args:
        user_id = request.args['user_id']
    else:
        return "Error: No id field provided. Please specify an id."

    if 'video_id' in request.args:
        video_id = request.args['video_id']
    else:
        return "Error: No id field provided. Please specify an id."
    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    result = user_videos[user_id][video_id]
    results.append({'result_video': result})

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


app.run()