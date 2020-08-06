# -*- coding: utf-8 -*-
import re

line = "<span style=\'mso-spacerun:yes\'>   </span>图木舒克市"
matchObj = re.match( r'(.*) </span>(.*)', line, re.S)
if matchObj:
    print "matchObj.group() : ", matchObj.group()
    print "matchObj.group(1) : ", matchObj.group(1)
    print "matchObj.group(2) : ", matchObj.group(2)
else:
    print "No match!!"


matchObj = re.match( r'(.*) are (.*?) .*', line, re.S)
if matchObj:
    print "matchObj.group() : ", matchObj.group()
    print "matchObj.group(1) : ", matchObj.group(1)
    print "matchObj.group(2) : ", matchObj.group(2)
else:
    print "No match!!"