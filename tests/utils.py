import re

NLRE = re.compile(r'\r\n|\r|\n')

def os_independent_text_equals(a, b):
    return NLRE.split(a) == NLRE.split(b)