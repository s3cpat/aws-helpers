#!/usr/bin/env python
'''
Prints YAML/JSON of a Security Group allowing
CloudFlare ports. For inclusion in a CloudFormation config.

@s3cpat
https://github.com/s3cpat
'''
import argparse
import json
import requests
import yaml


def get_range_data(include_ipv6=False):
    url = 'https://www.cloudflare.com/ips-v4'
    r = requests.get(url)
    r = r.text.splitlines()
    if include_ipv6:
        v6url = 'https://www.cloudflare.com/ips-v6'
        rv6 = requests.get(v6url)
        rv6 = rv6.text.splitlines()
        r = r + rv6
    return r


def generate_ingress_list(ranges):
    return [
        {
            'CidrIp': i,
            'Description': 'Allow 80 from Cloudflare IP',
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'ToPort': 80
        } for i in ranges if ':' not in i # if ipv4
    ] + [
        {
            'CidrIp': i,
            'Description': 'Allow 443 from Cloudflare IP',
            'FromPort': 443,
            'IpProtocol': 'tcp',
            'ToPort': 443
        } for i in ranges if ':' not in i # if ipv4
    ] + [
        {
            'CidrIpv6': i,
            'Description': 'Allow 80 from Cloudflare IP',
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'ToPort': 80
        } for i in ranges if ':' in i # if ipv6
    ] + [
        {
            'CidrIpv6': i,
            'Description': 'Allow 443 from Cloudflare IP',
            'FromPort': 443,
            'IpProtocol': 'tcp',
            'ToPort': 443
        } for i in ranges if ':' in i # if ipv6
    ]


def create_cfn_syntax_json(ranges):
    obj = {
        'CloudFlareWebPortsSecurityGroup': {
            'Type': 'AWS::EC2::SecurityGroup',
            'Properties': {
                'GroupDescription': 'Allow 80/443 via Cloudflare',
                'SecurityGroupIngress': generate_ingress_list(ranges),
            }
        }
    }
    return json.dumps(obj, indent=2)


def create_cfn_syntax_yaml(ranges):
    obj = json.loads(create_cfn_syntax_json(ranges))
    return yaml.dump(obj)


def generate_full_config(data, asyaml=False):
    obj = {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Description': 'CloudFormation config for CloudFlare web ' + \
                       'ports access via Security Group. @s3cpat' + \
                       ' | https://github.com/s3cpat',
        'Resources': json.loads(create_cfn_syntax_json(data))
    }
    if asyaml:
        return yaml.dump(obj)
    else:
        return json.dumps(obj, indent=2)


def main(args):
    print_as_yaml = args.yaml
    print_full_config = args.full
    include_ipv6 = args.includeipv6
    d = get_range_data(include_ipv6=include_ipv6)
    if print_full_config:
        print(generate_full_config(d, asyaml=print_as_yaml))
    else:
        if print_as_yaml:
            print(create_cfn_syntax_yaml(d))
        else:
            print(create_cfn_syntax_json(d))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create CloudFormation Resource (Security Group) to ' + \
                    'allow web access from Cloudflare IP Ranges. Pulls ' + \
                    'data from https://www.cloudflare.com/ips/' + \
                    'Prints as JSON or YAML.')
    parser.add_argument('--yaml', '-y',
                        default=False,
                        action='store_true',
                        help='Print Resource in YAML rather than JSON'
    )
    parser.add_argument('--includeipv6', '-s',
                        default=False,
                        action='store_true',
                        help='Include IPv6 ranges'
    )
    parser.add_argument('--full', '-f',
                        default=False,
                        action='store_true',
                        help='Print full CloudFormation config w/ ' + \
                             'resource inside rather than just the ' + \
                             'single resource'
    )
    args = parser.parse_args()
    main(args)
