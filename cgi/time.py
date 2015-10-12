__author__ = 'pp'
#!/usr/bin/python -w
import xml.etree.cElementTree as ET
import time

print "Content-type:text/xml"

time=int(time.time())

response = ET.Element("response",status="success")
ET.SubElement(response,"avp",a="currtime").text= str(time)
tree = ET.ElementTree(response)
print ET.tostring(response)
