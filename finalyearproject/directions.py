from django.conf import settings
import requests
import json

'''  Portion of Code from Bobby Stearman at 
     Scope: directions calculations and api call
https://github.com/bobby-didcoding/did_django_google_maps_api/blob/main/main/mixins.py   
Date Published:  July 20th 2021 '''

#handles and calculates directions. 
def Directions(*args, **kwargs):
	#the longitute and latitude parameters used in getting the relevant info. 
	lat_a = kwargs.get("lat_a")
	long_a = kwargs.get("long_a")
	lat_b = kwargs.get("lat_b")
	long_b = kwargs.get("long_b")

	origin = f'{lat_a},{long_a}'
	destination = f'{lat_b},{long_b}'

	#extract results from the api using the key
	result = requests.get(
		'https://maps.googleapis.com/maps/api/directions/json?',
		 params={
		 'origin': origin,
		 'destination': destination,
		 "key": settings.GOOGLE_API_KEY
		 })

	#converts results into a JSON file to output it onto the site. 
	directions = result.json()

	#Checks status of the json file before extracting travel information
	if directions["status"] == "OK":

		route = directions["routes"][0]["legs"][0]
		origin = route["start_address"]
		destination = route["end_address"]
		distance = route["distance"]["text"]
		duration = route["duration"]["text"]

		steps = [
			[
				s["distance"]["text"],
				s["duration"]["text"],
				s["html_instructions"],

			]
			for s in route["steps"]]
		
	#travel information returned in a dictionary format
	return {
		"origin": origin,
		"destination": destination,
		"distance": distance,
		"duration": duration,
		"steps": steps
		}