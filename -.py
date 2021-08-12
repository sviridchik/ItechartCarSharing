import re

pattern = "(?P<pk>\d)||(?P<me>me)"


s = "3"

match = re.search(pattern,s)


print(match.groupdict())
