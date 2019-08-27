# coding: utf-8
import os, sys, time, socket, json, urllib, urllib.request, urllib.parse
import argparse as ap
from ipwhois import IPWhois
from IPy import IP

parser = ap.ArgumentParser()
parser.add_argument("-i", "--ip", required=True)
parser.add_argument("-w", "--whois", action='store_false')
parser.add_argument("--info", action='store_false')
parser.add_argument("--iptohostname", action='store_false')
parser.add_argument("--hostnametoip", action='store_false')
args = parser.parse_args()
ip = args.ip
good = ip


def isIP(str):
    try:
        IP(str)
    except ValueError:
        return False
    return True

istrue = isIP(ip)

def whois():
    print("")
    print("[!] WHOIS\n")
    if istrue == False:
        ip = socket.gethostbyname(good)
    obj = IPWhois(ip)
    whois = obj.lookup_whois()
    for i in ["asn","asn_cidr","asn_country_code","asn_date","asn_description","asn_registry","nir","query","referral"]:
        if whois[i] == None:
            whois[i] = "None"
    print("[*] General result\n")
    print("[+] ASN : "+whois['asn'])
    print("[+] ASN CIDR : "+whois['asn_cidr'])
    print("[+] ASN country code : "+whois['asn_country_code'])
    print("[+] ASN date : "+whois['asn_date'])
    print("[+] ASN description : "+whois['asn_description'])
    print("[+] ASN registery : "+whois['asn_registry'])
    print("[+] IP : "+whois['query'])
    for a in range(len(whois['nets'])):
        for i in ["address","city","country","created","description","emails","handle","name","postal_code","state","updated","handle","postal_code","state","range"]:
            if whois['nets'][a][i] == None:
                whois['nets'][a][i] = "None"
        whois['nets'][a]['address'] = whois['nets'][a]['address'].replace("\n", " ")
        if a+1 == 2:
            number = "2nd"
        elif a+1 == 3:
            number = "3rd"
        else:
            number = str(a+1)+"th"
        print("")
        print("[*] "+number + " result\n")
        print("[+] Country : "+whois['nets'][a]['country'])
        print("[+] State : "+whois['nets'][a]['state'])
        print("[+] City : "+whois['nets'][a]['city'])
        print("[+] Address : "+whois['nets'][a]['address'])
        print("[+] Postal code : "+whois['nets'][a]['postal_code'])
        print("[+] Created date : "+whois['nets'][a]['created'])
        print("[+] Updated : "+whois['nets'][a]['updated'])
        print("[+] Description : "+whois['nets'][a]['description'])
        print("[+] Name : "+whois['nets'][a]['name'])
        print("[+] Handle : "+whois['nets'][a]['handle'])
        print("[+] Range : "+whois['nets'][a]['range'])
        print("[+] CIDR : "+whois['nets'][a]['cidr'])
        if str(type(whois['nets'][a]['emails'])) == "<class 'list'>":
            print("[+] Emails :",' , '.join(whois['nets'][a]['emails']))
        elif str(type(whois['nets'][a]['emails'])) == "<class 'str'>":
            print("[+] Email :",whois['nets'][a]['emails'])

def info():
    print("")
    print("[!] IP INFO\n")
    request = urllib.request.Request('http://ip-api.com/json/' + ip)
    info = urllib.request.urlopen(request).read().decode('utf-8')
    array = json.loads(info)
    print('[+] IP :',array['query'])
    print('[+] Country :',array['country'])
    print('[+] City :',array['city'])
    print('[+] Region :',array['regionName'])
    print('[+] Country Code :',array['countryCode'])
    print('[+] ZipCode :',array['zip'])
    print('[+] ISP :',array['isp'])
    print('[+] Location Lat/Lon :',str(array['lat']) + '/' + str(array['lon']))
    print('[+] Organization :',array['org'])
    print('[+] TimeZone :',array['timezone'])


def hostnameip():
    print("")
    print("[!] HOSTNAME TO IP\n")
    print('[+] ' + socket.gethostbyname(ip) + ' is the ip of ' + ip)

def iphostname():
    print("")
    print("[!] IP (or domain) TO HOSTNAME\n")
    print('[+]',socket.gethostbyaddr(ip)[0],'is the hostname of',ip)

if args.whois == False:
    whois()

if args.info == False:
    info()

if args.iptohostname == False:
    iphostname()

if args.hostnametoip == False:
    hostnameip()
