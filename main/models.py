
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
import os


class Document(models.Model):
    #image_path = os.path.join(settings.BASE_DIR, 'images')
    docfile = models.ImageField(upload_to='')
    #docfile = models.FileField(upload_to='images/')
