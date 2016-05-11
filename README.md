# Network-Traffic-Analyzer
Finding the list of users(IPs) downloading the content from blacklisted website.
My Scipts will find the src and destination IP addresses and their physical locations can be mapped on the Google Maps through a KML file that is generated.

Used dpkt to parse the top layers of the packet such as ethernet and IP. AS it is difficult to parse the http content from the pcap using dpkt, I have made use of scapy-http to retrieve the http content from the packet capture file. 


The username and password of an user logging in to a particular website will be fetched using the usrPwd.py, when run after running the pcapParseScapy.py.


Thats it  :)


