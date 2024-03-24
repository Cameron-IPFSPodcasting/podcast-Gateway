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
Use your API Key to communicate future updates with the `--apikey` option. You can also [modify this script](https://github.com/Cameron-IPFSPodcasting/podcast-Gateway/blob/72bf0f33a1e7d53d5c0f5314e3064c38554232ee/ipfspodcastgateway/ipfspodcastgateway.py#L31) (locally) to add your API Key.

To generate a new API Key, visit your account page at [IPFSPodcasting.net](https://IPFSPodcasting.net/Manage/Gateway)

## Status Updates
To inform IPFS Podcasting of your gateway status, use `--status up` to receive traffic, or `--status down` to stop receiving traffic.

This can be automated for maintenance, bandwidth usage (self-monitored), or time of day.

##Website
You may update your status, domain name, and payment info using the [website](https://IPFSPodcasting.net/Manage/Gateway).
![Untitled](https://github.com/Cameron-IPFSPodcasting/podcast-Gateway/assets/103131615/bb81e951-244e-4efe-98ce-87909332a3e7)

### Max file to stream
You can also set `--maxsize` to restrict hosting large files.

##Peer Connect
Use `--peers` to establish connections with other IPFS Podcasting Gateways.

### Garbage Collection
`--gc` will initiate IPFS garbage collection (same as running `ipfs repo gc`)

### IPFS Binary
The script will look for your IPFS binary in `/usr/local/bin;` `/usr/bin;` or `/bin;`

If you have installed IPFS in a non-standard location, use the `--ipfspath` option to specify the directory containing your IPFS binary.
