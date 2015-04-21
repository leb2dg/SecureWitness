#!/usr/bin/python

from Crypto.PublicKey import RSA
from Crypto import Random
from os.path import expanduser
import sys
import requests
import getpass
from os.path import expanduser

# enter username
usrnm = raw_input("Please enter your Secure Witness username: ")
#print ('Your input was' + " " + usrnm)
# enter password
psswrd = getpass.getpass("Please enter your Secure Witness password: ")
#print ('Your input was' + " " + psswrd)

# if logged in properly then show files available
payload = {'username': usrnm, 'password': psswrd}
r = requests.post("http://localhost:8000/SecureWitness/login_decrypt/", data=payload)
print(r.text)
# if authentification failed then quit
if r.text == "unsuccessful authentication" or r.text == 'Your account has been suspended by an administrator':
	print "Exiting application..."
	sys.exit(0)

# display reports that can be downloaded
payload = {'username': usrnm, 'password': psswrd}
r = requests.post("http://localhost:8000/SecureWitness/viewReports_decrypt/", data=payload)
print "Reports you have access to:"
print(r.text)
if r.text == "unsuccessful authentication":
	print "Exiting application..."
	sys.exit(0)

check = False
while check == False:
	# display files that can be downloaded in specified report
	rpt = raw_input("Please enter the report name you would like to view: ")
	payload = {'username': usrnm, 'password': psswrd, 'report': rpt}
	r = requests.post("http://localhost:8000/SecureWitness/viewFiles_decrypt/", data=payload)
	if r.text == "unsuccessful authentication":
		print "Exiting application..."
		sys.exit(0)
	if r.text != "Report not found.":
		check = True
		print "Report:" + "\t" + "Author:" + "\t" + "Short Description:" + "\t" + "Long Description:" + "\t" +"Loation:" + "\t" + "Keywords:" + "\t" + "Date:" + "\t" + "File:"
		print(r.text)
	else:
		print "Report not found. Please enter a valid report."

check = False
while check == False:
	# user enters file to decrypt 
	file_enc = raw_input("Please enter the file you wish to decrypt: ")
	#print ('Your input was' + " " + file_enc)
	print ""

	# check if user has access via django server and get key to decrypt
	payload = {'username': usrnm, 'password': psswrd, 'report': rpt, 'file': file_enc}
	r = requests.post('http://localhost:8000/SecureWitness/uploaded_key/', data=payload)
	#print r.text
	if r.text == "unsuccessful authentication" or r.text == 'Your account has been suspended by an administrator':
		print "Exiting application..."
		sys.exit(0)
	if r.text != "Invalid file name.":
		check = True
		key = RSA.importKey(r.text)
	else:
		print "File not found. Please enter a valid file name."

# gets file to decrpyt
r = requests.get('http://localhost:8000/SecureWitness/uploaded_files/' + file_enc)
enc_data = r.content

# decrypt 
# print decrypted file contents
decrypted = key.decrypt(enc_data) 
#print decrypted

# write back descrypted to file
downloads_dir = expanduser("~/Downloads/") + file_enc

newFile = open(downloads_dir, 'w')
newFile.write(decrypted)
newFile.close()

print "File downloaded to '" + downloads_dir + "'"

