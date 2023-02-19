from flask import Flask
from flask_restful import Resource, Api
from flask import request
import joblib
import numpy as np

app = Flask(__name__)
api = Api(app)

SVR_MODEL = joblib.load('final_svr.pkl')
RFR_MODEL = joblib.load('final_rfr.pkl')
SCALER = joblib.load('education_gini_scaler.pkl')

@app.route("/", methods=['POST'])
def post():
    data = request.get_json()
    return {
        'actual': {
            1975: 33.3,
            1981: 32.4,
            1987: 31.5,
            1991: 31.0,
            1994: 31.3,
            1997: 31.6,
            1998: 33.2,
            2000: 33.3,
            2004: 33.7,
            2007: 33.8,
            2010: 33.6,
            2012: 33.5,
            2013: 33.8,
            2014: 33.2,
            2015: 33.7,
            2016: 32.7,
            2017: 33.3
        },
        'prediction': generatePrediction(data.get('model'), data.get('params'))
    }

def scale(params):
    return SCALER.fit_transform(np.array(params).reshape(1, -1))

def generatePrediction(model, params):
    if model == 'svr':
        current_model = SVR_MODEL
    else:
        current_model = RFR_MODEL
    print(params)
    return current_model.predict(scale(params))[0]

if __name__ == '__main__':
    app.run(debug=True)