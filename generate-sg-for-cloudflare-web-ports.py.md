## Usage
```bash
python ./generate-sg-for-cloudflare-web-ports.py -h
usage: generate-sg-for-cloudflare-web-ports.py [-h] [--yaml] [--includeipv6]
                                               [--full]

Create CloudFormation Resource (Security Group) to allow web access from
Cloudflare IP Ranges. Pulls data from https://www.cloudflare.com/ips/Prints as
JSON or YAML.

optional arguments:
  -h, --help         show this help message and exit
  --yaml, -y         Print Resource in YAML rather than JSON
  --includeipv6, -s  Include IPv6 ranges
  --full, -f         Print full CloudFormation config w/ resource inside
                     rather than just the single resource
```
