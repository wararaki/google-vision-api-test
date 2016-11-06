'''
Google Vision API Test Application
'''
import base64
import json

import requests
from flask import Flask, render_template, request
#from PIL import Image, ImageDraw

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
def google_cloud_vision(image_content, check_option_list):
    '''
    Google Vision API request module
    '''
    # set request url
    api_url = API_URL + API_KEY

    # create request features type
    features = []
    for check_option in check_option_list:
        print("{0}".format(check_option))
        features.append({'type': check_option, 'maxResults': 10})

    # set request parameter
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_content
            },
            'features': features
        }]
    })

    # api request
    response = requests.post(api_url, data=req_body)

    # return response parameter
    return response.json()


# routing
@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    index module
    '''

    # validate request method type
    # [GET] method event
    if request.method == "GET":
        # rendering index page
        return render_template('index.html', items=analysis_list)

    # [POST] method event
    else:
        # get image file from form
        image_data = request.files['image']

        # get checked option list
        check_option_list = request.form.getlist('options')

        # To Do: change javascript checker
        if len(check_option_list) == 0:
            return render_template("result.html", error="error not check items")

        # convert binary to base64(utf-8) data
        image_base64 = base64.b64encode(image_data.read()).decode("utf-8")

        # call google vision api
        response_data = google_cloud_vision(image_base64, check_option_list)

        print(response_data)

        # output result page
        #if response_data["responses"][0]:
        return render_template("result.html", response="success")
        #else:
            #return render_template("result.html", error="error message")

# run main function
if __name__ == '__main__':
    # run flask application
    app.run()
