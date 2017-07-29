import csv

filename_in = "creditcard.csv"
filename_out = "transactional_dat.csv"

in_read = csv.reader(open(filename_in,"rb"), delimiter=',',quoting=csv.QUOTE_ALL)
out_write = csv.writer(open(filename_out,"wb"), delimiter=',',quoting=csv.QUOTE_ALL)
out_write.writerow(["Time", "Amount"])

in_read.next() # Ignore header

# META SETTTING
max_rows = 1000
count = 0


for row in in_read:
	# if count > max_rows:
		# break
	out_write.writerow([row[0], row[29]])
	count = count + 1
