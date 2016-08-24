# import libraries
from flask import Flask, request, jsonify, render_template
import urllib
import base64
import json
import requests

# set flask application
app = Flask(__name__)


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
                'type': 'LABEL_DETECTION',
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
def hello():
    return render_template('sample.html')


@app.route('/api/classify', methods=['POST'])
def classify():
    # get request parameter
    request_json = request.json

    if ('jpg' in request_json):
        # convert request data
        image_content = request_json['jpg'].replace('data:image/jpeg;base64,', '')

        # api request
        response = google_cloud_vision(image_content)

        # api response
        return jsonify(response)

    return 'Bad request!'


# run main function
if __name__ == '__main__':
    # run flask application
    app.run()
