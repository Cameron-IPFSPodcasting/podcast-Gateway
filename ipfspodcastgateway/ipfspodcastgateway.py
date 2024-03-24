#!/usr/bin/python3
import re
import sys
import json
import shutil
import argparse
import requests
import subprocess

def emailCheck(email):
    if not re.match(r"(?!(^[.-].*|[^@]*[.-]@|.*\.{2,}.*)|^.{254}.)([a-zA-Z0-9!#$%&\\\'*+\/=?^_`{|}~.-]+@)(?!-.*|.*-\.)([a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,15}", email):
        raise argparse.ArgumentTypeError('invalid email: \'' + email + '\'')
    return email

#Command line args
parser = argparse.ArgumentParser(
    prog='ipfsgateway.py',
    description='Update your gateway settings with IPFSPodcasting.net',
    epilog='You may also manage your gateway via https://ipfspodcasting.net/Manage/Gateway',
    allow_abbrev=False)
parser.add_argument('--status', type=str, choices=['up', 'down'], help="status of your gateway")
parser.add_argument('--maxsize', type=int, help="maximum size (megabytes) of file to stream. 0 = unlimited")
parser.add_argument('--peers', action="store_true", help="connect to other Podcast Gateways")
parser.add_argument('--gc', action="store_true", help="run garbage collection")
parser.add_argument('--email', type=emailCheck, help="email to link your IPFSPodcasting.net account")
parser.add_argument('--ipfspath', type=str, help="path to your IPFS binary")
parser.add_argument('--apikey', type=str, help="your gateway API key")
args = parser.parse_args()

#If you'd like to hardcode your API key, uncomment the line below.
#args.apikey = 'xxxyourxxxapixxxkeyxxx'

#Find IPFS binary
custompath = ''
if args.ipfspath != None: custompath = args.ipfspath + ':'
ipfspath = shutil.which("ipfs", 0, custompath + "/usr/local/bin:/usr/bin:/bin")
if ipfspath is None:
    print("IPFS not found, try --ipfspath with the path to your IPFS binary")
    sys.exit(100)

payload = {'ipfs_id': None, 'ipfs_ver': None, 'version': '0.1'}

# Get IPFS ID
ipid = subprocess.run(ipfspath + " id", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if ipid.returncode == 0:
    payload['ipfs_id'] = json.loads(ipid.stdout).get("ID")

#Get IPFS version
diag = subprocess.run(ipfspath + " diag sys", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if diag.returncode == 0:
    ipfs = json.loads(diag.stdout)
    payload["ipfs_ver"] = ipfs["ipfs_version"]

#Process args & Send update
if args.status != None: payload['status'] = args.status
if args.maxsize != None: payload['maxsize'] = args.maxsize
if args.email != None: payload['email'] = args.email
if args.peers is True: payload['peers'] = args.peers
if args.apikey != None: payload['apikey'] = args.apikey

#Run GC (if they ask)
if args.gc is True:
    print('Running Garbage Collection...\n')
    gc = subprocess.run(ipfspath + " repo gc && " + ipfspath + " repo stat -H", shell=True)
    if gc.returncode == 0: print('\n...Complete')

#Get active gateways from website & swarm connect other gateways
response = requests.post("https://IPFSPodcasting.net/API/Gateway", timeout=120, data=payload)
try:
    peerdata = json.loads(response.text)
    if args.peers is True and len(peerdata['peers']) > 0:
        print('Requesting peers...')
        for key,val in peerdata['peers'].items():
            conn = subprocess.run(ipfspath + " swarm connect " + '/ip4/' + val['ip'] + '/tcp/4001/p2p/' + val['id'], shell=True)
except:
    peerdata = {'status': 'ERROR: Connecting to IPFSPodcasting.net'}

print(peerdata['status'])
