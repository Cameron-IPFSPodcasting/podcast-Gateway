# Gateway Update Script

Use this script to communicate changes with IPFSPodcasting.net (run from your IPFS gateway).

```
usage: ipfsgateway.py [-h] [--status {up,down}] [--maxsize MAXSIZE] [--peers] [--gc] [--email EMAIL]
                      [--ipfspath IPFSPATH] [--apikey APIKEY]

Update your gateway settings with IPFSPodcasting.net

options:
  -h, --help           show this help message and exit
  --status {up,down}   status of your gateway
  --maxsize MAXSIZE    maximum size (megabytes) of file to stream. 0 = unlimited
  --peers              connect to other Podcast Gateways
  --gc                 run garbage collection
  --email EMAIL        email to link your IPFSPodcasting.net account
  --ipfspath IPFSPATH  path to your IPFS binary
  --apikey APIKEY      your gateway API key

You may also manage your gateway via https://ipfspodcasting.net/Manage/Gateway
```
## IPFS Binary

The script will look for your IPFS binary in /usr/local/bin; /usr/bin; or /bin;

If you have installed IPFS in a non-standard location, use the --ipfspath option to specify the directory containing the IPFS binary.

## First Run

## API Key

## Status Updates
