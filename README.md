# IPFS Podcasting Gateway
Setting up an IPFS gateway is easy.
Configuring it properly is difficult.

This repository is not a complete "app" for running an IPFS gateway. There are many ways to run an IPFS gateway. This repository is a collection of code snippets & documentation to help setting up & configuring an IPFS Gateway that is compatible with [IPFSPodcasting.net](https://ipfspodcasting.net).

## Setting up a basic gateway...
- Download IPFS from [https://dist.ipfs.tech/#kubo](https://dist.ipfs.tech/#kubo)
- Extract & Install 
- Run `ipfs init` to configure your gateway
- Launch the IPFS daemon with `ipfs daemon`
  
A gateway is now running with a webui at [127.0.0.1:5001/webui](http://127.0.0.1:5001/webui)
And a gateway running at [127.0.0.1:8080](http://127.0.0.1:8080/ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme)

- Configure your server to start IPFS on boot
  
## Configuring a reverse proxy...
A reverse proxy is preferred for more control over access to your gateway.

Refer to the [IPFS documentation](https://docs.ipfs.tech/how-to/gateway-best-practices/#self-hosting-a-gateway) for guidelines on setting up an IPFS gateway.

## Domain / SSL
Configure a domain name for your gateway and setup SSL.

At this point, you're running a public IPFS gateway. Any IPFS url to your gateway will resolve and serve IPFS content. 

---

# Configure an "IPFS Podcasting Gateway"
For a "Podcast Gateway", we only want to serve podcast media, so need to block all non-podcast urls.

A quick way to become a "podcast only" gateway is to filter urls that only match the ipfspodcasting format.

All media files on [IPFSPodcasting.net](https://ipfspodcasting.net) are "wrapped" in a hashed folder. This is how the web url appears in a gateway request for all ipfspodcasting enclosures.

- `https://<gateway>/ipfs/<hash>/<filename>.<extension>`
- [https://ipfs.io/ipfs/QmcffbRzN7qcF9xhbH52Fh5TvfddKt3FRucMsX8Qbn1GV5/PC20-145-2023-09-08-Final.mp3](https://ipfs.io/ipfs/QmX52fQAESMZTSjDZWNUReViC6LUJfeHiHPA3eS5viq5Q1/PC20-144-2023-09-01-Final.mp3#t=4828)

## Enclosure Analysis
The current ipfspodcasting database contains 128K enclosures. This data was used to analyze enclosure extensions.

![Untitled](https://github.com/Cameron-IPFSPodcasting/podcast-Gateway/assets/103131615/8bcce8a8-cdf8-4152-a8cd-1b0c152819f1)

96% of enclosures use the mp3 extension. 
99.7% use the mp3, m4a, or mp4 extension.

### URL Filter
A simple filter that matches the folder & file extension format above will handle 99.7% of the podcast media files.

If the request does not match this format, your gateway can redirect to ipfs.io for handling non-standard/non-podcast urls.

Of course, people could sneak past this filter by using the same hash/filename.mp3 format. If it becomes a bigger issue, we can investigate block lists. The key objective, is that we are not hosting malware in the form of applications (exe), powershell, or pdfs. And are not providing bandwidth to IPFS hosted websites or videos.

This regex will test if the url matches the ipfspodcasting format.
```
^\/ipfs\/Qm[1-9A-HJ-NP-Za-km-z]{44}(\/.*\.(?i)(mp3|mp4|m4a))
```
Adding this to the proxy will allow urls that match, or redirect any mismatches to ipfs.io. Even a mismatch should perform normally using ipfs.io.

- Sample [virtualhost.conf](https://github.com/Cameron-IPFSPodcasting/podcast-Gateway/blob/main/sample-apache-virtualhost.conf) for apache.
- Sample [location.conf](https://github.com/Cameron-IPFSPodcasting/podcast-Gateway/blob/main/sample-nginx-location.conf) for nginx.

### DNS Resolution
IPFS uses multiaddr for node resolution. Setup your DNS by adding a TXT records for _dnsaddr. Use [this link](https://github.com/multiformats/multiaddr/blob/master/protocols/DNSADDR.md) to setup your gateway's DNS record.

### Sample / Test urls
These links use the ipfspodcasting gateway (which is configured to check the url for a valid format). You can test your gateway by changing the domain to match your gateway's url...

A PC20#146 episode (works - stays on gateway.ipfspodcasting.net) - https://gateway.ipfspodcasting.net/ipfs/QmbBW9jBNh2G2wWXyywTQ9mSLuNXFUAmReSkSeRJsEbycH/PC20-146-2023-09-15-Final.mp3

Changing the filename to "mp5" doesn't match, so redirects to ipfs.io  (then fails because it doesn't exist) - https://gateway.ipfspodcasting.net/ipfs/QmbBW9jBNh2G2wWXyywTQ9mSLuNXFUAmReSkSeRJsEbycH/PC20-146-2023-09-15-Final.mp5

These urls will redirect to ipfs.io because they don't match the ipfspodcasting url format. Therefore aren't being served by the ipfspodcasting gateway.

An Apollo 12 Image - https://gateway.ipfspodcasting.net/ipfs/QmSnuWmxptJZdLJpKRarxBMS2Ju2oANVrgbr2xWbie9b2D/albums/QXBvbGxvIDEyIE1hZ2F6aW5lIDQ2L1k=/21688456932_c56ec92952_o.jpg

An IPFS hosted website - https://gateway.ipfspodcasting.net/ipfs/QmNksJqvwHzNtAtYZVqFZFfdCVciY4ojTU2oFZQSFG9U7B/index.html

A viral video - https://gateway.ipfspodcasting.net/ipfs/QmcniBv7UQ4gGPQQW2BwbD4ZZHzN3o3tPuNLZCbBchd1zh#t=85

### Conclusion
This approach should handle the majority of podcast media files used by [IPFSPodcasting.net](https://ipfspodcasting.net) while forwarding the rest (0.3%) to ipfs.io.

More improvements to come as they are discovered/required. Use the [discussions tab](https://github.com/Cameron-IPFSPodcasting/podcast-Gateway/discussions) to discuss other options, or the [issues tab](https://github.com/Cameron-IPFSPodcasting/podcast-Gateway/issues) to report problems with existing options.
