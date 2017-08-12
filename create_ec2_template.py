from jinja2 import Environment, FileSystemLoader
from utils import get_hosts
import os
   

def main():

    values = dict(
            volume_size = os.environ['EC2_VOLUME_SIZE'],
            instance_type = os.environ['EC2_INSTANCE_TYPE'],
            key_name = os.environ['EC2_KEYNAME'],
            tags = {
                "Business Unit": os.environ['EC2_TAG_BUSINESS_UNIT'],
                "Procuct": os.environ['EC2_TAG_PRODUCT'],
                "End Date": os.environ['EC2_TAG_END_DATE'],
                "Service": os.environ['EC2_TAG_SERVICE'],
                "Owner": os.environ['EC2_TAG_OWNER']
            }
        )

    TEMPLATE_OUTPUT = './ec2-template.json'
    env = Environment(loader=FileSystemLoader('./templates'))
    temp = env.get_template('ec2-template.jinja2')
    
    hosts = get_hosts()
    
    fp = open(TEMPLATE_OUTPUT, 'w')
    fp.write(temp.render(values=values))
    fp.close()

if __name__ == '__main__':
	main()


