import datetime
import time
import requests
import http.client
import json
import urllib.request
import os


api_domain = 'api.nasa.gov'
api_key = 'your-api-key-here'


def get_apod_data_from_nasa_api():
	url = f'/planetary/apod?api_key={api_key}'
	conn = http.client.HTTPSConnection(api_domain)
	conn.request("GET", url)
	response = conn.getresponse()
	data = response.read()
	data_decoded = data.decode("utf-8")
	return json.loads(data_decoded)


def get_image_url_from_apod_data(data, is_hd):
	date = data["date"]
	print("date: " + date)
	explanation = data["explanation"]
	print("explanation: " + explanation)
	hdurl = data["hdurl"]
	print("hdurl: " + hdurl)
	media_type = data["media_type"]
	print("media_type: " + media_type)
	service_version = data["service_version"]
	print("service_version: " + service_version)
	title = data["title"]
	print("title: " + title)
	url = data["url"]
	print("url: " + url)

	if is_hd:
		return hdurl
	else:
		return url


def get_format_from_url_image(url_image):
	if url_image and ('.' in url_image):
		format = url_image.split('.')[-1]
		print("format image: " + format)
		return format


def save_image_from_url_on_drive(url_image, filename, format):
	path = "/home/user/Desktop/"
	file = filename + ".jpg" #format
	urllib.request.urlretrieve(url_image, path + file)
	print ("Success! Image saved as: " + path + file)
	return file


def change_background_fail_one(file):
	if file and ('.' in file):
		dir = "/home/user/Desktop/"
		path = dir + file
		command2 = f'export DISPLAY=":1" && pcmanfm --set-wallpaper {path}'
		print(f'Command to execute by os.system is: {command2}')
		os.system(command2)


def change_background_fail_two(file):
	if file and ('.' in file):
		dir = "/home/user/Desktop/"
		path = dir + file
		content = f'"#! /bin/sh\nexport DISPLAY=:0\npcmanfm --set-wallpaper {path}"'
		#os.system(f'echo {content} > {dir}change_background.sh')
		#os.system(f'echo "date" > {dir}change_background.sh')
		#os.system(f'bash {dir}change_background.sh')
		os.system(f'xwallpaper --zoom {path}')

def main():
	try:
		data = get_apod_data_from_nasa_api()
		url_img = get_image_url_from_apod_data(data, False)
		format_img = get_format_from_url_image(url_img)
		file = save_image_from_url_on_drive(url_img, data["date"], format_img)
	except Exception as ex:
		print("An error occurred while retrieving data from NASA api." + str(ex))

main()
