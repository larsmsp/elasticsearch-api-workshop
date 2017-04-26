import json
import requests
import sys


def index(endpoint, from_file):
    print "Loading data from %s and posting it to %s..." % (from_file, endpoint)
    with open(from_file, 'r') as fp:
        data = json.load(fp)
        requests.post(endpoint, json=data)
    print "Done!"


def help():
    print "Usage: python %s <endpoint> <file to load from>\n" % sys.argv[0]


if __name__ == '__main__':
    if len(sys.argv) < 3:
        help()
    else:
        index(sys.argv[1], sys.argv[2])
