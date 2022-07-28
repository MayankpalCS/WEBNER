import time
import whois
import dns.resolver
import shodan
import requests
import sys
import argparse
import socket
from colorama import init, Fore
init()
red = Fore.RED
blue = Fore.BLUE
green = Fore.GREEN
yellow=Fore.YELLOW
reset = Fore.RESET
print("Created by mayank pal")
def banner():
    print("""%s
              |      | |------ ||    ||     | |------ | |
              |      | |       |  |  |  |   | |       |   |
              |  ||  | |------ ||    |   |  | |-----  | |
              | |  | | |       |  |  |    | | |       ||
              ||    || |------ ||    |     || |_____  |  |
                # Coded By Mayankpal - @mayank            |
                           """)
banner()

n="Its a tool for footprinting of websites created by mayank pal"
argparse=argparse.ArgumentParser(description=n,usage="python3"+sys.argv[0]+"-d Domain [-s IP]")
argparse.add_argument("-d","--domain",help="Enter the domain name to footprint",required=True)
argparse.add_argument("-s","--shodan",help="Enter the shodan")
argparse.add_argument("-f","--file",help="Enter file")

#fetching the arguments
args=argparse.parse_args()#parsed the values
domain=args.domain#above we enteres --domain will be fetched hhere
IP=args.shodan
file=args.file
#whoismodule
#using whois library andcreating instance
print("[+]Using whois module to collect information about {} ".format(domain))
whoisresult=""
#Getting the information
winstan = whois.query(domain)
try:
    print("[+] Got the information and extractin....")

    whoisresult+="[+]Name:{}".format(winstan.name) + '\n'
    whoisresult+="[+]Registrar:{}".format(winstan.registrar) + '\n'
    whoisresult+="[+]Creation date {}".format(winstan.creation_date) + '\n'
    whoisresult+="[+]Registrant {}".format(winstan.registrant) + '\n'
    whoisresult+="[+]Registration {}".format(winstan.registrant_country) + '\n'
    whoisresult+="[+]expiration date {}".format(winstan.expiration_date) + '\n'
    whoisresult+="[+]admin {}".format(winstan.admin) + '\n'
    whoisresult+="[+]owner {}".format(winstan.owner) + '\n'
    whoisresult+="[+]status {}".format(winstan.status) + '\n'
    whoisresult+="[+]tld {}".format(winstan.tld) + '\n'
    whoisresult+="[+]last updated {}".format(winstan.last_updated) + '\n'

except:
    pass

print(f"{green}{whoisresult}")

time.sleep(4)
#Getting DNS information
print("[+]Getting DNS information ...")
DNSINFO=""
try:
    #we used for loops because there might be multiple a records or multiple mx records in a single domain
    for a in dns.resolver.resolve(domain,'A'):
        DNSINFO+='[+]A record {}'.format(a.to_text()) + '\n'
except Exception as e:
    print("A record could not be found")
        #A record basically points our website to a server
        #so this for loop will get the ipv4 of our websute
try:
    for a in dns.resolver.resolve(domain,'MX'):
        DNSINFO+='[+]MX record {}'.format(a.to_text()) + '\n'
#MX basically helps in recieving emails in a server
except Exception as p:
    print("MX record could not be found")
try:
    for a in dns.resolver.resolve(domain,'NS'):
        DNSINFO+='[+]NS record {}'.format(a.to_text()) + '\n'
except Exception as m:
    print("NS record could not be found")
try:
    for a in dns.resolver.resolve(domain,'TXT'):
        DNSINFO+='[+]TXT record {}'.format(a.to_text()) + '\n'
except Exception as k:
    print("[-]TXT record could not be found")
try:
    for a in dns.resolver.resolve(domain,'AAAA'):
        DNSINFO+='[+]AAAA record {}'.format(a.to_text()) + '\n'
except Exception as y:
    print("AAAA record could not be found")
        #AAAA record basicall is similar to A record
        # but points to ipv6 ip
try:
    for a in dns.resolver.resolve(domain,'SRV'):
        DNSINFO+='[+]SRV record {}'.format(a.to_text()) + '\n'
except Exception as b:
    print("SRV record could not be found")
try:
    for a in dns.resolver.resolve(domain,'SOA'):
        DNSINFO+='[+]SOA record {}'.format(a.to_text()) +'\n'
except Exception as n:
    print("SOA record could not be found")
try:
    for a in dns.resolver.resolve(domain,'CNAME'):
        DNSINFO+='[+]CNAME record {}'.format(a.to_text()) + '\n'
except Exception as om:
    print("CNAME  record could not be found")
        # cname works for subdomains basically holds record that these subdomains redirect to main domain
try:
    for a in dns.resolver.resolve(domain,'SPF'):
        DNSINFO+='[+]SPFrecord {}'.format(a.to_text()) + '\n'
except Exception as o:
    print("SPF record could not be found")

print(f"{green}{DNSINFO}")
#Geolocation module
time.sleep(4)
GEOINFO=""
print("[+]Getting geolocation information....")
try:
    response=requests.request('GET','http://geolocation-db.com/json/' + socket.gethostbyname(domain)).json()
    GEOINFO+="[+] Country: {}".format(response['country_name']) + '\n'
    GEOINFO+="[+] Latitude: {}".format(response['latitude']) + '\n'
    GEOINFO+="[+] Longitude: {}".format(response['longitude']) + '\n'
    GEOINFO+="[+] State: {}".format(response['state']) + '\n'
    GEOINFO+="[+] City: {}".format(response['city']) + '\n'
except:
    pass
print(f"{green}{GEOINFO}")
if IP:
    Shodaninfo=""
    try:
        print("Getting information using shodan")
        api=input("What is you api")
        api=shodan.Shodan(api)
        results=api.search(IP)
        Shodaninfo+="Total results found: {}".format(results['total']) +'\n'
        for result in results['matches']:
            Shodaninfo+="IP:{}".format(result['ip_str']) + '\n'
            Shodaninfo+="{}".format(result['data'])+'\n'
    except:
        pass
    print(f"{green}{Shodaninfo}")
if (file):
    with open(file,'w') as file:
        file.write("Whois information"+'\n'+whoisresult + '\n\n\n')
        file.write("DNS information:"+'\n'+DNSINFO + '\n\n\n')
        file.write("Geological information"+'\n'+GEOINFO + '\n\n\n')
        file.write("Shodan information"+ '\n'+Shodaninfo+'\n\n\n')
