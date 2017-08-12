#!/bin/bash
# Script wraps all the individual calls to create the cluster
# This will get refactored to make it more coherent

# This contains all the variables required
echo "=== Configuration Environment variables ==="
source ./settings.sh

# Activate conda
echo "=== Activating aws ==="
source activate aws

echo "=== Create the instances template ==="
python ./create_ec2_template.py

# Create the instances in amazon
echo "=== Create the instances in amazon ==="
source ./launch_instances.sh
exit

# The above takes a while for the instances to be 'ready'
echo "=== Sleep for 3 minutes ==="
sleep 180
#read -p "Make sure instances are running. Press enter to continue"

# Create the hostfile which will be uploaded to /etc/hosts on 
# the instances
echo "=== Create the hostfile ==="
python ./create_host_file.py

# Use ansible to prepare the OS
echo "=== Use ansible to prepare the OS ==="
source ./launch_playbook.sh

# Create the blueprint for ambari
echo "=== Create the blueprint for ambari ==="
python ./create_blueprint.py

# Amabri agent/server specific settings - get the hostname of
# the ambari server
ambari_host=$(sed '2q;d' hostfile | awk -F" " '{print $2}')

# Point ambari agent to the ambari server
echo "=== Point ambari agent to the ambari server ==="
ansible all -m shell -a "ambari-agent reset $ambari_host" -b -i inventory
ansible all -m shell -a "ambari-agent start" -b -i inventory

# Upload the blueprints
ambari_public_ip=$(sed '2q;d' inventory | awk -F" " '{print $2}' | awk -F"=" '{print $2}')
bash launch_create_blueprint.sh $ambari_public_ip