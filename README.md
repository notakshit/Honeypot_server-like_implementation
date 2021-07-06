# Honeypot_server-like_implementation
Implementation of Honeypot-based Security Approach for Real-Time Intrusion Detection and Prevention

Before executing the project, follow these steps first –

Download XAMPP server - https://www.apachefriends.org/download.html
Open XAMPP and Switch on the Apache Web Server (default port 80)

Download ngrok (tunneling localhost to a public url) - https://ngrok.com/download
Save the ngrok Unix executable file in Downloads folder

Open terminal, type the following commands (to send face captures through whatsapp)
cd Downloads 
./ngrok http 80

Change paths in the app.py file wherever required (according to where you have stored the folder in your system – here, the folder was saved on desktop)

# For setting WhatsApp alerts: In the file app.py, add the ngrok url (generated above) and your own phone number (on which you have WhatsApp)
# Set up your twilio account – generate your own account_ssid and auth_token, and add it accordingly.

Instructions: https://www.twilio.com/docs/whatsapp/tutorial/send-and-receive-media-messages-whatsapp-python

# For setting Telegram alerts: Create your own bot on Telegram, generate the bot ID, and replace it with the api link in line 177 of the file app.py.

# For setting Email alerts – 

In app.py, lines 21 & 22, add your own email id and account password
Gmail -> Settings -> Allow “less secure app” and disable “2-Step Verification”



# Follow the below steps now –

# Instructions to Execute the Project

Download the Zip File and save folder to desktop 
Folder name: honeypot-project

Go to terminal and type -> cd desktop/honeypot-project

Build the virtual environment
pip install virtualenv
virtualenv venv
source venv/bin/activate

Pip install all the required libraries -> pip install -r requirements.txt

ls -> view all files in the given directory

Run the HashConversion.py file to enter correct set of username and password, and convert password to hash for security.

> python HashConversion.py

Enter the fields asked, remember this username and password, it is stored in data.json file

Now run the app.py file, which is the main file (flask integration)

> python app.py

Open your browser, open localhost website (default port: 5000) –
http://127.0.0.1:5000/

This will load the website, which is a login portal

Enter the correct set of username and password (which you entered earlier) for successful login.
It will automatically redirect you to VTOP (Online portal for students and faculties of my University)

Check terminal – you will see the corresponding output that “username” user has successfully logged in.

Load the portal again, this time enter wrong credentials twice. (The limitof unsuccessful attempts can be set in the app.py file)
Check terminal output -> you will see that “username” has entered the wrong password once/ twice, wrong password entered is – “xxxxxxx” and one/two more attempts are remaining. The remaining attempts message is also displayed on the website.

After 3rd unsuccessful attempt, wait for some time. Honeypot is automatically activated. Check terminal output for all knowing what all is happening in the honeypot implementation, all the real-time outputs are shown in terminal.

Go to the folder: honeypot-project/sswebcam
You will see the following two files:
Face capture: Intruder-RealTime-Capture.png
Video capture: Intruder-RealTime-Capture.mp4

Run keylogger script, to capture keystrokes
Open new terminal window, go to the project directory
sudo python key.py
(you might be asked to enter your system password)

Check the folder: honeypot-project/keylogger
Logs are stored every 20 seconds

After 1-2 minutes, check your WhatsApp, Telegram and Gmail for real-time intruder alerts. 
Date and time of attack
IP address, and other details of the intruder’s system
Screen capture
Face capture and video

Check terminal output at the end to see total time taken for execution and for sending the mail. 

Execution is successful! :)
