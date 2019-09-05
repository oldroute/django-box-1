import os
import random

SETTINGS_DIR = os.path.join(os.path.dirname(__file__), '{{ project_name }}', 'settings.py')
file = open(SETTINGS_DIR, 'w')
SECRET_KEY = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
file_content = """from generic_settings import *

NORECAPTCHA_SITE_KEY=''
NORECAPTCHA_SECRET_KEY=''
SECRET_KEY='%s'""" % SECRET_KEY
file.write(file_content)
file.close()
