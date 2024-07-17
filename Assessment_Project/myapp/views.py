from django.shortcuts import render
from .models import User,Patient
import requests
import random

# Create your views here.
def index(request):
	return render(request,'index.html')

def contact(request):
	return render(request,'patient-contact.html')

def doctor(request):
	return render(request,'patient-doctor.html')

def about(request):
	return render(request,'patient-about.html')

def service(request):
	return render(request,'patient-service.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'login.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password'],
					profile_picture=request.FILES['profile_picture'],
					usertype=request.POST['usertype'],
					)
				msg="User Registered Successfully"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="Password and Confirm New Password does not Match"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_picture']=user.profile_picture.url
				if user.usertype=="doctor":
					return render(request,'index.html')
				else:
					return render(request,'patient-index.html')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email not Registered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_picture']
		msg="User Logged Out Successfully"
		return render(request,'login.html',{'msg':msg})
	except:
		msg="User Logged Out Successfully"
		return render(request,'login.html',{'msg':msg})

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_picture=request.FILES['profile_picture']
		except:
			pass
		user.save()
		request.session['profile_picture']=user.profile_picture.url
		msg="Profile Updated Successfully"
		if user.usertype=="doctor":
			return render(request,'profile.html',{'user':user,'msg':msg})
		else:
			return render(request,'patient-profile.html',{'user':user,'msg':msg})
	else:
		if user.usertype=="doctor":
			return render(request,'profile.html',{'user':user})
		else:
			return render(request,'patient-profile.html',{'user':user})

def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				if request.POST['old_password']!=request.POST['new_password']:
					user.password=request.POST['new_password']
					user.save()
					del request.session['email']
					del request.session['fname']
					del request.session['profile_picture']
					msg="Password Changed Successfully"
					return render(request,'login.html',{'msg':msg})
				else:
					msg="Old Password and New Password Can't be Same"
					if user.usertype=="doctor":
						return render(request,'change-password.html',{'msg':msg})
					else:
						return render(request,'patient-change-password.html',{'msg':msg})
			else:
				msg="New Password & Confirm New Password Does not Match"
				if user.usertype=="doctor":
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'patient-change-password.html',{'msg':msg})
		else:
			msg="Old Password does not Match"
			if user.usertype=="doctor":
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'patient-change-password.html',{'msg':msg})
	else:
		if user.usertype=="doctor":
			return render(request,'change-password.html')
		else:
			return render(request,'patient-change-password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(mobile=request.POST['mobile'])
			mobile=request.POST['mobile']
			otp=str(random.randint(1000,9999))
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"rWEmNPYvC6FzQ72fu8RqkwBeI3d5Z9UxKDVpMt1GihHAXoOl4cXkATcQySg8G1LdzUKwoPrFMNCR5v3j","message":"OTP "+otp,"language":"english","route":"q","numbers":mobile}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			print(response.text)
			print("OTP :",otp)
			request.session['otp']=otp
			request.session['mobile']=mobile
			return render(request,'otp.html')
		except:
			msg="Mobile Number not Registered"
			return render(request,'forgot-password.html',{'msg':msg})
	else:
		return render(request,'forgot-password.html')

def verify_otp(request):
	otp1=int(request.POST['otp'])
	otp2=int(request.session['otp'])
	if otp1==otp2:
		del request.session['otp']
		return render(request,'new-password.html')
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'msg':msg})

def new_password(request):
	if request.POST['new_password']==request.POST['cnew_password']:
		user=User.objects.get(mobile=request.session['mobile'])
		user.password=request.POST['new_password']
		del request.session['mobile']
		user.save()
		msg="Password Changed Successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="Password & Confirm New Password does not Match"
		return render(request,'new-password.html',{'msg':msg})

def doctor_single(request):
	return render(request,'patient-doctor-single.html')

def appointment(request):
	if request.method=="POST":
		try:
			Patient.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'appointment.html',{'msg':msg})
		except:
			if request.POST['email']==request.POST['email']:
				Patient.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					message=request.POST['message'],
					doctortype=request.POST['doctortype'],
					)
				msg="Appointment Registered Successfully"
				return render(request,'appointment.html',{'msg':msg})
			else:
				msg="Appointment Not Registered"
				return render(request,'appointment.html',{'msg':msg})
	else:
		return render(request,'appointment.html')
