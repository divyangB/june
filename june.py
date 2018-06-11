#!/usr/bin/python3

import os
from gtts import gTTS    #for text to speech conversion
import speech_recognition as sr    #for speech recognition
import webbrowser as wb
import time,os
import requests
import pafy
import vlc
import cv2
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

#recognizing the voice
r = sr.Recognizer()


guide = '''
	Beware!! I am watching you :)
	1. Greet June
	2. Run a command
	3. Play a song on youtube
	4. Search something on internet(say "search+keyword")
	5. Create a note
	6. Who accesed my program in the end
	7. Motion tracker'''

#capturing the person who last accessed this program
cap = cv2.VideoCapture(0)
status,frame= cap.read()
cv2.imwrite('detected.png',frame)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cap.release()

#sending email when the program is accessed
msg = MIMEMultipart()
msg['From']="junechatbot@gmail.com"
msg['To'] = "divyang018@gmail.com"
msg['Subject'] = "ALERT!!"

with open("detected.png",'rb') as fp:
	img = MIMEImage(fp.read())
	msg.attach(img)

server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
server.login(msg['From'],"june123@#")
server.sendmail(msg['From'], msg['To'],msg.as_string())
server.quit()

#bot intro
bot_start = "Hi! I am June. How may I help you?"
tts = gTTS(text=bot_start, lang='en')
tts.save('startvoice.mp3')
os.system('mpg321 startvoice.mp3')

while True:
	os.system("clear")
	print(guide)
 	#listening through microphone 
	with sr.Microphone() as source:
		print("Say something!")	
		audio = r.listen(source)
		print("Done!")

 	#recognizing voice and taking actions accordingly
	try:
		text = r.recognize_google(audio).lower()
		text1= text.split()
		length= len(text1)
		print("You said: "+text)
		
		#--------------to greet the bot------------------------------------
		for i in range(0,length):
			if(text1[i]=='hello' or text1[i]=='hey' or text1[i]=='hi'):
				greet="hello sir!!"
				tts=gTTS(text=greet,lang='en')
				tts.save('greet.mp3')
				os.system('mpg321 greet.mp3')
			#to exit from the bot
			
		else:
			#---------searching query on web-------------------------------
			for i in range(0,length):
				if(text1[i]=='search'):
					wb.get('firefox').open('https://www.google.com/search?q='+text)
	

			#---------running a linux command------------------------------
			for i in range(0,length):
				x= os.system(text1[i])
				#opening and reading output of linux command
				cmd= os.popen(text1[i]).read()    
				if(x==0):
					inn1 = gTTS(text =cmd,lang='en')
					inn1.save("new.mp3")
					os.system("mpg321 new.mp3")

			#--------to make directories-----------------------------------
			for i in range(0,length):
				if(text1[i]=='directories' or text1[i]=='folders'):
					reply='Sure,how many directories?'
					d_text=gTTS(text=reply, lang='en')
					d_text.save("directory.mp3")
					os.system('mpg321 directory.mp3')
					with sr.Microphone() as source:
						print('Listening')
						ans = r.listen(source)
						print('OK!')
						try:
							num = int(r.recognize_google(ans))
							for i in range(1,num+1):
								os.system('mkdir dir'+str(i))
						except Exception as e:
								pass
			#--------searching songs on youtube----------------------------	
			
			#to play any song on youtube default browser firefox				
			for i in range(0,length):
				if(text1[i]=="music" or text1[i]=="song"):
					with sr.Microphone() as source:
						tts=gTTS(text="which song ",lang='en')
						tts.save('whichsong.mp3')
						os.system("mpg321 whichsong.mp3")
						audio1=r.listen(source)
						try:
							song=r.recognize_google(audio1)	
							print("...")
							page=requests.get("https://www.youtube.com/results?search_query="+str(song))
							soup=BeautifulSoup(page.text,"html.parser")
							print("...")
							s=soup.findAll("a")
							for i in s:
								if i.get('href').count('/watch')>0:
									ss="https://www.youtube.com"+str(i.get('href'))
									video=pafy.new(ss)
									best=video.getbest()
									playurl=best.url
									Instance = vlc.Instance()
									player = Instance.media_player_new()
									Media = Instance.media_new(playurl)
									Media.get_mrl()
									player.set_media(Media)
									player.play()									

									#wb.get('firefox').open_new_tab(ss)
									#os.system("cvlc "+ss)
									break
						except Exception as e:
							pass

			#if anyone has accessed this program
			for i in range(0,length):
				if(text1[i]=="open" or text1[i]=="access" or text1[i]=="axis" or text1[i]=='excess' or text1[i]=='opened'):
					reply = "Wait! Let me check"
					tts= gTTS(text=reply ,lang='en')
					tts.save('camera.mp3')
					os.system('mpg321 camera.mp3')
					#showing the saved image of the person
					try:
						img = cv2.imread('detected.png',1)
						person="This person"
						tts=gTTS(text=person, lang='en')
						tts.save('person.mp3')
						os.system('mpg321 person.mp3')
						cv2.imshow('This person',img)
						cv2.waitKey(0)
						cv2.destroyAllWindows()
					except Exception as e:
							pass
			'''
			for i in range(0,length):
				if (text1[i]=='send' and text1[i]=='email'):
					from email.mime.multipart import MIMEMultipart
					from email.mime.image import MIMEImage
					from email.mime.text import MIMEText
					import smtplib

					msg=MIMEMultipart()
			'''
									

			
					
				
			#---------for making a note-----------------------------------
			
			#for i in range(0,length):
			#	if(text1[i]=="note"):
			#		n_reply = 'do you to make a new note or do you want to play the last note?'
			#		n_ans = gTTS(text=n_reply,lang='en')
			#		n_ans.save("note.mp3")
			#		os.system('mpg321 note.mp3')
			#		with sr.Microphone() as source:
			#			print("Listening")					
			#			note_voice = r.listen(source)	

	except Exception as e:
				pass

