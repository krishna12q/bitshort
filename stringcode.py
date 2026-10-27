import string
import random

alphanumericlist = list(string.ascii_uppercase + string.digits)
code = ""

for i in range(5):
    code += random.choice(alphanumericlist)
    print(code)