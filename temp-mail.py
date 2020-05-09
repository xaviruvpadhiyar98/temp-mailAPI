from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep,strftime,gmtime
from requests import get
from json import loads,dumps
from bs4 import BeautifulSoup


from pytesseract import image_to_string

caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}


options = Options()
options.add_argument('--headless')
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-infobars')
options.add_argument("--disable-extensions")
options.add_experimental_option('w3c', False)
driver = Chrome(options=options,desired_capabilities = caps)


def process_browser_log_entry(entry):
    response = loads(entry['message'])['message']
    return response
    


driver.get('https://temp-mail.org')
email = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/form/div[1]/div/input')
email.screenshot('email.png')
text = image_to_string('email.png')
print(f"Your temporary email is {text} ")

while True:
	try:
		browser_log = driver.get_log('performance') 
		events = [process_browser_log_entry(entry) for entry in browser_log]
		events = [event for event in events if 'Network.response' in event['method']]
		url = events[-1]['params']['response']['url']
		if 'https://api4.temp-mail.org/request/mail/id/' in  url:
			#print(events[-1]['params']['response']['url'])
			break
		
	except:
		sleep(3)
		print("Error")

driver.quit()
while True:
	r = get(url)
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
		
		data = {	'createdAt':createdAt,
					'mail_from':mail_from,
					'mail_subject':mail_subject,
					'mail_text_only':mail_text_only,
					'mail_text':mail_text,
					'mail_attachments_count':mail_attachments_count,
					'mail_attachments':mail_attachments
		}
		print(f"createdAt:{createdAt}\nmail_from:{mail_from}\nmail_subject:{mail_subject}\nmail_text_only:{mail_text_only}\nmail_text:{mail_text}\nmail_attachments_count:{mail_attachments_count}\nmail_attachments:{mail_attachments}")
		#print(dumps(data, sort_keys=True, indent=4))
	input("Press Any Key to refresh or Control + C to stop")
	
