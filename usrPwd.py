from sys import argv 
import re

def GetPwd():
	#myfile=raw_input("Enter the http content file name: ")
	#script, myfile = argv
	f=open('myContent')
	file_length = sum(1 for line in f)
	#print num_lines
	f.seek(0)
	l="uid="
	p="passw="
	while file_length != 1:
	   file_length -= 1
	   m = f.readline()
	   if l and p in m:
	      #print m.replace('&',' ').split()
	      x = m.replace('&',' ').split()
	#      print x
	      for items in x:
	         #print "x1xxxxxxx"
	         if "uid" in items:
	             print "UserName: ", items.replace("'",'')
	         if "pass" in items:
	             print "Password: ", items
	   else:
	     continue

if __name__=="__main__":
	GetPwd()
