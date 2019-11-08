from flask import request
from flask import jsonify
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test")
def test():
    return "Hello test!"

@app.route("/greeting")
def greeting():
    name = request.args.get('name')
    return "<p><h3>Hello "+name+"</h3></p>"

@app.route("/testjson")
def testjson():
    get_id = request.args.get('id')
    d = dict()
    d['id']=get_id
    d['score']=[{'quiz1':20,'quiz2':30,'quiz3':25},{'quiz1':21,'quiz2':23,'quiz3':19}]
    return jsonify(d)

@app.route("/insertscore")
def getscore():
	client = MongoClient("mongodb+srv://6131866021:1234@cluster0-3xijp.mongodb.net/test?retryWrites=true&w=majority")
	db = client.student_scores
	file = open('score.csv')
	list_of_score = []
	for line in file:
		score = line.split(',')
		score = [int(e) for e in score]
		dscore = {'id':score[0], 'quiz1':score[1], 'quiz2':score[2], 'quiz3':score[3], 'quiz4':score[4], 'quiz5':score[5], 'sum': sum(score[1:])}
		list_of_score.append(dscore)
	db.scores.delete_many({})
	result = db.scores.insert_many(list_of_score, ordered=False)
	return "upload done"

@app.route("/findscore")
def findscore():
	client = MongoClient("mongodb+srv://6131866021:1234@cluster0-3xijp.mongodb.net/test?retryWrites=true&w=majority")
	db = client.student_scores
	getid = request.args.get('id')
	docs = db.scores.find_one({'id':int(getid)})
	ret = {'id':docs['id'], 'quiz 1':docs['quiz1'], 'quiz 2':docs['quiz2'], 'quiz 3':docs['quiz3'], 'quiz 4':docs['quiz4'], 'quiz5':docs['quiz 5'], 'sum':docs['sum']}
	r = dict()
	r['data'] = ret
	return jsonify(r)
