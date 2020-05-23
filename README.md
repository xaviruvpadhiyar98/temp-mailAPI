# TempMailAPI 

TempMailAPI is python file for Temporary Disposable Mails on Terminal 

## Dependecies
1. Chrome or Chromium Browser
2. ChromeDriver(Version of chromedriver and chrome browser should be same)
3. Selenium
4. Requests Module from python


## Installation

Clone the repository from github

'''bash
git clone https://github.com/xaviruvpadhiyar98/temp-mailAPI.git
cd temp-mailAPI/
pip install -r requirements.txt
'''

# Install Chromedriver of same version as chrome

wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip

unzip chromedriver_linux64.zip

sudo mv chromedriver /usr/bin/chromedriver

sudo chown root:root /usr/bin/chromedriver

sudo chmod +x /usr/bin/chromedriver



#Installation of Tesseract

sudo apt install tesseract-ocr




#Running the File

python3 temp-mail.py 


