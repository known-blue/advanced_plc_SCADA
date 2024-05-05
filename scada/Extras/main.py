from subprocess import run
import time
import json
import requests
from datetime import datetime


class Node():
    def __init__(self, name, Thetype, interface):
        self.name = name # Name of the node
        self.nodeType = Thetype # What type of node is it
        self.interface_name = interface # The name of the interface
        self.interface = self.get_interface(interface) # The details of the interface
        self.info = self.get_info(name, Thetype) # Other node information
        self.curData = ''
        if Thetype == 'topic':
            if name == '/rosout' or name == '/parameter_events':
                # These are 2 of ROS's topics, they don't give out messages frequently 
                # Plus they aren't usually very important for us lol
                pass
            else:
                self.curData = self.get_topic(name)

    def get_interface(self, name) -> str:
        out = run(["ros2","interface","show",name], capture_output=True, text=True)
        return out.stdout 

    def get_info(self, node_name, theType) -> str:
        out = run(["ros2",theType,"info",node_name], capture_output=True, text=True)
        return out.stdout
    
    def get_topic(self, node_name):
        out = run(["ros2","topic","echo","--once",node_name], 
                  capture_output=True, text=True)
        return out.stdout

def get_nodes_from_X_type(theType) -> list: 
    node_list = []
    out = run(["ros2",theType,"list","-t"], capture_output=True, text=True)
    for node in out.stdout.split("\n"): # Split to get individual nodes and get this string: /node_name [node_type]
        if not node: # If empty
             break
        temp = node.split() # split to break up name from type
        node_list.append(Node(temp[0],theType,temp[1][1:-1])) #splice to remove []
    return node_list


def create_data_structure_for_cache(thelist) -> dict:
    # Creating tag dictionary
    # IE: {'In hand': True, "In auto": False}

    result_dict = {}
    # Iterate through unknown number of objects
    for node in thelist:
        for i in range(0,len(node)):
            result_dict[node[i].name] = [node[i].nodeType, node[i].interface_name, 
                                         node[i].interface, node[i].info,
                                         node[i].curData]
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


def main(session):
    node_list = []

    # Check for all nodes currently brodcasting
    print("Getting actions....")
    node_list.append(get_nodes_from_X_type('action'))
    print("Getting topics....")
    node_list.append(get_nodes_from_X_type('topic'))
    print("Getting services....")
    node_list.append(get_nodes_from_X_type('service'))

    # Run forever
    while True:
        # setup tag dictionary with unlimited nodes
        node_dict = create_data_structure_for_cache(node_list)
        send_data_to_webserver(node_dict, session)

        new_node_catcher = []
        # Check for all nodes currently brodcasting and catch any new nodes
        print("Getting actions....")
        new_node_catcher.append(get_nodes_from_X_type('action'))
        print("Getting topics....")
        new_node_catcher.append(get_nodes_from_X_type('topic'))
        print("Getting services....")
        new_node_catcher.append(get_nodes_from_X_type('service'))
        # Set all nodes found into the old list to be sent next loop around
        node_list = new_node_catcher


if __name__ == '__main__':
     # Create a session with our webserver to speed things up
    session = requests.Session()
    try:
        main(session)
    except KeyboardInterrupt:
        # Send a blank to reset all data
        node_dict = {'blank':['','','','','']}
        send_data_to_webserver(node_dict, session)