from generic_settings import *

DEBUG = True

from django.core.cache import cache
cache.clear()

NORECAPTCHA_SITE_KEY = '6LeijW8UAAAAAAy4r2oO3CFxsJWCMhEPD76qSggC'
NORECAPTCHA_SECRET_KEY = '6LeijW8UAAAAAOOkINNxEqkElGtT0llRnmcAEUeR'