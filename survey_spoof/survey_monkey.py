import requests, json, random
from argparse import ArgumentParser

def parse_args():
	# Returns the users parsed arguments 
	parser = ArgumentParser()
	parser.add_argument('--user', type=str, required=True)
	parser.add_argument('--url', type=str, required=True)
	parser.add_argument('--token', type=str, required=True)
	return parser.parse_args()


def main():
	# User is a name who'd you would like to vote for
	# R_Url is the link to send on survey monkey
	# Token is taken from the website ( This can be obtained by inspecting the button element)

	args = parse_args()
	user = args.user
	r_url = args.url
	survey_data_token = args.token

	comp_data = json.load(open("compliments.json","r"))
	choices_survey = {
		"Teamwork":"2339642436",
		"Respect":"2339642437",
		"Integrity":"2339642438",
		"Commitment":"2339642439",
		"Excellence":"2339642440"
	}

	r = requests.get(r_url)
	if not r.ok:
		print('HTTP', r.status_code)
		exit(1)
	else: 
		for i in comp_data:
			rand_choice = random.choice(list(choices_survey.values()))
			print('submitted', {
				'354222340': user, 
				'354222338': [index for index, value in choices_survey.items() if value == rand_choice][0], 
				'354222339': i
			})
			requests.post(r_url, data={
				'354222340': user, 
				'354222338': rand_choice, 
				'354222339': i,
				"survey_data": survey_data_token},
cookies=r.cookies)
	exit(0)

if __name__ == "__main__" :
	main()