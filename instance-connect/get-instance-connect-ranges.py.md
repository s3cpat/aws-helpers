## Usage
```bash
python ./get-instance-connect-ranges.py -h
usage: get-instance-connect-ranges.py [-h] [--yaml] [--full]

Create CloudFormation Resource (Security Group) to allow SSH from EC2 Instance
Connect IP Ranges. Pulls data from https://ip-ranges.amazonaws.com/ip-
ranges.json. Prints as JSON or YAML.

optional arguments:
  -h, --help  show this help message and exit
  --yaml, -y  Print Resource in YAML rather than JSON
  --full, -f  Print full CloudFormation config w/ resource inside rather than
              just the single resource
```
