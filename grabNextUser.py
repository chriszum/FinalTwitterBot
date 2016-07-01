from twitter_info import get_twit_info
def grab_next_user():
	with open ("count.txt", "r") as myfile:
		data=myfile.read()
		count = int(data) + 1


		newtxt = str(count)
		print("Grabbing number " + newtxt + " in the list")

	text_file = open("count.txt", "w")
	text_file.write(newtxt)
	text_file.close()

	import requests
	response = requests.get('https://docs.google.com/spreadsheets/d/1_4Nwvrwsasrztbh5ITv8C7dFaj9yZIVyYXfF0j8Gm0U/pub?gid=0&single=true&output=csv')
	assert response.status_code == 200, 'Wrong status code'
	cool_list = response.content
	cool_csv = list(cool_list.splitlines())
	print(cool_csv)
	try:
		cool_user = (cool_csv[count])
		print ("Running Tweety Bot for" + cool_user)
		get_twit_info(cool_user)
	except IndexError:
		print('You did it again. We ran through the whole dang list. It will start again at the beginning tomorrow.')
		text_file = open("count.txt", "w")
		text_file.write('0')
		text_file.close()



