####################################################################
# Description:
#  Creates a host file based on current
#  instances in the amazon aws. Currently it makes no filtering
#  on the instances which means it will generate a host file
#  simply based on the instances that are available to your ec2 account,
#  event those that have been stopped 
# 
# Prerequisites:
#  1. Python 3+
#  2. AWS CLI installed. See AWS site for details
#  3. Make sure you've defined ~/.aws/configure and it contains the
#     entries to your amazon access id and keys. See
#     http://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html
#     for information on how to do this
#  4. Your instances should be in a running state so it could retrieve
#     the public ip address 
#
# Syntax:
#  python create_host_file.py
#
# Output:
#  Empty. It will create a file called hostfile in the directory where
#  it is running
####################################################################

import sys
from utils import get_hosts

class HostFile:
    
    HOST_OUTPUT = "./hostfile"
    ANSIBLE_INVENTORY = "./inventory"
    output = []
    private_ips = []
    public_ips = []
    def main(self):
        hosts = get_hosts(False)
        for host, ips in hosts.items():
            self.private_ips.append({'ip':ips['private_ip'],'host':host})
            self.public_ips.append({'ip':ips['public_ip'],'host':host})

        # push the first entry
        self.private_ips.insert(0, {'ip': '127.0.0.1', 'host': 'localhost'})

        fp = open(self.HOST_OUTPUT, 'w')
        for item in self.private_ips:
            fp.write(item['ip'] + ' ' + item['host'] + "\n")
        
        fp.close()

        self.write_inventory_file();

        print("Done!")

    def write_inventory_file(self):
       fp = open(self.ANSIBLE_INVENTORY, 'w');

       fp.write("[all]\n");
       counter = 1
       for item in self.public_ips:
           fp.write('hdphost%s ansible_host=%s\n' % (counter, item['ip']))
           counter += 1

       fp.write('\n')
       fp.write('[ambari-server]\n')
       fp.write('hdphost1 ansible_host=%s\n\n' % self.public_ips[0]['ip'])

       fp.write('[all:vars]\n')
       fp.write('ansible_ssh_private_key_file=/Users/egleeck/amazon_keypairs/hdp_demo.pem\n')
       fp.write('ansible_user=centos\n')

       fp.close()

if __name__ == '__main__':
    hf = HostFile()
    hf.main()