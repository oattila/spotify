import constants
import requests
import webbrowser
import base64
import re
import os

class Exp(Exception):
	def __init__(self, url, response):
		self.url = url
		self.response = response
		super().__init__()

	def __str__(self):
		return self.url + ": " + str(self.response.status_code) + "\n" + str(self.response.json)

class Connection:
	def __init__(self):
		self.refreshToken = GetRefreshToken()
		self.UpdateAccessToken()

	def UpdateAccessToken(self):
		print("Updating access token")

		response = requests.post(constants.TOKEN_URL,
			headers = {"authorization": "Basic " + GetBase64ClientIdClientSecret()},
			data = {"grant_type": "refresh_token", "refresh_token": self.refreshToken})

		if not response.ok:
			raise Exception("Ei menny hyvin: " + str(response.status_code))

		data = response.json()

		if not "access_token" in data:
			raise Exception("Ei menny hyvin, ei access_tokenia")

		self.access_token = data["access_token"]

	def Get(self, url, params = None):
		headers = {"Authorization": "Bearer " + self.access_token}
		response = requests.get(url, params = params, headers = {"Authorization": "Bearer " + self.access_token});

		if response.status_code == 429:
			print("RATE LIMITING IN ACTION")
			print(str(response.json()))
			input()
			return Get(self, url, params)

		if not response.ok:
			raise Exp(url, response)

		return response.json()


	def Post(self, url, data):
		headers = {"Authorization": "Bearer " + self.access_token}

		response = requests.post(url, json = data, headers = {"Authorization": "Bearer " + self.access_token});

		if response.status_code == 429:
			print("RATE LIMITING IN ACTION")
			print(str(response.json()))
			input()
			return Post(self, url, data)

		if not response.ok:
			raise Exp(url, response)

		return response.json()


	def Put(self, url, data):
		headers = {"Authorization": "Bearer " + self.access_token}

		response = requests.put(url, json = data, headers = {"Authorization": "Bearer " + self.access_token});

		if response.status_code == 429:
			print("RATE LIMITING IN ACTION")
			print(str(response.json()))
			input()
			return Put(self, url, data)

		if not response.ok:
			raise Exp(url, response)


def GetCode():
	scope = constants.SCOPE
	params = { "client_id": constants.CLIENT_ID, "response_type": "code", "redirect_uri": constants.REDIRECT_URL, "scope": scope }
	response = requests.get(constants.AUTHORIZE_URL, params = params)
	url = response.url

	webbrowser.open(response.url)
	print("Kerro koodi: ", end = "")
	code = input()
	assert(code)
	return code

def GetBase64ClientIdClientSecret():
	s = constants.CLIENT_ID + ":" + constants.CLIENT_SECRET
	bytes = base64.b64encode(s.encode("utf8"))
	return str(bytes, "utf8")

def GetRefreshToken():
	if not os.path.isfile(constants.REFRESH_TOKEN_FILE_NAME):
		MakeRefreshToken();

	print("Reading refresh token from " + constants.REFRESH_TOKEN_FILE_NAME)

	with open(constants.REFRESH_TOKEN_FILE_NAME, "r") as file:
		token = file.readline()

	assert(token)
	return token

def MakeRefreshToken():
	print("Making refresh token")

	code = GetCode()

	response = requests.post(constants.TOKEN_URL,
		headers = {"authorization": "Basic " + GetBase64ClientIdClientSecret()},
		data = {"grant_type": "authorization_code", "code": code, "redirect_uri": constants.REDIRECT_URL })

	data = response.json()

	if not response.ok:
		raise Exception("Ei menny hyvin: " + str(response.status_code))

	if not "refresh_token" in data:
		raise Exception("Ei refresh_tokenia")

	refreshToken = data["refresh_token"]

	with open(constants.REFRESH_TOKEN_FILE_NAME, "w") as file:
		file.write(refreshToken)

	print("Refresh token was written to " + constants.REFRESH_TOKEN_FILE_NAME)

connection = None

def GetConnection():
	global connection

	if not connection:
		connection = Connection()
	
	return connection

def main():
	connection = Connection();
	print(connection.Get(constants.ME_URL)["email"])

if __name__ == "__main__":
	main()
