#!/usr/bin/env python
'''
Prints YAML/JSON of a Security Group allowing
EC2 Instance Connect. For inclusion in a CloudFormation config.

@s3cpat
https://github.com/s3cpat
'''
import argparse
import json
import requests
import yaml


def get_range_data():
    url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
    r = requests.get(url)
    j = json.loads(r.text)
    return j

def filter_range_to_ec2_instance_connect(data):
    service = 'EC2_INSTANCE_CONNECT'
    ranges = [d['ip_prefix'] for d in data['prefixes'] if d['service'] == service]
    return ranges


def generate_ingress_list(ranges):
    return [
        {
            'CidrIp': i,
            'Description': 'Allow SSH from EC2 Instance Connect Range',
            'FromPort': 22,
            'IpProtocol': 'tcp',
            'ToPort': 22
        } for i in ranges
    ]


def create_cfn_syntax_json(ranges):
    obj = {
        'EC2INSTANCECONNECTSecurityGroup': {
            'Type': 'AWS::EC2::SecurityGroup',
            'Properties': {
                'GroupDescription': 'Allow SSH via AWS EC2 Instance Connect',
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
        'AWSTemplateFormatVersion': '2010-09-09T00:00:00.000Z',
        'Description': 'CloudFormation config for EC2 Instance ' + \
                       'Connect-oriented Security Group. @s3cpat' + \
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
    d = get_range_data()
    f = filter_range_to_ec2_instance_connect(d)
    if print_full_config:
        print(generate_full_config(f, asyaml=print_as_yaml))
    else:
        if print_as_yaml:
            print(create_cfn_syntax_yaml(f))
        else:
            print(create_cfn_syntax_json(f))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create CloudFormation Resource (Security Group) to ' + \
                    'allow SSH from EC2 Instance Connect IP Ranges. Pulls ' + \
                    'data from https://ip-ranges.amazonaws.com/' + \
                    'ip-ranges.json. Prints as JSON or YAML.')
    parser.add_argument('--yaml', '-y',
                        default=False,
                        action='store_true',
                        help='Print Resource in YAML rather than JSON'
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
