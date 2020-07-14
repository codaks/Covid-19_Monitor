from django.shortcuts import render,redirect
from .models import Patients
from .models import XRayData
import datetime

import keras
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
import datetime
'''
import os
import sys
import json
import datetime
import numpy as np
import skimage.draw
from numpy import zeros
from numpy import asarray
from mrcnn.utils import Dataset
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
from numpy import expand_dims
from numpy import mean
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
from mrcnn.utils import Dataset
from mrcnn.utils import compute_ap
from mrcnn.model import load_image_gt
from mrcnn.model import mold_image 
from matplotlib import pyplot
import itertools
import colorsys
import random
import numpy as np
from skimage.measure import find_contours
import matplotlib.pyplot as plt
from matplotlib import patches,  lines
from matplotlib.patches import Polygon
from mrcnn.config import Config
from mrcnn import model as modellib, utils



import matplotlib.lines as mlines
from matplotlib.patches import Rectangle
from matplotlib.pyplot import text
import matplotlib.pyplot as plt

'''
import sys
import numpy as np
import os
import cv2
from keras.preprocessing import image
import urllib
import keras.backend.tensorflow_backend as tb
from django.core import serializers
from django.forms.models import model_to_dict
import json


# Create your views here.

#-------------------------------------------------------------------------------------------------------#
#----------------------------------------/covid/dashboard-----------------------------------------------#
#-------------------------------------------------------------------------------------------------------#
def dashboard(request):

    if request.method == "GET":
        if request.session.has_key('lab'):
            ids = request.session['lab']
            lab_id = ids['username']
            patinets  = Patients.objects.filter(lab_id=lab_id)
            patinets_data = serializers.serialize('json', patinets)
            struct = json.loads(patinets_data)
            patinets_data = struct
            active  = []
            death = []
            recovered = []
            request.session['patients_data'] = patinets_data
            if len(patinets_data) == 0:

                request.session['total_cases'] = 0
                request.session['active'] = 0
                request.session['recovered'] = 0
                request.session['death'] = 0
                request.session['patients_data'] = patinets_data
                return render(request, 'dashboard/index.html', {
                    
                'lab_data':request.session['lab'],
                'active' :active[:6],
                'recover':recovered[:6],
                'death':death[:6],
                'act': 0,
                'total': 0,
                'rec': 0,
                'dth': 0
                })

            for data in patinets_data:
                if data['fields']['status'] == "Active":
                    data['fields']['id'] = data['pk']
                    active.append(data['fields'])
                elif data['fields']['status'] == "Recover":
                    data['fields']['id'] = data['pk']
                    recovered.append(data['fields'])
                elif data['fields']['status'] == "Death":
                    data['fields']['id'] = data['pk']
                    death.append(data['fields'])

                request.session['patients_data'] = patinets_data
                request.session['total_cases'] = len(active)+len(death)+len(recovered)
                request.session['active'] = len(active)
                request.session['recovered'] = len(recovered)
                request.session['death'] = len(death)
            return render(request, 'dashboard/index.html', {
                'lab_data':request.session['lab'],
                'active' :active[:6],
                'recover':recovered[:6],
                'death':death[:6],
                'act':request.session['active'],
                'total':request.session['total_cases'],
                'rec':request.session['recovered'],
                'dth':request.session['death']
            })
        else:
            return redirect("/user")
    else:
        search = request.POST['search']
        
        return redirect("/covid-19/dashboard/{{search}}/profile")
        

