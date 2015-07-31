import re

s = r'sena\2015_06_19_8888\sean'
date_pattern = re.compile(r'\d{4}_?\d{2}_?\d{2}_\d{4}')
match = date_pattern.search(s)
print match.group()

