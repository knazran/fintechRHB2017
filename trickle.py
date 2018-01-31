import csv
import math
import timeit
import requests

# A dumb algorithm implementation
def roundUp(num, round_to):
	if not round_to:
		change = round(math.ceil(num) - num, 2)
		if change > 0.5:
			change = round(change - 0.5)
		return str(change)
	else:
		num = num / 10
		change = round(math.ceil(num) - num, 2)
		if change > 0.5:
			change = round(change - 0.5)
		return str(change * 10)

# Make a POST request to our backend, requesting for transaction
# In PROD, the request should be to the payment gateway to initiate payment
def sendToBackend(time, change_amnt, transc_num, acc_num):
	url = "http://localhost:5000/todo/api/v1.0/post_transc"
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	data = {
		'datetime' : time,
		'acc_num': acc_num,
        'transc_num': transc_num,
        'transc_amnt': change_amnt
	}
	r = requests.post(url=url, headers=headers, json=data)
	print r.status_code

# File names
filename_in = "trans-out.csv"
user_f = "users-large.csv"

# Read csv
in_read = csv.reader(open(filename_in,"rb"), delimiter=',',quoting=csv.QUOTE_ALL)
users_read = csv.reader(open(user_f,"rb"), delimiter=',',quoting=csv.QUOTE_ALL)
in_read.next()
users_read.next()

# Create user dict
# Optimization problem here if user list doesn't fit in memory
users_dict = {}
for user in users_read:
	users_dict[user[0]] = {"spending-limit" : user[1], "round-to" : user[2]}

start = timeit.default_timer()
for row in in_read:
	# row[0] == time
	# row[1] == account
	# row[2] == transaction number 
	# row[3] == amount

	# See if account number is our users
	if row[1] in users_dict:
		user_info = users_dict[row[1]]
		if float(row[3]) <= float(user_info["spending-limit"]):
			change = roundUp(float(row[3]), float(user_info["round-to"]))
			if change != "0.0":
				sendToBackend(row[0], change, row[2], row[1])
				print "REQUEST TRANS AMNT " + change + " FROM " + row[1] + " REFNUM: " + row[2]
			else:
				print "NO CHANGE FROM " + row[1] + " REFNUM: " + row[2]
		else:
			print "ABOVE SPENDING LIMIT. ACCOUNT NUM: " + row[1] + " REFNUM: " + row[2]

stop = timeit.default_timer()
print "RUN TIME: " + str(stop - start)