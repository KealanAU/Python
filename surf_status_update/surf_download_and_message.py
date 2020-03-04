import requests, re, json, time
from bs4 import BeautifulSoup
from twilio.rest import Client 

user_id = ""
auth_token = ""
client = Client(user_id, auth_token) 
location = "Curl Curl".replace(" ","-")
now = time.localtime()
download_url = f"https://magicseaweed.com/{location}-Surf-Report/1000/Print-Ready/"


def apos_repl_attach(matchedObj):
		# matches in the seach function and appends : 
		return f'"{matchedObj[0][:-2]}":'



def main(): 
	
	r =  requests.get(download_url)

	if r.ok: 
		# Checks if r is possible to access
		r_soup = BeautifulSoup(r.content, 'html.parser')

		# Finds script tag and loads them into text
		text = r_soup.find_all('script')
		

		# Regex checks for Forecast or tide and the relvant json within them 
		text = re.search("forecast: \[.*\]\,\n\t*tide: {.*}", str(text))[0]

		replaced_with_function_apos = re.sub('(\w+)\:\ ', apos_repl_attach, text)

		# Breaks out the forecast that is provided
		forecast = re.search('"forecast":\[.*\]', replaced_with_function_apos)[0]
		# Breaks out the tide that is provided
		tide = re.search('"tide":\{.*\}', replaced_with_function_apos)[0]
		# cleans so it's valid JSON
		forecast_tide_joined = "{" + forecast + "," + tide +"}"

	forecast_tide_joined = json.loads(forecast_tide_joined)

	with open("forecast.json", "w") as file:
		file.write(forecast)

	print(time.strftime('%Y-%m-%d', now))
	 

	for index, value in enumerate(forecast_tide_joined["forecast"]):

		if time.strftime('%Y-%m-%d', now) == time.strftime('%Y-%m-%d', time.localtime(value["timestamp"])) :

			if( 12 <= int(time.strftime("%H", time.localtime(value["timestamp"]))) <= 20 ):
				msg_send = [location.replace("-"," "), " Surf Report for ",
							time.strftime("%A", time.localtime(value["timestamp"])),
							" at ",
							time.strftime("%H:%M", time.localtime(value["timestamp"])), 
							"\n" ,
						 	value["swell"]["height"],
						 	value["swell"]["unit"], " ",
							value["swell"]["compassDirection"], "Swell",
							"\n",
							value["wind"]["stringDirection"], " ",
							value["wind"]["compassDirection"]," Wind"
							]
				result = ''
				for element in msg_send:
				    result += str(element)
				message = client.messages.create( 
								from_='whatsapp:+14155238886',  
								body=f"{result}",      
								to='whatsapp:+61402201922' 
							) 

	print(message.sid)	

	 

if __name__ == "__main__":
	main()


	 




