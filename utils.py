import sys
import subprocess
from subprocess import Popen
import json

def get_hosts_from_aws():
    aws_command = ["aws", "ec2", "describe-instances"]
    proc = Popen(aws_command, stdout=subprocess.PIPE)
    hosts = {}
    output = []
    while True:
        line = proc.stdout.readline()
        if line != ''.encode():
            output.append(line)
        if proc.poll() != None:
            break

    j = json.loads(' '.encode().join(output), encoding='utf-8') 
    
    for item in j['Reservations']:
        for inst in item['Instances']:
            if inst['State']['Name'] in ('running', 'pending'):
                fqdn = inst['PrivateDnsName']
                private_ip = inst['PrivateIpAddress']
                public_ip = inst['PublicIpAddress']
                hosts[fqdn] = {'private_ip':private_ip, 'public_ip':public_ip}
    
    write_amazon_hosts_to_file(hosts, './hosts_from_amazon.txt')

    return hosts

def write_amazon_hosts_to_file(hosts, filename):
    with open(filename, 'w') as fp:
        for host, ips in hosts.items():
            fp.write('%s %s %s\n' % (ips['private_ip'], ips['public_ip'], host))
    
def get_hosts_from_file(filename):

    hosts = {}

    with open(filename, 'r') as fp:
        for line in fp:
            fields = line.split(' ')
            fqdn = fields[2].rstrip()
            private_ip = fields[0]
            public_ip = fields[1]
            hosts[fqdn] = {'private_ip':private_ip, 'public_ip':public_ip}
    
    return hosts

def get_hosts(from_local_file=True):

    if from_local_file:
        return get_hosts_from_file('./hosts_from_amazon.txt')
    else:
        return get_hosts_from_aws()
 