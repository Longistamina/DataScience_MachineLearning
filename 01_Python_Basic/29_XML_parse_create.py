'''
XML stands for eXtensible Markup Language.

It is a markup language that defines a set of rules for encoding documents in a format that is
both human-readable and machine-readable.

XML is designed to store and transport data, and it is often used in web services, configuration files,
and data interchange between systems.

XML is similar to HTML, but it is more flexible and allows users to define their own tags.

XML is structured as a tree, with elements represented by tags.
Python provides several libraries to work with XML, including `xml.etree.ElementTree`, `lxml`, and `minidom`.

The `xml.etree.ElementTree` module is part of the Python standard library 
and provides asimple and efficient way to parse and create XML documents.
'''

import xml.etree.ElementTree as ET

parent_dir = "/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/xml_files"


#------------------------------------------------#
#-------------- XML file structure --------------#
#------------------------------------------------#
'''
<?xml version="1.0" encoding="UTF-8"?>    (This line tells the computer that we are using XML, the content version is 1.0, with UTF-8 encoding)

<CATALOG>   (This is the start of the Root Element. Each XML file has ONLY ONE Root Element)

  <CD>      (This is the start of a Child Element. Each Child Element can also have their own Child Elements. But should not > 3 levels)

    <TITLE>Empire Burlesque</TITLE>   (This is the Child Element of element <CD>, which is also a child element itself)

    <ARTIST>Bob Dylan</ARTIST>

    <COUNTRY>USA</COUNTRY>

    <COMPANY>Columbia</COMPANY>

    <PRICE>10.90</PRICE>

    <YEAR>1985</YEAR>

  </CD>

</CATALOG> (This is the end of the Root Element. Agian, each XML file has ONLY ONE Root Element)
'''

# Start an element: <element_name>
#                      contents ......................
#                      contents ......................
#                      contents ......................
# End an element:   </element_name>

# Element can also be called as "Node"

# The Element/Node level should not exceed 3
#     <Root_Element>
#      <Child_Element_Level_1>
#       <Child_Element_Level_2>
#        <Child_Element_Level_3>


#-----------------------------------------------------#
#-------------- Read and Parse XML file --------------#
#-----------------------------------------------------#

##################################################
## Parse an XML file into an ElementTree object ##
##################################################

# Parse the XML file into tree_food variable
# The parse() function reads the XML file and creates an ElementTree object
tree_food = ET.parse(f'{parent_dir}/food.xml')
print(tree_food) # <xml.etree.ElementTree.ElementTree object at 0x7fb02723bc50>


# Get the root element of the XML file
# The getroot() function returns the root element of the XML tree
root_food = tree_food.getroot()
print(root_food) # <Element 'breakfast_menu' at 0x7fb027162cf0>


# Get basic information about the root element
print(f"Root Element: {root_food.tag}") # Root Element name: breakfast_menu
print(f"Root Element Attributes: {root_food.attrib}") # Root Element Attributes: {} (empty dictionary means no attributes)
print(f"Root Element Text: {root_food.text}") # Root Element Text: None (no text content directly under the root element)
print(f"Root Element Tail: {root_food.tail}") # Root Element Tail: None (no tail text after the root element)
print(f"Root Element Children: {list(root_food)}") # Root Element Children: 
                                                   # [
                                                   # <Element 'food' at 0x7fb027162d60>, 
                                                   # <Element 'food' at 0x7fb027162db0>, 
                                                   # ...]

# Get the number of child elements of the root element
num_children = len(list(root_food))
print(f"Number of Child Elements: {num_children}") # Number of Child Elements: 5


########################################
## Parse a XML string into XML object ##
########################################

xml_string = '''<?xml version="1.0"?>
<student>
    <name>Alice Johnson</name>
    <age>20</age>
    <major>Computer Science</major>
</student>'''

root_string = ET.fromstring(xml_string)
print(f"Student name: {root_string.find('name').text}")
