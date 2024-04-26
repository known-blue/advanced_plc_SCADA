from subprocess import run
import time
import json
import requests
from datetime import datetime


class Node():
    def __init__(self, name, type, interface):
        self.name = name # Name of the node
        self.type = type # What type of node is it
        self.interface_name = interface # The name of the interface
        self.interface = self.get_interface(interface) # The details of the interface
        self.info = self.get_info(name, type) # Other node information

    def get_interface(name) -> str:
        out = run(["ros2","interface","show",name], capture_output=True)
        return out.stdout 

    def get_info(node_name, type) -> str:
        out = run(["ros2",type,"info",node_name], capture_output=True)
        return out.stdout


def get_nodes_from_X_type(type) -> list: 
    node_list = []
    out = run(["ros2",type,"list","-t"], capture_output=True)
    for node in out.stdout.split('\n'): # Split to get individual nodes and get this string: /node_name [node_type]
        temp = node.split() # split to break up name from type
        node_list.append(Node(temp[0],type,temp[1][1:-1])) #splice to remove []
    return node_list


def create_data_structure_for_cache(list) -> dict:
    # Creating tag dictionary
    # IE: {'In hand': True, "In auto": False}

    result_dict = {}
    # Iterate through unknown number of objects
    for node in list:
        result_dict[node.name] = [node.type, node.interface_name, 
                                  node.interface, node.info]

    return result_dict


def send_data_to_webserver(data_dict, session) -> None:
    # Convert from python dict to JSON string
    # to be able to send to our django web server
    json_string = json.dumps(data_dict)

    # This is the site you are trying to send to
    site_url = 'http://localhost:8000/receive-data/'
    # These are some headers for your browser, I wouldn't worry about these
    headers = {'User-Agent': 'Mozilla/5.0'}

    # This is sending the data to the webserver
    r = session.post(site_url, data=json_string, headers=headers)

    # This is the webservers response, which if it is working
    # should be a response code of 200
    print(r.status_code)


def main():
    node_list = []
    
    # Create a session with our webserver to speed things up
    session = requests.Session()

    # Check for all nodes currently brodcasting
    node_list.append(get_nodes_from_X_type('action'))
    node_list.append(get_nodes_from_X_type('topic'))
    node_list.append(get_nodes_from_X_type('service'))

    # Run forever
    while True:
        # setup tag dictionary with unlimited nodes
        node_dict = create_data_structure_for_cache(node_list)
        send_data_to_webserver(node_dict, session)

        new_node_catcher = []
        # Check for all nodes currently brodcasting and catch any new nodes
        new_node_catcher.append(get_nodes_from_X_type('action'))
        new_node_catcher.append(get_nodes_from_X_type('topic'))
        new_node_catcher.append(get_nodes_from_X_type('service'))
        # Set all nodes found into the old list to be sent next loop around
        node_list = new_node_catcher


if __name__ == '__main__':
    main()
