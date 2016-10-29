# import libraries
from flask import Flask, request, jsonify, render_template
import urllib
import base64
import json
import requests
from PIL import Image
from PIL import ImageDraw

# set flask application
app = Flask(__name__)


# define key type
analysis_list = [
    'TYPE_UNSPECIFIED',
    'FACE_DETECTION',
    'LANDMARK_DETECTION',
    'LOGO_DETECTION',
    'LABEL_DETECTION',
    'TEXT_DETECTION',
    'SAFE_SEARCH_DETECTION',
    'IMAGE_PROPERTIES'
]


# read api key
API_KEY = ''
with open('../passwords/google_vision_api.txt') as f:
    API_KEY = f.readline()


# define api url
API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='


# google api request function
def google_cloud_vision(image_content):
    # set request url
    api_url = API_URL + API_KEY

    # set request parameter
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_content
            },
            'features': [{
                'type': 'FACE_DETECTION',
                'maxResults': 10,
            }]
        }]
    })

    # api request
    response = requests.post(api_url, data=req_body)

    # return response parameter
    return response.json()


# routing
@app.route('/')
def index():
    # validate request method type
    if request.method == "GET":
        # rendering index page
        return render_template('index.html', items=analysis_list)
    else: # method == "POST"
        # get image file from form
        image_data = request.files['image']

        # convert binary to base64 data
        image_base64 = base64.b64encode(data,getValue())

        # call google vision api
        response_data = google_cloud_vision(image_base64)

        # output result page
        if res["responses"][0]:
            return render_template("result.html")
        else:
            return render_template("result.html")


# @app.route('/api/classify', methods=['POST'])
# def classify():
#     # get request parameter
#     request_json = request.json

#     # set image list container
#     results = []

#     if request.method == 'POST' and ('image' in request_json):
#         # convert request data
#         image_content = request_json['image'].replace('data:image/jpeg;base64,', '')

#         # api request
#         response = google_cloud_vision(image_content)

#         # create response data
#         results = jsonify(response)

#     # return render template
#     return results

# run main function
if __name__ == '__main__':
    # run flask application
    app.run()