#-------------------------------------------------------------------------------------------------------#
#-----------------------------------/covid/dashboard/register-------------------------------------------#
#-------------------------------------------------------------------------------------------------------#
def register(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        dbo = request.POST['DOB']
        address = request.POST['address']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        pnum = request.POST['pnum']
        diseases = request.POST.getlist('diseases[]')
        gender = request.POST.get('gender')
        lab_id = request.session['lab']
        lab_id = lab_id['username']
        dis = ""
        for i in diseases:
            dis += i+" "
        dbo = str(dbo)
        dbo = dbo.split("/")
        dbo = dbo[2]+"-"+dbo[0]+"-"+dbo[1]
        diseases = dis
        patient = Patients()
        patient.first_name = fname
        patient.last_name = lname
        patient.date_of_birth = dbo
        patient.address = address
        patient.state = state
        patient.zipcode = zipcode
        patient.prev_dess = diseases
        patient.phone_no = int(pnum)
        patient.Gender = gender
        patient.lab_id = lab_id
        patient.save()
        return redirect("/covid-19/dashboard")

    else:
        if request.session.has_key('lab'):

            return render(request,"patients/register.html",
            {
                'act':request.session['active'],
                'total':request.session['total_cases'],
                'rec':request.session['recovered'],
                'dth':request.session['death'],
                'lab_data':request.session['lab']
            })
        else:
            return redirect("/")


#-------------------------------------------------------------------------------------------------------#
#----------------------------------------/covid/dashboard-----------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

def x_rayAnaluzier(request,question_id):
    if request.method == "POST":
        data = request.FILES['fileUpload']
        tb._SYMBOLIC_SCOPE.value = True
        image =  _grab_image(stream=request.FILES["fileUpload"])
        res = validateImage(image)

        if res != "xray":
            request.session['output'] = "Not A Valid X-Ray"
            return redirect("/covid-19/dashboard")
        classifier=Sequential()
        #adding convulation layer pooling

        classifier.add(Conv2D(64,(3, 3), input_shape = (152, 152, 3), activation = 'relu',padding = 'same'))
        classifier.add(MaxPooling2D(pool_size=(2,2)))


        # Adding a second convolutional layer
        classifier.add(Conv2D(64, (3, 3), activation = 'relu',padding = 'same'))
        classifier.add(MaxPooling2D(pool_size = (2, 2)))


        classifier.add(Conv2D(64, (3, 3), activation = 'relu',padding = 'same'))
        classifier.add(MaxPooling2D(pool_size = (2, 2)))


        classifier.add(Conv2D(64, (3, 3), activation = 'relu'))
        classifier.add(MaxPooling2D(pool_size = (2, 2)))


        #flattening

        #-----------------Old: weights-17-0.91.hdf5--------------#
        classifier.add(Flatten())

        classifier.add(Dense(units=228,activation='relu'))
        classifier.add(Dropout(0.2))
        classifier.add(Dense(units=128,activation='relu'))
        classifier.add(Dropout(0.2))

        classifier.add(Dense(units=98,activation='relu'))
        classifier.add(Dense(units=2,activation='softmax'))


        '''
        #-----------------New: weights-20-0.98.hdf5--------------#

        classifier.add(Flatten())
        classifier.add(Dense(units=128,activation='relu'))
        classifier.add(Dropout(0.2))
        classifier.add(Dense(units=98,activation='relu'))
        classifier.add(Dropout(0.2))
        #classifier.add(Dense(units=48,activation='relu'))

        classifier.add(Dense(units=2,activation='softmax'))'''

        classifier.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
        '''
            New: weights-20-0.98.hdf5;
            Old: weights-17-0.91.hdf5;
        '''
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(BASE_DIR,'templates/patients/weights-20-0.98.hdf5')
        path = str(path)
        classifier.load_weights(path)
        labels_name={0:"Covid-19" ,1:"Normal"}
        

        Xlst=[]
        input_img=image
        input_img_resize = cv2.resize(input_img,(152,152))
        Xlst.append(input_img_resize)
        test_image = np.array(Xlst)
        test_image = test_image.astype('float32')
        test_image /= 255
        b=classifier.predict(test_image)
        k=np.argmax(b)
        label = labels_name[k]
        acc = round(b[0][k]*100, 2)
        
        x_ray_object  = XRayData()
        x_ray_object.status = label
        x_ray_object.img = request.FILES['fileUpload']
        x_ray_object.accuracy = acc
        x_ray_object.sacnned_img = sacnned_image
        x_ray_object.bed_no = question_id
        x_ray_object.save()
        return redirect("/covid-19/dashboard/"+str(question_id)+"/profile")
    else:
        if request.session.has_key('lab'):
            redirect("/user")
        return render(request,"patients/x-rayAnalizer.html",{
            'act':request.session['active'],
            'total':request.session['total_cases'],
            'rec':request.session['recovered'],
            'dth':request.session['death'],
            'lab_data':request.session['lab']
        })


#-------------------------------------------------------------------------------------------------------#
#------------------------------------/covid/dashboard/prfile--------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

def profile(request,question_id):
    if request.session.has_key('lab'):
        patients_data = request.session['patients_data']
        lab_id = request.session['lab']['username']

        for data in patients_data:
            if data['fields']['id'] == question_id and lab_id == data['fields']['lab_id']:
                day = data['fields']['admit_time'].split("T")[0].split("-")[2]
                mnth = data['fields']['admit_time'].split("T")[0].split("-")[1]
                yr = data['fields']['admit_time'].split("T")[0].split("-")[0]
                date = yr+"-"+mnth+"-"+day
                date_format = "%Y-%m-%d"
                c_date = datetime.date.today()
                date = datetime.date(int(yr),int(mnth),int(day))
                no_of_days = (c_date - date).days
                
                xray_data = XRayData.objects.filter(bed_no = question_id).order_by('-date_time')
                xray_data = serializers.serialize('json', xray_data)
                xray_data = json.loads(xray_data)

                
                return render(request,"patients/profile.html",{
                    'lab_data':request.session['lab'],
                    'act':request.session['active'],
                    'total':request.session['total_cases'],
                    'rec':request.session['recovered'],
                    'dth':request.session['death'],
                    'data' :data['fields'],
                    'days' :no_of_days,
                    'xray':xray_data,
                    'length' : len(xray_data)
                })
        return redirect("/covid-19/dashboard")
    return redirect("/user")


#-------------------------------------------------------------------------------------------------------#
#------------------------------------/covid/dashboard/deadUpdate--------------------------------------------#
#-------------------------------------------------------------------------------------------------------#
def dead(request,question_id):
    if request.method == "POST":
        patient = Patients.objects.get(pk = question_id)
        patient.status = "Death"
        patient.save()
        patient_data = request.session['patients_data']
        for data in patient_data:
            if(data['pk'] == question_id):
                data['fields']['status'] = "Death"
                break
        request.session['patients_data'] = patient_data
        return redirect("/covid-19/dashboard/"+str(question_id)+"/profile")
        

#-------------------------------------------------------------------------------------------------------#
#------------------------------------/covid/dashboard/recoverUpdate--------------------------------------------#
#-------------------------------------------------------------------------------------------------------#
def recovered(request,question_id): 
    if request.method == "POST":
        patient = Patients.objects.get(pk = question_id)
        patient.status = "Recover"
        patient.save()
        patient_data = request.session['patients_data']
        for data in patient_data:
            if(data['pk'] == question_id):
                data['fields']['status'] = "Recover"
                break
        request.session['patients_data'] = patient_data
        return redirect("/covid-19/dashboard/"+str(question_id)+"/profile")
    

#-------------------------------------------------------------------------------------------------------#
#-----------------------------------------/covid/logout-------------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

def logout(request):

    del request.session['patients_data'] 
    del request.session['total_cases'] 
    del request.session['active'] 
    del request.session['recovered'] 
    del request.session['death'] 
    del request.session['lab']
    

    return redirect('/user')



def patientList(request):
    patients_data = request.session['patients_data']

    return render(request,"patients/list.html",{
        'Patients' : patients_data
    })


#---------------------------------------------------------------------------------------------------#
#--------------------------Conversion of POST object into an open cv object-------------------------#
#---------------------------------------------------------------------------------------------------#

def _grab_image(path=None, stream=None, url=None):
    
	if path is not None:
		image = cv2.imread(path)
	else:	
        
		if url is not None:
			resp = urllib.urlopen(url)
			data = resp.read()

		# if the stream is not None, then the image has been uploaded
		elif stream is not None:
			data = stream.read()


		# convert the image to a NumPy array and then read it into
		# OpenCV format
		image = np.asarray(bytearray(data), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image

def search(request):
    return redirect("/covid-19/dashboard/patients")

def validateImage(image):
    classifier=Sequential()
    #adding convulation layer pooling

    classifier.add(Conv2D(64,(3, 3), input_shape = (152, 152, 3), activation = 'relu',padding = 'same'))
    classifier.add(MaxPooling2D(pool_size=(2,2)))


    # Adding a second convolutional layer
    classifier.add(Conv2D(64, (3, 3), activation = 'relu',padding = 'same'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))


    classifier.add(Conv2D(64, (3, 3), activation = 'relu',padding = 'same'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))


    classifier.add(Conv2D(64, (3, 3), activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))


    #flattening

    #flattening
    classifier.add(Flatten())

    classifier.add(Dense(units=128,activation='relu'))

    classifier.add(Dense(units=48,activation='relu'))

    classifier.add(Dense(units=2,activation='softmax'))

    classifier.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR,'templates/patients/weights-01-0.96.hdf5')
    path = str(path)
    classifier.load_weights(path)
    labels_name={0:"xray" ,1:"normal"}

    Xlst=[]
    input_img=image
    input_img_resize = cv2.resize(input_img,(152,152))
    Xlst.append(input_img_resize)
    test_image = np.array(Xlst)
    test_image = test_image.astype('float32')
    test_image /= 255
    b=classifier.predict_classes(test_image)

    label = labels_name[b[0]]
    return label 

##################################################################################################################
################################################################################################################## 
##################################################################################################################   
