#!/usr/bin/python
# -*- coding: utf-8 -*-
import dpkt
import socket
import pygeoip
import optparse
import dropbox
import webbrowser

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

def retGeoStr(ip):
    try:
        rec = gi.record_by_name(ip)
        city = rec['city']
        country = rec['country_code3']
        if city != '':
            geoLoc = city + ', ' + country
        else:
            geoLoc = country
        return geoLoc
    except Exception, e:
        return 'Unregistered'


def printPcap(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            printPcap.ip = eth.data
            vip=printPcap.ip
            printPcap.src = socket.inet_ntoa(vip.src)
            src=printPcap.src
            printPcap.dst = socket.inet_ntoa(vip.dst)
            dst=printPcap.dst
            print '[+] Src: ' + src + ' --> Dst: ' + dst
            print '[+] Src: ' + retGeoStr(src) + '--> Dst: ' \
              + retGeoStr(dst)
        except:
            pass

def retKML(ip):
    rec = gi.record_by_name(ip)
    try:
        longitude = rec['longitude']
        latitude = rec['latitude']
        kml = (
               '<Placemark>\n'
               '<name>%s</name>\n'
               '<Point>\n'
               '<coordinates>%6f,%6f</coordinates>\n'
               '</Point>\n'
               '</Placemark>\n'
               ) %(ip,longitude, latitude)
        return kml
    except:
        return ''


def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            #eth = dpkt.ethernet.Ethernet(buf)
            #ip = eth.data
            ip= printPcap.ip
            #src = socket.inet_ntoa(printPcap.ip.src)
            src= printPcap.src
            srcKML = retKML(src)
            #dst = socket.inet_ntoa(ip.dst)
            dst= printPcap.dst
            dstKML = retKML(dst)
            kmlPts = kmlPts + srcKML + dstKML
        except:
            pass
    return kmlPts


def read_pcap():
    parser = optparse.OptionParser('usage %prog -p <pcap file>')
    parser.add_option('-p', dest='pcapFile', type='string',\
      help='specify pcap filename')
    (options, args) = parser.parse_args()
    if options.pcapFile == None:
        print parser.usage
        exit(0)
    pcapFile = options.pcapFile
    f = open(pcapFile)
    f2=open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    return pcap

def geo_pcap():
    pcap= read_pcap()
    printPcap(pcap)

def kml_main():
    pcap= read_pcap()
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?>\
    \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
    print kmldoc
    with open('nvk.kml', 'wb') as output:
        output.write(kmldoc)
    #printPcap(pcap)

def mydropbox():
    access_token= raw_input('Enter the access token')
    myAPP= dropbox.client.DropboxClient(access_token)
    #print 'linked account: ', myAPP.account_info()
    file=open('nvk.kml', 'rb')
    response= myAPP.put_file('/nvk.kml', file)
    print('uploaded: ', response)
    #folder_metadata=myAPP.metadata('/')
    #print 'metadata: ', folder_metadata

def access_Google_maps():
    url= 'https://www.dropbox.com/home/Apps/Viewmykml/nvk.kml'
    brwsr= webbrowser.get('firefox')
    brwsr.open(url)


if __name__ == '__main__':
    geo_pcap()
    kml_main()
    mydropbox()


