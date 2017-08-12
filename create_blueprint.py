from jinja2 import Environment, FileSystemLoader
from utils import get_hosts
   

def main():

    TEMPLATE_OUTPUT = './blueprint-template.json'
    env = Environment(loader=FileSystemLoader('./templates'))
    temp = env.get_template('blueprint-template.jinja2')
    
    hosts = get_hosts()
    
    fp = open(TEMPLATE_OUTPUT, 'w')
    fp.write(temp.render(hosts=hosts))
    fp.close()

    # Create the blueprint
    TEMPLATE_OUTPUT = './blueprint.json'
    env = Environment(loader=FileSystemLoader('./templates'))
    temp = env.get_template('blueprint.jinja2')

    fp = open(TEMPLATE_OUTPUT, 'w')
    fp.write(temp.render())
    fp.close()

if __name__ == '__main__':
	main()


