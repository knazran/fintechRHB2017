import csv
import random
import timeit

filename_in = "transactional_dat.csv"
account_f = "accounts-large.csv"
users_f = "users-large.csv"
file_out = "trans-out.csv"
num_account = 1000
num_users = 500

# CSV stuff
in_read = csv.reader(open(filename_in,"rb"), delimiter=',',quoting=csv.QUOTE_ALL)
account_write = csv.writer(open(account_f,"wb"), delimiter=',',quoting=csv.QUOTE_ALL)
user_write = csv.writer(open(users_f,"wb"), delimiter=',',quoting=csv.QUOTE_ALL)
out_write = csv.writer(open(file_out,"wb"), delimiter=',',quoting=csv.QUOTE_ALL)

out_write.writerow(["Time","Account_Num", "Transaction_Num", "Amount"])
account_write.writerow(["Account"])
user_write.writerow(["User", "Spend_Limit", "Round_up"])

accounts = []
users = []
spending_limit = [500, 1000, 5000, -99]
round_up = [0, 1]

start = timeit.default_timer()

# Generate random account numbers and users
for i in range(0,num_account):
	account = ''.join(random.choice('0123456789') for i in range(16))
	accounts.append(account)
	account_write.writerow([account])

	if i < num_users:

		user_write.writerow([account, random.choice(spending_limit), random.choice(round_up)])

# Random generator
secure_random = random.SystemRandom()

# Get a new data set
in_read.next()
for row in in_read:
	random_acc = random.choice(accounts)
	transac_num = ''.join(secure_random.choice('0123456789ABCDEF') for i in range(32))
	out_write.writerow([row[0],random_acc, transac_num, row[1]])

stop = timeit.default_timer()
print "RUN TIME: " + str(stop - start)


