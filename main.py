import requests, json, time, random, datetime, threading, pickle
from termcolor import colored

sitekey = "6Ld-VBsUAAAAABeqZuOqiQmZ-1WAMVeTKjdq2-bJ"


def log(event):
	d = datetime.datetime.now().strftime("%H:%M:%S")
	print("Raffle OFF-S by Azerpas :: " + str(d) + " :: " + event)
		
class Raffle(object):
	def __init__(self):
		self.s = requests.session()
		self.shoes = [
		{"shoe_id":"8","shoe_name":"ZOOM VAPORFLY"},
		{"shoe_id":"7","shoe_name":"VAPOR MAX"}]
		self.url = "https://www.offspring.co.uk/view/component/entercompetition"

	def register(self,identity):
			# register to each shoes.
			for dshoes in self.shoes:

				print("Signin for: " + dshoes['shoe_name'])

				d = datetime.datetime.now().strftime('%H:%M')
				log("Getting Captcha")
				flag = False
				while flag != True:
					d = datetime.datetime.now().strftime('%H:%M')
					try:
						file = open(str(d)+'.txt','r') #r as reading only
						flag = True
					except IOError:
						time.sleep(2)
						log("No captcha available(1)")
						flag = False
				try:
					FileList = pickle.load(file) #FileList the list where i want to pick out the captcharep
				except:
					log("Can't open file")
				while len(FileList) == 0: #if len(FileList) it will wait for captcha scraper 
						d = datetime.datetime.now().strftime('%H:%M')
						try:
							file = open(str(d)+'.txt','r')
							FileList = pickle.load(file)
							if FileList == []:
								log("No captcha available(2)")
								time.sleep(3)
						except IOError as e:
							log("No file, waiting...")
							print(e)
							time.sleep(3)
				captchaREP = random.choice(FileList) 
				FileList.remove(captchaREP)
				file  = open(str(d)+'.txt','w')
				pickle.dump(FileList,file)
				log("Captcha retrieved")

				# captcha
				headers = {
					"authority":"www.offspring.co.uk",
					"method":"POST",
					"path":"/view/component/entercompetition",
					"scheme":"https",
					"accept":"*/*",
					"accept-encoding":"gzip, deflate, br",
					"accept-language":"fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4",
					"content-length":"624",
					"content-type":"application/x-www-form-urlencoded; charset=UTF-8",
					"origin":"https://www.offspring.co.uk",
					"referer":"https://www.offspring.co.uk/view/content/nikecompetition",
					"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
					"x-requested-with":"XMLHttpRequest",}

				payload = {"firstName":identity['fname'],
							"lastName":identity['lname'],
							"competitionIDEntered":dshoes['shoe_id'],
							"competitionNameEntered":dshoes['shoe_name'],
							"emailAddress":identity['mail'],
							"phoneNumber":identity['phone'],
							"optIn":"false",
							"size":identity['shoesize'],
							"grecaptcharesponse":captchaREP,
					}


				req = self.s.post(self.url,headers=headers,data=payload)
				print(req)
				jsonn = json.loads(req.text)
				if req.status_code == 200:
					if jsonn['statusCode'] == "success":
						print(colored('Successfully entered','red', attrs=['bold']))
				sleep = random.uniform(2.3,2.9)
				log("Sleeping: " + str(sleep) + " seconds")
				time.sleep(sleep)
				self.s.cookies.clear()

if __name__ == "__main__":
	ra = Raffle()
	accounts = [
		# 11 5US , 18 9US , 14 7US
		{"fname":"pete","lname":"james","mail":"7768james@gmail.com","phone":"+33612334455","city":"London","zip":"HEC 178","shoesize":"10",},
		]
	# catpcha 
	for i in accounts:
		ra.register(i)
