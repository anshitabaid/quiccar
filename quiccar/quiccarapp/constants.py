import re, pytz
from django.core.validators import RegexValidator

VARY_PREC = 1
PRECISION = 6
FP_TOKEN_LENGTH=16
EV_TOKEN_LENGTH=6

ALPHABET_VALIDATOR = RegexValidator (r"^[a-zA-Z]+$", "Only letters alllowed")
PHONENUMBER_VALIDATOR = RegexValidator (r"^[0-9]{10}$", "Invalid phone number")


LINK_VALID_TIME = 12 #hours 
CHANGE_PASSWORD_LINK='http://quiccar2.herokuapp.com/quiccar/verifyToken?username={username}&token={token}'
EMAIL_BODY = 'Hello {name}.\nPlease click on this link to reset your password.\n\n{link}\n\nThis link is valid for ' + str(LINK_VALID_TIME) + ' hours.\n\n' +  'Thank you!'
EMAIL_SUBJECT = 'Password reset'
TIMEZONE = pytz.timezone ('Asia/Kolkata')

DATETIME_FORMAT = "%d-%b-%Y %H:%M:%S"

MINUTES_CUTOFF=60