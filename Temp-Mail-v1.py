from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from json import loads,dumps
from time import sleep
from requests import get



def process_browser_log_entry(entry):
	response = loads(entry['message'])['message']
	return response


def getTempEmail(driver):
	driver.get('https://temp-mail.org')
	email = driver.execute_script("return document.getElementById('mail').value")
	print(f"Your temporary email is {email}.")
	with open('TempMail.txt','w') as f:
		f.write(email)
	return email



def getTempEmailApi(driver):
	print("Fetching Api....")
	while True:
		try:
			browser_log = driver.get_log('performance') 
			events = [process_browser_log_entry(entry) for entry in browser_log]
			events = [event for event in events if 'Network.response' in event['method']]
			url = events[-1]['params']['response']['url']
			if 'https://api4.temp-mail.org/request/mail/id/' in  url:
				print(events[-1]['params']['response']['url'])
				with open('APITempMail.txt','w') as f:
					f.write(url)
					f.close()
				break
		except:
			sleep(3)
	driver.quit()
	return url

def requestMail(url):
	while True:
		r = get(url)
		with open("Mails.txt",'w') as f:
			f.write(r.text)	
		try:
			loads(r.text)['error']
			print(loads(r.text)['error'])
		except:		
			createdAt = loads(r.text)[0]['createdAt']['$date']['$numberLong']
			createdAt = strftime('%m/%d/%Y %H:%M:%S', gmtime(createdAt/1000.))
			mail_from = loads(r.text)[0]['mail_from']
			mail_subject = loads(r.text)[0]['mail_subject']
			mail_text_only = loads(r.text)[0]['mail_text_only']
			mail_text_only = BeautifulSoup(mail_text_only).get_text().strip()

			mail_text = loads(r.text)[0]['mail_text']
			mail_text = BeautifulSoup(mail_text).get_text().strip()
			
			mail_attachments_count = loads(r.text)[0]['mail_attachments_count']
			mail_attachments = loads(r.text)[0]['mail_attachments']
			
			# data = {	'createdAt':createdAt,
			#             'mail_from':mail_from,
			#             'mail_subject':mail_subject,
			#             'mail_text_only':mail_text_only,
			#             'mail_text':mail_text,
			#             'mail_attachments_count':mail_attachments_count,
			#             'mail_attachments':mail_attachments
			# }
			print(f"createdAt:{createdAt}\nmail_from:{mail_from}\nmail_subject:{mail_subject}\nmail_text_only:{mail_text_only}\nmail_text:{mail_text}\nmail_attachments_count:{mail_attachments_count}\nmail_attachments:{mail_attachments}")
			#print(dumps(data, sort_keys=True, indent=4))
		input("Press Any Key to refresh or Control + C to stop")


while True:
	oldNew = input("Enter 0 for Existing Email or 1 to create A new Temp Mail: ")
	if oldNew == '0':
		try:
			with open('TempMail.txt','r') as f:
				email = f.read()
			with open('APITempMail.txt', 'r') as f:
				api = f.read()
			print(f"Your Email is {email}")
			requestMail(api)	
		except:
			print("FILE ERROR! Probably Need TO Create NEW TEMP MAIL")
	elif oldNew == '1':

		options = Options()
		options.add_argument('--headless')
		options.add_argument("--start-maximized")
		options.add_argument("--incognito")
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-gpu')
		options.add_argument('--disable-infobars')
		options.add_argument("--disable-extensions")
		options.add_experimental_option('w3c', False)

		caps = DesiredCapabilities.CHROME
		caps['loggingPrefs'] = {'performance': 'ALL'}


		driver = Chrome(options=options,desired_capabilities = caps)
		email = getTempEmail(driver)
		url = getTempEmailApi(driver)
		requestMail(url)
	else:
		print("Wrong Option. Please Select From the list")