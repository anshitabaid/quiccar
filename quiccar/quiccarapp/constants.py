import re
from django.core.validators import RegexValidator

VARY_PREC = 1
PRECISION = 6
TOKEN_LENGTH=16

ALPHABET_VALIDATOR = RegexValidator (r"^[a-zA-Z]+$", "Only letters alllowed")
PHONENUMBER_VALIDATOR = RegexValidator (r"^[0-9]{10}$", "Invalid phone number")

CHANGE_PASSWORD_LINK='http://localhost:8000/quiccar/verifyToken?username={username}&token={token}'
EMAIL_BODY = 'Hello {name}.\nPlease click on this link to reset your password.\n\n{link}\n\Thank you!'