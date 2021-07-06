from flask import Flask, render_template, flash, request,session,redirect, jsonify  # for FLASK connection
import cv2  # to store face capture image and video
import numpy as np # for image arrays
import json  # to store data in json file
from PIL import ImageGrab # to send image on telegram
import io  # to handle io
import requests  # For handling server and client requests
import time  # For time related functions
from flask_mail import Mail, Message  # To send mail
from datetime import date, datetime # For date & time related functions
import simplejson # to retreive credentials from json file
import json # to retreive credentials from json file
import os  # to send Whatsapp message
from twilio.rest import Client # to send Whatsapp message

app = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''       # replace with your own email ID
app.config['MAIL_PASSWORD'] = ''      # replace with your own password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key='12345678'

@app.route('/')
def index():
	session['tries']=0
	return render_template('mine.html')

@app.route('/auth',methods = ['GET' ,'POST'])
def video_feed1():
	with open("data.json") as e:
		k = json.load(e)	

	if request.method=='POST':
		
		print(str(request.remote_addr))
		url = request.form["username"]
		pwd = request.form["psw"]
		if (url==k["username1"] and pwd ==k["password1"]):
			print("\n\nUSER: ",url, "has logged in succesfully...\nRedirected to the requested url\n\n")
			return render_template('successful.html')
		else :
			honeypot_start_time = time.time();	
			session['tries']=session['tries']+1
			if session['tries'] == 1:
				print("\n\nUSER: ",url, "has entered a wrong password once.\nPassword entered: ", pwd, "\n2 more attempts remaining.\n\n")
				flash(u'Invalid password provided - 2 more attempts remaining', 'error')
			elif session['tries'] == 2:
				print("\n\nUSER: ",url, "has entered a wrong password twice.\nPassword entered: ", pwd, "\n1 more attempt remaining.\n\n")
				flash(u'Invalid password provided - 1 more attempt remaining', 'error')

			if session['tries']>=3:
				print("\n\nUSER: ",url, "has entered a wrong password thrice.\nPassword entered: ", pwd)
				print("\n\nIntruder has been captured. Real-time honeypot activated in backend.....")

				print("\nFace capture of intruder initiated...\n")
				
				# Face capture
				cam = cv2.VideoCapture(0)
				frame=None
				while (True):
					ret, frame = cam.read()
					if (ret):
						break
				cv2.imwrite("C:/Users/ASUS/Desktop/honeypot-project/ss_webcam/Intruder-RealTime-Capture.png",frame)	
				cv2.imwrite("C:/xampp/htdocs/honeypot-whatsapp/Intruder-RealTime-Capture.png",frame)	
				cv2.destroyAllWindows()
				
				# screenshot
				print("\nFace capture successful and saved in the system....\n")


				# Store IP address and other details from JSON 
				print("\nCapturing IP address and other details of the intruder's system....\n")
				url = "http://ipinfo.io" 
				try:
						uResponse = requests.get(url)
				except requests.ConnectionError:
					return "Connection Error"  
				Jresponse = uResponse.text
				data = json.loads(Jresponse)

				ip = data['ip']
				city = data['city']
				country = data['country']
				location = data['loc']
				organisation = data['org']
				region = data['region']
				# hostname = data['hostname']
				print("\nIP address, location, address captured successfully....\n")
				# IP address captured - end

				# Date and Time - start
				today1 = date.today()
				d1 = today1.strftime("%B %d, %Y")
				time_now1 = datetime.now()
				t1 = time_now1.strftime("%H:%M:%S")
				# Date and Time - end 

				#whatsapp-start
				print("\nSending message to Akshit Sawnani's Whatsapp: +91 7230053300....")
				
				text_body = "*Intruder/ Hacker details:* "
				text_body += "\n\n*IP Address of the location* where intruder is present: " + ip
				text_body += "\n\n*City:* " + city + "\n\n*Country:* " + country + "\n\n*Location Coordinates:* " + location
				text_body += "\n\n*Organisation:* " + organisation + "\n\n*Region:* " + region # + "\n\n*Host Name:* " + hostname
				text_body += "\n\nThis was just to inform you that someone was trying to hack into your organisation.\n\nThank you,\nHONEYPOT REAL-TIME IMPLEMENTATION"

				account_sid = 'AC764e1ce2c84b71af9661d5b477476497' #generate your own account_ssid and add here
				auth_token = '94055e26d4eafaf8987f02f200b79cd4'  #generate your own auth_token and add here
				client = Client(account_sid, auth_token)

				message = client.messages.create( from_='whatsapp:+14155238886', body='*INTRUDER ALERT!*\nThere is an Intruder who is trying to hack in to the organization.\n\n*Date of attack:* ' + d1 +'\n*Time of attack:* ' + t1 + '\n\nHere are the details: ',
												to='whatsapp:+917230053300')
				message = client.messages.create( from_='whatsapp:+14155238886', body=text_body,
												to='whatsapp:+917230053300')
				message = client.messages.create( from_='whatsapp:+14155238886', body='*Real-time Captures (Image and Video)* of the hacker have been *mailed* to \n*akshitexam@gmail.com*, \nalong with the above details.',
												to='whatsapp:+917230053300')
				message = client.messages.create( from_='whatsapp:+14155238886', body='*Real-time keylogger screenshots* of the intruder\'s system have been sent to you on *Telegram.*',
												to='whatsapp:+917230053300')
				message = client.messages.create( from_='whatsapp:+14155238886', body='*Intruder Face Capture*',
					media_url = "http://308686771f1e.ngrok.io/honeypot-whatsapp/Intruder-RealTime-Capture.png",
					to='whatsapp:+917230053300')	#replace with ngrok url and your own phone number
				message = client.messages.create( from_='whatsapp:+14155238886', body='Intruder detected and captured successfully\n\nThank you,\nReal-time Honeypot System',
												to='whatsapp:+917230053300') #replace with your own phone number 

												
				print("\nWhatsapp messages sent successfully...\nMessage ID:" + message.sid +"\n")
				#whatsapp - end


				#telegram - start
				for i in range(1,6):
					im = ImageGrab.grab()  # Taking system screenshot
					if im is None:
						print("Error Occured")
					else:
						img_byte_arr = io.BytesIO()						
						im.save(img_byte_arr, format='PNG')
						img_byte_arr = img_byte_arr.getvalue()

						# GROUP ID
						response = requests.post("https://api.telegram.org/bot1759404630:AAG2aDpZQM3HlNaMgYnG-uopwf8vuta3Deo/sendPhoto?chat_id=-571834323", files={"photo": img_byte_arr}, data={"caption": "INTRUDER REAL TIME SCREENSHOT"})
						
						# MY BOT ID
						response = requests.post("https://api.telegram.org/bot1759404630:AAG2aDpZQM3HlNaMgYnG-uopwf8vuta3Deo/sendPhoto?chat_id=925839626", files={"photo": img_byte_arr}, data={"caption": "INTRUDER REAL TIME SCREENSHOT"})
						# responsealt = requests.post("https://api.telegram.org/bot1759404630:AAG2aDpZQM3HlNaMgYnG-uopwf8vuta3Deo/sendPhoto?chat_id=925839626", files={"photo": "/Applications/XAMPP/xamppfiles/htdocs/honeypot-whatsapp/Intruder-RealTime-Capture.png"}, data={"caption": "INTRUDER face capture"})

						# akshit_bot 
						# response3 = requests.post("https://api.telegram.org/bot1700733646:AAFVWxGcdkOxZ3GgAqffoCgLHKFvqwnE82A/sendPhoto?chat_id=-589847408", files={"photo": img_byte_arr}, data={"caption": "INTRUDER REAL TIME SCREENSHOT"})
						# response4 = requests.post("https://api.telegram.org/bot1700733646:AAFVWxGcdkOxZ3GgAqffoCgLHKFvqwnE82A/sendPhoto?chat_id=-501152227", files={"photo": img_byte_arr}, data={"caption": "INTRUDER REAL TIME SCREENSHOT"})	
						# response5 = requests.post("https://api.telegram.org/bot1759404630:AAG2aDpZQM3HlNaMgYnG-uopwf8vuta3Deo/sendPhoto?chat_id=925839626", files={"photo": img_byte_arr2}, data={"caption": "INTRUDER PHOTO CAPTURE"})

						print("\nSending Image#",i," on telegram....Response Status code: ", response.status_code)

						if response.status_code != 200:
							print(response.json())
							print("sent image")
						
						print("\nSent the Intruder's screen capture image#",i," on TELEGRAM...\n")
				# telegram - ends


				# Date and Time - start
				today = date.today()
				d = today.strftime("%B %d, %Y")
				time_now = datetime.now()
				t = time_now.strftime("%H:%M:%S")
				time_start_mail = time.time()
				print("\n\nSending Mail to Akshit Sawnani's gmail account....\non date:", d + " at time: " + t)
				# Date and Time - end 

				# Send Mail - start
				msg = Message('HONEYPOT REAL-TIME INTRUDER ALERT on ' + d + ' at ' + t, sender = 'akshitexam@gmail.com', recipients = ['akshitexam@gmail.com'])
				# msg.add_recipient("other_email_id_may_be_entered")

				# send face capture, videos and system screenshots ---> through mail attachments
				with app.open_resource("C:/Users/ASUS/Desktop/honeypot-project/ss_webcam/Intruder-RealTime-Capture.png") as fp:  
        				msg.attach("Intruder-RealTime-Capture.png","image/png",fp.read())  
				with app.open_resource("C:/xampp/htdocs/honeypot-whatsapp/screen-capture-1.jpg") as fp:  
        				msg.attach("screen-capture-1.jpg","image/jpg",fp.read())  
				with app.open_resource("C:/xampp/htdocs/honeypot-whatsapp/screen-capture-2.jpg") as fp:  
        				msg.attach("screen-capture-2.jpg","image/jpg",fp.read())  
				with app.open_resource("C:/xampp/htdocs/honeypot-whatsapp/screen-capture-3.jpg") as fp:  
        				msg.attach("screen-capture-3.jpg","image/jpg",fp.read())  
				
				# send face capture, videos and system screenshots ---> embedded inline mail
				with open('C:/Users/ASUS/Desktop/honeypot-project/ss_webcam/Intruder-RealTime-Capture.png', 'rb') as fp:
    					msg.attach('Intruder-RealTime-Capture.png', 'image/png', fp.read(), 'inline', headers=[['Content-ID','<pic>']])
				with open('C:/xampp/htdocs/honeypot-whatsapp/screen-capture-1.jpg', 'rb') as fp:
    					msg.attach('screen-capture-1.jpg', 'image/jpg', fp.read(), 'inline', headers=[['Content-ID','<ss1>']])
				with open('C:/xampp/htdocs/honeypot-whatsapp/screen-capture-2.jpg', 'rb') as fp:
    					msg.attach('screen-capture-2.jpg', 'image/jpg', fp.read(), 'inline', headers=[['Content-ID','<ss2>']])
				with open('C:/xampp/htdocs/honeypot-whatsapp/screen-capture-3.jpg', 'rb') as fp:
    					msg.attach('screen-capture-3.jpg', 'image/jpg', fp.read(), 'inline', headers=[['Content-ID','<ss3>']])
				
				msg.html = render_template('mail_content.html',ip=ip,city=city,country=country,location=location,organisation=organisation,region=region)
				mail.send(msg)
				print("\n\nMail sent successfully to akshitexam@gmail.com")
				time_end_mail = time.time()
				print("\n\nTime taken to send mail: ", int(time_end_mail-time_start_mail)," seconds\n")
				print("\n\nTOTAL TIME TAKEN for honeypot implementation: ", int(time_end_mail-honeypot_start_time)," seconds\n\n")
				
				return render_template('ip.html', data=data)
			return render_template('mine.html')

if __name__ == '__main__':
    app.run(debug=True)  