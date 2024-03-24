import requests
import argparse
import os.path
import sys

debug = True

# if debug = True, ignore command line arguments and use the following:
ip = "192.168.50.20"
port = 8080
base_url = "http://{}:{}/api/v1".format(ip, port)
file = r"C:\Users\jadle\OneDrive\Desktop\Projects\Litter Bag Holder\Litter Bag Holder v3_0.2mm_PLA_A350_2h39m.gcode"

def get_token(url):
	""" requests session token """
	r = requests.post(url+"/connect")
	if r.status_code == 200:
		return r.json()["token"]
	else:
		return ""

def get_status(url, token):
	""" request printer status """
	payload = {"token": token}
	r = requests.get(url+"/status", params=payload)
	return r

def post_file(url, token, file):
	""" upload file to printer """
	payload = {"token": token}
	file_payload = {"file": open(file, 'rb')}
	r = requests.post(url+"/upload", params=payload, files=file_payload)


if __name__ == "__main__":
	if not debug:
		parser = argparse.ArgumentParser(description="upload a gcode file to snapmaker2.0")
		parser.add_argument("-p", dest='port', help="port number (default=8080)", default=8080, type=int)
		parser.add_argument("-i", dest='address', help="ip address or hostname of printer", default=ip)
		parser.add_argument("filename", help=".gcode file to upload", default=file, type=str)
		args = parser.parse_args()

		if not args.filename.endswith(".gcode"):
			print("Invalid file type")
			sys.exit()
		file = args.filename
		base_url = "http://{}:{}/api/v1".format(args.address, args.port)
	try:
		token = get_token(base_url)
		# assert token
	except:
		print("Couldn't connect to printer")
		sys.exit()

	status = get_status(base_url, token)
	while status.status_code == 204:
		status = get_status(base_url, token)

	if status.status_code == 200:
		try:
			assert os.path.isfile(file)
			print("Attempting upload...")
			post_file(base_url, token, file)
		except:
			print("ERROR: check connection/path")
			sys.exit()
	else:
		print("Upload rejected")