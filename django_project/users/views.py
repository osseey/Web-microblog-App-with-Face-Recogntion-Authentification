from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from django.contrib.auth import views as auth_views
import os
from django.urls import path, include
import face_recognition
import cv2 
from PIL import Image
import numpy as np
from django.shortcuts import render
from blog.models import Post
from users.forms import LoginForm
import users
from django.contrib.auth import authenticate, login
#from django.contrib.auth import views as auth_views
import os
from django.contrib.auth.models import User

from pathlib import Path
import os
import smtplib
import imghdr
from email.message import EmailMessage
from django.core.mail import send_mail

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


EMAIL_HOST_USER = 'xfactblog@gmail.com'#'xfactblog@gmail.com'
EMAIL_HOST_PASSWORD = 'zufkgdtrsjesjqoz'#jbsomrrukejlujgj'

def capture():
	cam = cv2.VideoCapture(0)   # 0 -> index of camera
	s, img = cam.read()
	if s:    # frame captured without any errors
		cv2.namedWindow("cam-test")
		cv2.imshow("cam-test",img)
		#cv2.waitKey(0)
		cv2.destroyWindow("cam-test")
		cv2.imwrite("filename2.jpg",img)



# initialize the camera
def facedect(loc):
	gamma=0.7
	cam = cv2.VideoCapture(0)   # 0 -> index of camera
	s, img = cam.read()
	if s:    # frame captured without any errors
		cv2.namedWindow("cam-test")
		cv2.imshow("cam-test",img)
		#cv2.waitKey(0)
		cv2.destroyWindow("cam-test")
		cv2.imwrite("filename2.jpg",img)

		#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		#MEDIA_ROOT =os.path.join(BASE_DIR,'pages')

		print(MEDIA_ROOT,loc)
		loc=(str(MEDIA_ROOT)+loc)
		print(loc)
		#print("/home/light/codes/web/djangoproject/mysite/pages/media/profil_images/IMG_20180330_1600482-01.jpg")
		face_1_image = face_recognition.load_image_file(loc)
		face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
		lookUpTable = np.empty((1,256), np.uint8)
		for i in range(256):
			lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
		res = cv2.LUT(img, lookUpTable)
		cv2.imwrite("test4.jpg",res)

		#

		small_frame = cv2.resize(res, (0, 0), fx=0.25, fy=0.25)

		rgb_small_frame = small_frame[:, :, ::-1]

		lookUpTable = np.empty((1,256), np.uint8)
		for i in range(256):
			lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
		res = cv2.LUT(rgb_small_frame, lookUpTable)
		cv2.imwrite("test2.jpg",res)

		face_locations = face_recognition.face_locations(res)
		face_encodings = face_recognition.face_encodings(res, face_locations)


		check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)
		top,right, bottom, left= (face_recognition.face_locations(res))[0]
		face_image=res[top:bottom,left:right]
		pil_image= Image.fromarray(face_image)
		pil_image.save("face2.jpg")
		
		
		print(check)
		if check[0]:
			return True

		else :
			return False 
	  

def mailing(message_text, contacts, name_file):

	msg = EmailMessage()
	msg['Subject'] = 'Failed attempt to authenticate!!!'

	msg['From'] = 'xfactblog@gmail.com'
	msg['To'] = ', '.join(contacts)

	msg.set_content(message_text)

	with open(name_file,'rb') as f:
		file_data=f.read()
		file_type=imghdr.what(f.name)
		file_name=f.name
	msg.add_attachment(file_data,maintype='image', subtype=file_type, filename=file_name)


	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
	    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
	    smtp.send_message(msg)









# Create your views here.
def register(request):
	return render(request,'users/register.html', {'title': 'Register'})


def login2(request):
	contacts = ['jshoescover@gmail.com']
	if request.method =="POST":
		form =LoginForm(request.POST)
		if form.is_valid():
			username=request.POST['username']
			password=request.POST['password']
			#message=' an unknown person (capture) tried to access '+username+' account on XFact Blog. This mail is send to inform you of the failed authentification attempt!!!'
			user = authenticate(request,username=username,password=password)
			
			if user is not None:
				if facedect('/profile_pics/'+username+'.jpg'):#/profile_pics/Josepha_3.jpg'):#user.userprofile.head_shot.url):
					login(request,user)
					messages.success(request, f'You have been successfully logged in!')
				else:
					mail=user.email
					contacts.append(mail)
					name_file='filename.jpg'
					message_text='An unknown person (capture) tried to log in '+username+' account on XFact Blog but failed the second factor authentification by Face Recognition. This mail is send to inform you of the failed authentification attempt!!!'
					mailing(message_text, contacts,name_file)
				return redirect('profile')
			else:
				capture()
				name_file='filename2.jpg'
				messages.error(request, f'Your login attempt has failed! If you forgot your login informations, please refer to the admin!!!')
				message_text='An unknown person (in the attached capture) tried to log in '+username+' account on XFact Blog but failed the first factor authentification by Username & Password. This mail is send to inform you of the failed authentification attempt!!!'
				mailing(message_text, contacts,name_file)
				return redirect('register')        
	else:
		MyLoginForm = LoginForm()
		return render(request,"users/login.html",{"MyLoginForm": MyLoginForm}) 










@login_required
def profile(request):

	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
        
		if u_form.is_valid() :
			u_form.save()
            
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
     

	context = {
        'u_form': u_form
    }

	return render(request, 'users/profile.html', context)
