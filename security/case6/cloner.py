import csv
from opcua import Client, ua

client = Client("opc.tcp://localhost:4840")
client.connect()
client.load_type_definitions()  # load definition of server specific structures/extension objects

def upcua_tree(node):
    children = client.get_node(node).get_children()

    for child in children:
        print(child.get_children())





def get_upcua_tree(node):
    children = client.get_node(node).get_children()
    
    for child in children:
        nodeid=str(child)
        children_data=child.get_children()
        browse_name=child.get_browse_name()
        name=child.get_browse_name().Name
        print(child, browse_name, name)
        try:
            attributes=child.get_attribute(ua.AttributeIds.Value)
        except:
            attributes="no_attributes"
        Display_Name=child.get_display_name()
        try:
            Description=child.get_description()
        except:
            Description="no_description"
        try:
            Data_Type=child.get_data_type()
        except: 
            Data_Type="no_data_type"
        try:
            Data_Value=child.get_data_value()
        except:
            Data_Value="no_data_value"
        try:
            Node_ID=child.get_node_id()
        except: 
            Node_ID="no_node_id"
        try:    
            Node_Class=child.get_node_class()
        except:
            Node_Class="no_node_class"
        try:    
            Parent=child.get_parent()
        except:
            Parent="no_parent"
        try:
            References=child.get_references()
        except:
            References="no_references"
        try:
            Type_Definition=child.get_type_definition()
        except:
            Type_Definition="no_type_definition"
        try:
            User_WriteMask=child.get_user_write_mask()
        except:
            User_WriteMask="no_user_write_mask" 

        try:
            Value=child.get_value()
        except:
            Value="no_value"
        

        # Save the data to the CSV file
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([nodeid, children_data, browse_name, name, attributes, Display_Name, Description, Data_Type, Data_Value, Node_ID, Node_Class, Parent, References, Type_Definition, User_WriteMask, Value])
            print("Data saved to the CSV file.")
        
        # Recursively call the function to get the children of the current node
        get_upcua_tree(child)


csv_file = 'procsys.csv'

# Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
root = client.get_root_node()
print("Root node is: ", root)
objects = client.get_objects_node()
print("Objects node is: ", objects)

# Node objects have methods to read and write node attributes as well as browse or populate address space
print("Children of root are: ", root.get_children())


upcua_tree(root)
