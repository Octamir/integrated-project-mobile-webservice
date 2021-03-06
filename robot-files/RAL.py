##!flask/bin/python
import sys
sys.path.append("/usr/lib/pynaoqi")
from datetime import timedelta
from flask import Flask, abort, jsonify, request, make_response, current_app
import naoqi
from random import randint
import json
from functools import update_wrapper
from naoqi import ALProxy

app = Flask(__name__)

nao_host = "127.0.0.1"
webserverIp = "0.0.0.0"
nao_port = 9559
battery = 100
chargeStatus = True
randNum = 0

#logger = logger.Logger(4) # Initialize logger with level "debug"

#CROSSDOMAIN SHIZZLE

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

#INDEX
@app.route('/')
@crossdomain(origin='*')
def index():
    return "Hello Robotic World!"

#IP
def getIP():
    return nao_host

@app.route('/getIP', methods=['GET'])
@crossdomain(origin='*')
def getIP_HTTP():
    return jsonify({'IP': getIP()}), 200

#TYPE
def getType():
    """
    if randNum == 0:
        return "PEPPER"
    elif randNum == 1:
        return "NAO"
    elif randNum == 2:
        return "BUDDY"
    else:
        return "JIBO"
    """

    return 'NAO'

@app.route('/getType', methods=['GET'])
@crossdomain(origin='*')
def getType_HTTP():
    return jsonify({'type':getType()}), 200

#NAME
def getName():
    """
    if randNum == 0:
        return "Mister Pepperoni"
    elif randNum == 1:
        return "Mister I_want_it_Nao"
    elif randNum == 2:
        return "Mister Buttbuddy"
    else:
        return "Mister Hibo_jibo"
    """

    return 'Mister Nao'

@app.route('/getName', methods=['GET'])
@crossdomain(origin='*')
def getName_HTTP():
    return jsonify({'name':getName()}), 200

#CHARGE
def charging():
    chargeStatus = True
    return "charging"

@app.route('/charge', methods=['GET'])
@crossdomain(origin='*')
def charging_HTTP():
    return jsonify({'chargeStatus':charging()}), 200

#UNPLUG
def unplug():
    chargeStatus = False
    return "unplugged"

@app.route('/unplug', methods=['GET'])
@crossdomain(origin='*')
def unplug_HTTP():
    return jsonify({'chargeStatus':unplug()}), 200

#BATTERY LEVEL
def getBatteryLevel():
    batt_json = json.dumps(battery)
    return batt_json

@app.route('/getBatteryLevel', methods=['GET'])
@crossdomain(origin='*')
def getBatteryLevel_HTTP():
    return jsonify({'batteryLevel':getBatteryLevel()}), 200

#GET ACTIONS
def getActions():
    return [
            { 'route': 'actions/StandInit', 'displayName': 'Stand Init', 'type': 'standing' },
            { 'route': 'actions/StandZero', 'displayName': 'Stand Zero', 'type': 'standing' },
            { 'route': 'actions/Stand', 'displayName': 'Stand', 'type': 'standing' },

            { 'route': 'actions/SitRelax', 'displayName': 'Sit Relax', 'type': 'sitting' },
            { 'route': 'actions/Crouch', 'displayName': 'Crouch', 'type': 'sitting' },
            { 'route': 'actions/Sit', 'displayName': 'Sit', 'type': 'sitting' },

            { 'route': 'actions/LyingBelly', 'displayName': 'Lie on belly', 'type': 'lying' },
            { 'route': 'actions/LyingBack', 'displayName': 'Lie on back', 'type': 'lying' },

            { 'route': 'move/hand/open/LHand', 'displayName': 'Open left hand', 'type': 'hand gesture' },
            { 'route': 'move/hand/open/RHand', 'displayName': 'Open right hand', 'type': 'hand gesture' },
            { 'route': 'move/hand/close/LHand', 'displayName': 'Close left hand', 'type': 'hand gesture' },
            { 'route': 'move/hand/close/RHand', 'displayName': 'Close right hand', 'type': 'hand gesture' },
           ]

@app.route('/getActions', methods=['GET'])
@crossdomain(origin='*')
def getActions_HTTP():
    # Flask doesn't allow jsonify with lists
    return json.dumps(getActions()), 200

