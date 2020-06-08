"""
This can be run only the first time, but recommended to run every time. 
Chrome may use some tracking ID which would be deleted if it gets removed.

How to run:

  bash requirements_gcp.sh 

"""

sudo apt update
yes "y" | sudo apt install software-properties-common

# remove Chrome dependancies
rm -rf ~/.config/google-chrome/
rm -rf ~/.cache/google-chrome/ 
rm -rf ~/.config/chromium
rm -rf /usr/bin/google-chrome
rm -rf /usr/bin/google-chrome@
rm -rf /usr/bin/google-chrome-stable
rm -rf /usr/bin/google-chrome-stable@ 
sudo apt-get purge google-chrome
sudo apt-get purge chromium-chromedriver
rm -rf /usr/bin/chromedriver 

# download chromedriver
# wget https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip

# unzip chromedriver_linux64.zip
version=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -qP "/tmp/" "https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip"
sudo apt -f install
sudo apt install zip
sudo apt install unzip
sudo unzip -o /tmp/chromedriver_linux64.zip -d /usr/bin

rm chromedriver_linux64.zip
# sudo mv chromedriver /usr/bin

# download chrome
sudo apt -f install
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
yes "y" | sudo apt --fix-broken install
sudo apt install google-chrome-stable # this one says package not available but referred to by another package. 
rm google-chrome-stable_current_amd64.deb

# To install python/pip requirements - FIRST TIME
yes "y" | sudo apt -f install
yes "y" | sudo apt install python3-setuptools
yes "y" | sudo apt install curl
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
yes "y" | sudo apt install python3-pip
echo "export PATH=$PATH:$HOME/.local/bin" > ~/.profile
source ~/.profile
echo "export PATH=$PATH:/usr/bin/chromedriver" > ~/.profile
source ~/.profile
rm get-pip.py
sudo apt update
pip install -r requirements.txt
