#! /usr/bin/python
from datetime import datetime,date


dia = '14/1/2013'
formatter_string = "%d/%m/%Y" 
datetime_object = datetime.strptime(dia, formatter_string)
dia1 = datetime_object.date()
print dia1

dia = '14/01/2014'
formatter_string = "%d/%m/%Y" 
datetime_object = datetime.strptime(dia, formatter_string)
dia2 = datetime_object.date()
print dia2

if dia1<dia2:
    print "dia:",dia1,"<", dia2
if dia2<dia1:
    print "dia:",dia2,"<",dia1
if dia2==dia1:
    print "dia:",dia1,"=",dia2   