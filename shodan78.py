import shodan
import sys
import argparse
argparse=argparse.ArgumentParser(description=sys.argv[0]+"will let you search about anything on shodan",usage=sys.argv[0]+"-s <topic>")
argparse.add_argument("-s","--shodan",help="Use it look up anything on shodan")
args=argparse.parse_args()
shodan1=args.shodan
api='X6AOVf7BYQ7CMP2nMqKLTTrlJcnXa4dU'
api=shodan.Shodan(api)
results=api.search(shodan1)
print("Total results found {}".format(results['total']))
try:
    for result in results['matches']:
        print(print("IP:{}".format(result['ip_str'])))
        print("{}".format(result['data']))
except Exception as e:
    print("No results found")
