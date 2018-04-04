from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.utils import OperationalError
import json

import h5py
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import math
import pandas as pd
import pickle
import cv2
#from Utils import load_pkl_data
#from Utils import load_pd_data
from modules.Utils import load_pd_direct
from modules.startconvert import start_conversion

import glob
import os
import re
from shutil import rmtree


import brewer2mpl
import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from keras.models import load_model

from main.models import Document
from main.forms import DocumentForm


# Create your views here.
def home(request):
    return render(request, 'main/home.html')

@csrf_exempt
def submit(request):

    image_path = os.path.join(settings.BASE_DIR, 'static')
    image_path = os.path.join(image_path, 'images')
    #image_file = os.path.join(image_path, 'test.jpg')

    if os.path.isdir(image_path):
        rmtree(image_path)
    os.mkdir(image_path)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        newdoc = Document(docfile = request.FILES['avatar'])
        image_name = request.FILES['avatar'].name
        request.FILES['avatar'].name = 'example.jpg'
        try:
            newdoc.save()
        except OperationalError:
            pass
        #print(form.is_valid())
        #if form.is_valid():
            #newdoc = Document(docfile = request.FILES['avatar'])
            #newdoc.save()
        #for chunk in img.chunks():
            #f.write(chunk)

    #if request.method == 'POST':
    #    upload = DocumentForm(request.POST, request.FILES)
    #    print(upload.is_valid())
    #    if upload.is_valid():
    #        m = Document.objects.get(pk=course_id)
    #        m.model_pic = form.cleaned_data['image']
    #        m.save()

        # run DL algorithm on photo to produce json
    
    #print(image_file)
    #for f in glob.glob(image_path + '/*.*'):
        #image_file = f

    start_number = 1

    output_pd, error_file = start_conversion(image_path, start_number)
    #print(image_file)
    test_X, test_Y, _, _, test_file = load_pd_direct(output_pd)
    model_file = os.path.join(settings.BASE_DIR, 'model/mymodel.h5py')
    model = load_model(model_file)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    #score = model.evaluate(test_X, test_Y, verbose=0)
    #print("model %s: %.2f%%" % (model.metrics_names[1], score[1] * 100))
    y_prob = model.predict(test_X, batch_size=32, verbose=0)
    predction = y_prob[0].astype(np.float64)
    #print(predction.dtype)
    #y_pred = [np.argmax(prob) for prob in y_prob]
    #y_true = [np.argmax(true) for true in test_Y]
    #counts = np.bincount(y_pred)
    labels = ['Anger', 'Contempt', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    res = dict([[x, '{:.4f}'.format(y)] for x, y in zip(labels, predction)])
    print(res)
    result = json.dumps(res)
    photo = "{% static \"images/" + image_name+"\"%}"
    return render(request, 'main/results.html', {'result':result, 'photo':photo})
