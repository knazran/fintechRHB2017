from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS, cross_origin

# Set up flask
app = Flask(__name__)
CORS(app)

# Our ephemeral database because hooking up to AWS takes time and I aint got no time
transcs = {}

@app.route("/")
def main():
    return "Welcome! This is Trickle's service server"

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/get_transc', methods=['GET'])
def get_transc():
	if not request.args.get('acc_num'):
		abort(400)

	acc_num = request.args.get('acc_num')
	if acc_num in transcs:
		return jsonify({acc_num: transcs[acc_num]})
	else:
        # TO DO return a more descriptive error message
		abort(404)

@app.route('/todo/api/v1.0/post_transc', methods=['POST'])
def post_transc():
    if not request.json or not 'datetime' in request.json or not 'transc_num' in request.json or not 'transc_amnt' in request.json or not 'acc_num' in request.json:
        abort(400)
    transc = {
    	'datetime' : request.json['datetime'],
        'transc_num': request.json['transc_num'],
        'transc_amnt': request.json['transc_amnt'],
        'data': {}
    }
    # Place in user dictionary
    user_acc = request.json['acc_num']
    if user_acc in transcs:
    	transcs[user_acc].append(transc)
    else:
    	transcs[user_acc] = [transc]

    return jsonify({'transc': transc}), 201

if __name__ == "__main__":
    app.run(debug=True)