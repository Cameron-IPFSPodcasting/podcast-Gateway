# IPFS Podcasting Gateway
Setting up an IPFS gateway is easy.
Configuring it properly is difficult.

This is not a complete solution for running an IPFS gateway. There are many ways to run an IPFS gateway. This repository is for guidelines and discussion around setting up an "IPFS Podcasting Gateway".

This repository is a collection of code snippets & documentation to help setting up & configuring an IPFS Gateway that is compatible with [IPFSPodcasting.net](https://ipfspodcasting.net).

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

# Configure an "IPFS Podcasting Gateway"
For a "Podcasting Gateway", we only want to serve podcast media, so need to block all non-podcast urls.

A quick way to become a "podcast only" gateway is to filter urls that only match the IPFS Podcasting format.

All media files on [IPFSPodcasting.net](https://ipfspodcasting.net) are "wrapped" in a hashed folder.

This is how the web url appears in a gateway request for all ipfspodcasting enclosures.

`https://<gateway>/ipfs/<hash>/<filename>`

https://ipfs.io/ipfs/QmcffbRzN7qcF9xhbH52Fh5TvfddKt3FRucMsX8Qbn1GV5/PC20-145-2023-09-08-Final.mp3

The current ipfspodcasting database contains 128K enclosures. This data was used to analyze enclosure filenames/extensions.

95.96%	mp3
2.75%	m4a
0.99%	mp4
0.13%	jpeg
0.05%	m4v
0.04%	pdf
0.04%	jpg
0.04%	png

96% of enclosures end in the .mp3 extension. 
99.7% have the mp3, m4a, or mp4 extension.

A simple filter that matches this folder & file extension format will handle nearly 100% of the podcast media files.

If the request does not match this format, your gateway can redirect to ipfs.io to let ipfs.io handle any non-standard/non-podcast urls.

People could sneak past this filter by using the same hash/filename.mp3 format. If it becomes a bigger issue, we can investigate block lists. The key objective, is that we are not hosting malware in the form of applications(exe), powershell, pdfs. And are not hosting IPFS hosted websites or videos.

This Regex will test that the url matches the podcasting format (99.7% of the enclosures on ipfspodcasting.net).
^\/ipfs\/Qm[1-9A-HJ-NP-Za-km-z]{44}(\/.*\.(?i)(mp3|mp4|m4a))

Adding this to my (apache) proxy will pass to my gateway on a match, or ipfs.io for any mismatches. Even a mismatch should perform normally using ipfs.io (unless they have setup block lists for the url).

(sample ipfs-gateway.conf for apache. This gateway runs on a LAN with port forwards from cloudflare to manage SSL)
```
<VirtualHost 192.168.1.1:81>
  RewriteEngine On
  RewriteCond "%{REQUEST_URI}" "^\/ipfs\/Qm[1-9A-HJ-NP-Za-km-z]{44}(\/.*\.(?i)(mp3|mp4|m4a))"
  RewriteRule (.*) http://127.0.0.1:8080$1 [P]
  RewriteRule (.*) https://ipfs.io$1 [L,R]

  ProxyPass / http://127.0.0.1:8080/
  ProxyPassReverse / http://127.0.0.1:8080/
  ProxyPreserveHost On
</VirtualHost>
```
These links use the ipfspodcasting gateway (which is configured to check the url for a valid format)...

A PC20#146 episode (works - stays on gateway.ipfspodcasting.net)...
https://gateway.ipfspodcasting.net/ipfs/QmbBW9jBNh2G2wWXyywTQ9mSLuNXFUAmReSkSeRJsEbycH/PC20-146-2023-09-15-Final.mp3
Changing the filename to "mp5" doesn't match, so redirects to ipfs.io  (then fails because it doesn't exist)
https://gateway.ipfspodcasting.net/ipfs/QmbBW9jBNh2G2wWXyywTQ9mSLuNXFUAmReSkSeRJsEbycH/PC20-146-2023-09-15-Final.mp5

All these urls will redirect to ipfs.io because they don't match the ipfspodcasting url format. Therefore aren't being served by the ipfspodcasting gateway.
Apollo12 Image - https://gateway.ipfspodcasting.net/ipfs/QmSnuWmxptJZdLJpKRarxBMS2Ju2oANVrgbr2xWbie9b2D/albums/QXBvbGxvIDEyIE1hZ2F6aW5lIDQ2L1k=/21688456932_c56ec92952_o.jpg
An IPFS hosted website - https://gateway.ipfspodcasting.net/ipfs/QmNksJqvwHzNtAtYZVqFZFfdCVciY4ojTU2oFZQSFG9U7B/index.html
A viral video - https://gateway.ipfspodcasting.net/ipfs/QmcniBv7UQ4gGPQQW2BwbD4ZZHzN3o3tPuNLZCbBchd1zh#t=85

More improvements to come as they are discovered/required. This approach should handle the majority of podcast media files used my IPFSPodcasting.net while blocking/forwarding the rest to ipfs.io.
