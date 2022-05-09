import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download('omw-1.4')
nltk.download('wordnet')
import re
from flask import Flask, redirect, url_for, request
from flask_restful import Api, Resource
from flask import render_template
import pickle;
import json
from flask_cors import CORS
BAYES="";
with open('../model_creation/naive-bayes.pkl','rb') as f:
    BAYES=pickle.load(f);

SVM="";
with open('../model_creation/svm.pkl','rb') as f:
    SVM=pickle.load(f);

NN="";
with open('../model_creation/mlp.pkl','rb') as f:
    NN=pickle.load(f);

#Clean up our data
def clean_text(text):
    rem = re.compile(r'')
    rem2 = re.compile(r'[^a-zA-Z \-]')
    text = re.sub(rem,'',text)
    text = re.sub(rem2,'',text)
    return text.lower()

def cleanup_stopwords(text):
    stop_words = set(stopwords.words('english'))
    #print(text)
    rem = re.compile(r' +')
    text = re.sub(rem,' ',text)
    textarr = text.strip().split(' ');
    #print(textarr)
    new_text=""
    for x in textarr:
        if x not in stop_words:
            new_text=new_text+ " "+x
        #else:
            #print("excluded: " +x)
    return new_text;

net = WordNetLemmatizer()
def lemmatize(text):
    textarr = text.strip().split(' ');
    newtext=""
    for word in textarr:
        newtext=newtext+" "+net.lemmatize(word)
    return newtext

def clean_headline(text):
    
    #clean headline
    text = clean_text(text);
    text = cleanup_stopwords(text);
    text = lemmatize(text)

    return text;


def predict(text):
    returnObj = dict();

    #call each model, add attr to dict
    nt = []
    nt.append(text)
    text=nt;
    returnObj["bayes"] = BAYES.predict(text)[0]
    returnObj["svm"] = SVM.predict(text)[0];
    returnObj["mlp"] = NN.predict(text)[0];


    return json.dumps(returnObj);


app = Flask(__name__)
CORS(app)
api = Api(app)
class ModelAPI(Resource):

    @app.route('/predict',methods=['POST'])
    def post():
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            req = request.json
            headline = req["headline"]
            headline = clean_headline(headline)
            return predict(headline)
    
    @app.route('/testdata',methods=['GET'])
    def get():
        f= open("../model_creation/testdata.json","r");
        rStr = f.read();
        return rStr

    @app.route('/')
    def hello():
       return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True);
