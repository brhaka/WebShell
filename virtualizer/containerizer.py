import docker
import threading
import time
import atexit
import base64
import os
from datetime import datetime, timedelta
from termcolor import colored
from urllib import request
from flask import Flask, jsonify, request
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

maxLifeTime = timedelta(minutes=21) # Container maximum active time without any interaction from the user
containers = {}
isExiting = {}

class CryptManager():
	iterations = 1000000
	keyLength = 0

	# Encrypts 'data' and returns it
	@staticmethod
	def crypt_data(data, password):
		salt = os.urandom(16)
		kdf = PBKDF2HMAC(algorithm=hashes.SHA3_512(), length=32, salt=salt, iterations=CryptManager.iterations)
		key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

		f = Fernet(key)

		CryptManager.keyLength = len(key)

		return (key + f.encrypt(data.encode())).decode()

	# Decrypts 'data' and returns it
	@staticmethod
	def decrypt_data(data):
		key = data[:CryptManager.keyLength].encode()
		data = data[CryptManager.keyLength:].encode()

		f = Fernet(key)
		decrypted_data = f.decrypt(data).decode()

		return decrypted_data

# Initiates Flask
app = Flask(__name__)

@app.route("/start", methods = ["GET"])
def start():
	client = docker.from_env()

	container = client.containers.run("debian:latest", detach=True, tty=True)
	# container.exec_run("yes | unminimize")

	rtrn = {
		"id": CryptManager.crypt_data(container.id, "W6d#34jwahk^2537$%3v#$3^6@#3%8")
	}

	containers[container.id] = datetime.now()
	isExiting[container.id] = False

	# Stops the container after some time
	stopThread = threading.Thread(target=checkLifeTime, args=(container.id,))
	stopThread.setDaemon(True)
	stopThread.start()

	containerActionPrint(container.id, "Created", "green")

	return rtrn

@app.route("/executeCommand", methods = ["GET"])
def executeCommand():
	command = request.args.get("command", default="", type=str)
	id = request.args.get("id", default="", type=str)
	client = docker.from_env()

	if id == "":
		return {
			"return": "ERROR:0x001"
		}

	if command == "":
		return {
			"return": "ERROR:0x004"
		}

	id = CryptManager.decrypt_data(id)

	try:
		container = client.containers.get(id)
	except docker.errors.NotFound:
		return {
			"return": "ERROR:0x002"
		}

	msg = container.exec_run(command)

	rtrn = {
		"return": msg[1].decode()
	}

	# Stores the container active date
	containers[container.id] = datetime.now()

	return rtrn

def checkLifeTime(id):
	while True:
		# print("Container active date:", datetime.now() - activeDate[id])
		if containers[id] == None or datetime.now() - containers[id] > maxLifeTime:
			break
		time.sleep(0.1)

	stop(id)

def stop(id):
	if id == "":
		print("ERROR:0x001")
		return

	if isExiting[id]:
		return
	isExiting[id] = True

	client = docker.from_env()

	container = client.containers.get(id)

	container.stop()
	container.remove()

	containers[container.id] = None

	containerActionPrint(id, "Destroyed", "red")

def exit():
	runningContainers = [id for id, status in containers.items() if status]

	if len(runningContainers) <= 0:
		return

	print(colored(f"\nStopping {len(runningContainers)} running container{'s' if len(runningContainers) > 1 else ''}.", "yellow"))
	print("Please wait...")

	threads = []
	for container in runningContainers:
		threads.append(threading.Thread(target=stop, args=(container,)))

	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()

	for container in runningContainers:
		while containers[id] != None:
			time.sleep(0.1)

	print("Done.\n\nExiting...")

def containerActionPrint(containerId, action, actionColor):
	msg = "Container (" + containerId[0:5] + ") "

	delimiter = "#"
	for i in range(len(msg) + len(action) + 2):
		delimiter += "*"
	delimiter += "#"

	msg = colored(delimiter + "\n# ", "cyan") + msg
	msg += colored(action, actionColor)
	msg += colored(" #\n" + delimiter, "cyan")

	print(msg)

atexit.register(exit)

if __name__ == "__main__":
	port = 8000
	app.run(threaded=True, host="0.0.0.0", port=port)
