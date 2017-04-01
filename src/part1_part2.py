import re

str1 = 'onyx.southwind.net - - [01/Jul/1995:00:03:03 -0400] "GET /images/KSC-94EC-412-small.gif HTTP/1.0" 200 20484 '
str2 = 'ix-war-mi1-20.ix.netcom.com - - [01/Jul/1995:00:05:13 -0400] "GET /shuttle/missions/sts-78/news HTTP/1.0" 302 - '

pattern = '(?P<ip>\S+).*' + \
          '\[(?P<date>.+)\]\s*' + \
          '"(?P<request_method>\S+)\s+(?P<url>\S+)\s+(?P<protocol>\S+)"\s*' + \
          '(?P<response_code>\d+)\s+(?P<response_length>\d+|-)'

regex = re.compile(pattern)
result = regex.match(str1)


print(result.group("ip"))
print(result.group("date"))
print(result.group("url"))
print(result.group("response_code"))
print(result.group("response_length"))