#DO ACTION
def doAction(actionName):
    postureProxy = ALProxy("ALRobotPosture", nao_host, nao_port)
    postureProxy.goToPosture(str(actionName), 1.0)
    return postureProxy.getPostureFamily()

@app.route('/actions/<string:actionName>', methods=['GET'])
@crossdomain(origin='*')
def doAction_HTTP(actionName):
    return jsonify({'posture':doAction(actionName)}), 200

#ASK
def ask(text):
    tts = ALProxy("ALTextToSpeech", nao_host, nao_port)
    tts.say(str(text))
    return text

@app.route('/ask/<string:text>', methods=['GET'])
@crossdomain(origin='*')
def ask_HTTP(text):
    return jsonify({'text': ask(text)}), 200

#MOVE
#http://doc.aldebaran.com/2-1/_downloads/almotion_moveTo1.py
def move(x,y,d):
    motionProxy = ALProxy("ALMotion", nao_host, nao_port)
    motionProxy.wakeUp()
    xCoo = float(x)
    yCoo = float(y)
    theta = float(d)
    motionProxy.moveTo(xCoo, yCoo, theta)
    return [x,y,d]

@app.route('/move/<int:x>/<int:y>/<int:d>', methods=['GET'])
@crossdomain(origin='*')
def move_HTTP(x,y,d):
    return jsonify({'coordinates': move(x,y,d)}), 200

def openHand(hand):
    motionProxy = ALProxy("ALMotion", nao_host, nao_port)
    if(hand == "LHand"):
        motionProxy.openHand("LHand")
    else:
        motionProxy.openHand("RHand")
    return hand

@app.route('/move/hand/open/<string:hand>', methods=['GET'])
@crossdomain(origin='*')
def openHand_HTTP(hand):
    if not hand in ["LHand", "RHand"]:
        return jsonify({'error': 'Incorrect value for "hand"'}), 418
    return jsonify({'opened': openHand(hand)}), 200

def closeHand(hand):
    motionProxy = ALProxy("ALMotion", nao_host, nao_port)
    if(hand == "LHand"):
        motionProxy.closeHand("LHand")
    else:
        motionProxy.closeHand("RHand")
    return hand

@app.route('/move/hand/close/<string:hand>', methods=['GET'])
@crossdomain(origin='*')
def closeHand_HTTP(hand):
    if not hand in ["LHand", "RHand"]:
        return jsonify({'error': 'Incorrect value for "hand"'}), 418
    return jsonify({'closed': closeHand(hand)}), 200

#GET ALL FROM ROBOT
def getRobot():
    return jsonify({'ip':getIP(), 'type':getType(), 'name':getName(), 'batteryLevel':getBatteryLevel(), 'chargeStatus':chargeStatus, 'posture':doAction("StandInit"), 'actions':getActions()})

@app.route('/getRobot', methods=['GET'])
@crossdomain(origin='*')
def getRobot_HTTP():
    return getRobot(), 200

def getPicture_HTTP():
    try:
        photoCaptureProxy = ALProxy("ALPhotoCapture", nao_host, nao_port)
        photoCaptureProxy.setResolution(2)
        photoCaptureProxy.setPictureFormat("png")
        photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")
        with open("/home/nao/recordings/cameras/image_0.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return jsonify({'image': encoded_string})
    except Exception, e:
        return jsonify({'error': str(e)}), 200

"""
This function is purely to test the livestream of images while using a virtual robot, as it does not have a camera
In case of a real robot, transfer the app.route and crossdomain to the function above
"""
arnold_images = []
arnold_counter = 0
import base64
import os
for i in range(1, 8): # There are 7 Arnold images
    with open('{0}/img/arnold{1}.png'.format(os.path.dirname(os.path.realpath(__file__)), i), 'rb') as image_file:
        arnold_images.append(base64.b64encode(image_file.read()))

@app.route('/getPicture', methods=['GET'])
@crossdomain(origin='*')
def getArnold_HTTP():
    global arnold_images
    global arnold_counter

    tmp = jsonify({'image': arnold_images[arnold_counter]})
    arnold_counter = (arnold_counter + 1) % len(arnold_images)
    return tmp

if __name__ == '__main__':
    app.run(debug=True,host=webserverIp)
    randNum = randint(0,2)
