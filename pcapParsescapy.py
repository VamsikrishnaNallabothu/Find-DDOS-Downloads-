try:
	import scapy.all as scapy
except ImportError:
	import scapy
import sys
import re


try:
	import scapy_http.http
except ImportError:
	from scapy.layers import http


def mymain():
	packets=scapy.rdpcap('login.pcap')
	mylist=[]
	for p in packets:
		#p.show()
		#sys.stdout=open("my", 'w')
		Get_http(p)
		



def Get_http(mypkt):
	http_pkt=str(mypkt)
	if http_pkt.find('POST'):
		return print_POST(mypkt)


def print_POST(pkt):
	ret = "\n".join(pkt.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
	print ret
	return ret


if __name__=='__main__':
	#mymain()
	sys.stdout=open("myContent", 'w')
	mymain()
	#GetPwd()


