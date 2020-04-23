import re
from django.core.validators import RegexValidator

VARY_PREC = 1
PRECISION = 6

ALPHABET_VALIDATOR = RegexValidator (r"^[a-zA-Z]+$", "Only letters alllowed")
PHONENUMBER_VALIDATOR = RegexValidator (r"^[0-9]{10}$", "Invalid phone number")
