sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get autoremove -y
sudo apt-get autoclean -y
wget -O - https://apt.enpass.io/keys/enpass-linux.key | apt-key add -F
sudo apt-get install -y enpass ansible
