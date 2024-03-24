# Gateway Update Script
Use this script to communicate gateway changes with IPFSPodcasting.net (run from your IPFS gateway).

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
## First Run
On first run, you must supply an email address to link/notify your account at [IPFSPodcasting.net](https://IPFSPodcasting.net/Manage)

Once linked to your account, an API Key will be generated for future updates.

## API Key
Use your API Key to communicate future updates with the `--apikey` option. You can also modify this script to add your API Key.

## Status Updates

### IPFS Binary
The script will look for your IPFS binary in `/usr/local/bin;` `/usr/bin;` or `/bin;`

If you have installed IPFS in a non-standard location, use the `--ipfspath` option to specify the directory containing your IPFS binary.
