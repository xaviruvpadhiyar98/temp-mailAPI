# temp-mailAPI
Python File For Temp Mail on Terminal 

#Step To Install
pip3 install -r requriements.txt 

#Install Chromedriver of same version as chrome
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver

#Installation of Tesseract
sudo apt install tesseract-ocr


#Running the File 
python3 temp-mail.py 
