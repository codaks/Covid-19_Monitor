from django.shortcuts import render,redirect
import string
import random
import json
from .models import LabsLogin
# Create your views here.

def user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = LabsLogin.objects.get(user_name=username,password=password)
            if user is not None:
                x =  '{ "username":"'+username+'", "lab_name":"'+user.lab_name+'", "email":"'+user.email_id+'", "zipcode":"'+str(user.zipcode)+'"}'
                '''x = {
                    "username": username,
                    "lab_name": user.lab_name,
                    "email": "New York",
                    "zipcode": str(user.zipcode)
                }
                '''
                # convert into JSON:
                y = json.loads(x)

                print("------------------TYPE:",type(y))
                request.session['lab'] = y
                return redirect("covid-19/dashboard")
            else:
                return redirect("user")
        except LabsLogin.DoesNotExist:
            return redirect("login")
    else:
        return render(request,"users/login.html")

def home(request):
    return redirect("/user")

def register(request):
    if request.method == "POST":
        email = request.POST['email']
        lab = request.POST['labname']
        zipcode = request.POST['zipcode']
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^*"
        username = ''.join((random.choice(letters) for i in range(10)))
        password = ''.join((random.choice(letters) for i in range(18)))
        lab_login_data = LabsLogin()

        while LabsLogin.objects.filter(user_name=username).exists():
            username = ""
            username = ''.join((random.choice(letters) for i in range(10)))
        
        lab_login_data.user_name = username
        lab_login_data.password = password
        lab_login_data.email_id = email
        lab_login_data.zipcode = zipcode
        lab_login_data.lab_name = lab
        lab_login_data.save()
        print("ID Created:")
        return redirect("/register")
    else:
        return render(request,"users/register.html")