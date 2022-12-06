import json
import sys
from hashlib import md5
import base64
from cryptography.fernet import Fernet

key = str()

def keyGen(passwd):
	return base64.b64encode(md5(passwd.encode("utf-8")).hexdigest().encode())

def writeDB(data, filename):
	global key
	strdata = json.dumps(data)
	fr = Fernet(key)
	ciph_text = fr.encrypt(strdata.encode())
	ciph_text = ciph_text.decode()
	with open("creds.txt", "w") as f:
		f.write(ciph_text)

def rem(data):
	print("\033c", end="")
	printData(data)
	choice = int(input("Which login to remove: "))
	data.pop(choice)
	return data
	
def add(data):
	print("\033c", end="")
	app = input("app  : ")
	name = input("user : ")
	passwd = input("pass : ")

	data.append({"app":app, "username":name, "password":passwd})
	return data

def printData(data):
	for i in range(len(data)):
		print("ID   : "+str(i))
		print("app  : "+data[i]["app"])
		print("user : "+data[i]["username"])
		print("pass : "+data[i]["password"])
		print("\n--------------------------------\n")

def readDB(filename):
	global key
	password = input("Decryption key: ")
	key = keyGen(password)

	with open(filename) as f:
		data = f.read()
	try:
		fr = Fernet(key)
		ciph_text = data.encode()
		plain = fr.decrypt(ciph_text)
		jdata = json.loads(plain)
	except:
		print("\033c", end="")
		print("Invalid Decryption Key !!")
		exit()

	return jdata

def main(filename):
	print("\033c", end="")
	data = readDB(filename)
	try:
		while True:
			print("\033c", end="")
			printData(data)
			com = str(input("add / remove user\n(a/r) ~> "))
			if (com == "a" or com == "A" or com == "add" or com == "Add" or com == "ADD"):
				data = add(data)
				writeDB(data, filename)
			elif (com == "r" or com == "R" or com == "remove" or com == "Remove" or com == "REMOVE"):
				data = rem(data)
				writeDB(data, filename)
			else:
				print("\033c", end="")
				return 0
	except KeyboardInterrupt:
		print("\033c", end="")
		return 0




print("\n")
main(sys.argv[1])
