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
print(f"Root Element: {root_food.tag}") # "tag" is the name of that element: breakfast_menu (like "key" in dictionary)
print(f"Root Element Attributes: {root_food.attrib}") # Root Element Attributes: {} (empty dictionary means no attributes)
print(f"Root Element Text: {root_food.text}") # Text (like value in dict): None (no text content directly under the root element)
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
print(f"Student name: {root_string.find('name').text}") # Alice Johnson


#-----------------------------------------------------------------------#
#------------ A custom function to summarize XML structure -------------#
#-----------------------------------------------------------------------#

def summarize_xml_structure(element, level=0):
    indent = "  " * level
    print(f"{indent}{element.tag}")
    for child in element:
        summarize_xml_structure(child, level + 1)

# Use with your XML:
summarize_xml_structure(root_food)


#-----------------------------------------------#
#-------------- Navigate XML tree --------------#
#-----------------------------------------------#

# <breakfast_menu>
#   <food>
#     <name>Belgian Waffles</name>
#     <price>$5.95</price>
#     <description>Two of our famous Belgian Waffles with plenty of real maple syrup</description>
#     <calories>650</calories>
#   </food>
# .....
# </breakfast_menu>

tree_food = ET.parse(f'{parent_dir}/food.xml')
root_food = tree_food.getroot()


# Find single element (fist occurrence)
print(root_food.find("food")) # <Element 'food' at 0x7f4f7e87bab0> (first occurrence of <food> under <breakfast_menu>)

print(root_food.find("food/name").text) # Belgian Waffles (first occurrence of <name> under <food>)


# Find all elements with the tag "food"
food_items = root_food.findall("food")
print(food_items)
# [<Element 'food' at 0x7f4f7e87bab0>, <Element 'food' at 0x7f4f7e87bc40>, <Element 'food' at 0x7f4f7e87be20>, <Element 'food' at 0x7f4f7e88c040>, <Element 'food' at 0x7f4f7e88c1d0>]


#------------------------------------------------------------#
#-------------- Loop through XML tree elements --------------#
#------------------------------------------------------------#

tree_food = ET.parse(f'{parent_dir}/food.xml')
root_food = tree_food.getroot()
food_items = root_food.findall("food")

##################################
## Iterate with .find(...).text ##
##################################

for food in food_items:
    name = food.find("name").text
    price = food.find("price").text
    print(f"Food Name: {name} _____ Price: {price}")
# Food Name: Belgian Waffles
# Food Name: Strawberry Belgian Waffles
# Food Name: Berry-Berry Belgian Waffles
# Food Name: French Toast
# Food Name: Homestyle Breakfast


################################################
## Iterate using element.tag and element.text ##
################################################

for food_element in root_food:
    string_out = ""
    for food_subelement in food_element:
      if food_subelement.tag == "description": # Ignore an unwanted subelement
          continue
      string_out += f"{food_subelement.tag}: {food_subelement.text} ||| "
    print(string_out.rstrip(" "))   
# name: Belgian Waffles ____ price: $5.95 ____ calories: 650
# name: Strawberry Belgian Waffles ____ price: $7.95 ____ calories: 900
# name: Berry-Berry Belgian Waffles ____ price: $8.95 ____ calories: 900
# name: French Toast ____ price: $4.50 ____ calories: 600
# name: Homestyle Breakfast ____ price: $6.95 ____ calories: 950


#------------------------------------------------------------#
#-------------- Create XML object from scratch --------------#
#------------------------------------------------------------#

######################################
## Create new XML tree from scratch ##
######################################

import xml.etree.ElementTree as ET

# Create the root element with the tag "STARWARS"
root_starwars = ET.Element("STARWARS")


# Add the first child element with the tag "CHARACTER" 
# (as well as the first observation, like the first row in a dataframe)
character_1 = ET.SubElement(root_starwars, "CHARACTER")
ET.SubElement(character_1, "Name").text = "Padmé Amidala" # Add subelement "Name" for the character_1 element
ET.SubElement(character_1, "Gender").text = "F"           # Add subelement "Gender" for the character_1 element
ET.SubElement(character_1, "Age").text = "27"             # Add subelement "Age" for the character_1 element
ET.SubElement(character_1, "Job").text = "Queen of Naboo" # Add subelement "Job" for the character_1 element
ET.SubElement(character_1, "Income", currency = "$").text = "45000" # Add subelement "Income" for the character_1 element with currency


# Add the second child element also with the tag "CHARACTER" 
# (as well as the second observation, like the second row in a dataframe)
character_2 = ET.SubElement(root_starwars, "CHARACTER")
ET.SubElement(character_2, "Name").text = "Anakin Skywalker"
ET.SubElement(character_2, "Gender").text = "M"
ET.SubElement(character_2, "Age").text = "22"
ET.SubElement(character_2, "Job").text = "Jedi"
ET.SubElement(character_2, "Income", currency = "$").text = "23450"


# Create the XML tree from the defined root element
tree_starwars = ET.ElementTree(root_starwars)

print(tree_starwars) # <xml.etree.ElementTree.ElementTree object at 0x7f4f7e8856a0>


###############################
## Loop through new xml tree ##
###############################
root_starwars = tree_starwars.getroot()

for character_element in root_starwars:
    string_out = ""
    for character_subelement in character_element:
        string_out += f"{character_subelement.tag}: {character_subelement.text} ||| "
    print(string_out.rstrip(" "))


#-------------------------------------------------------------------#
#-------------- Write a XML tree object into XML file --------------#
#-------------------------------------------------------------------#

# Add indentation before writing
ET.indent(tree_starwars, space="  ", level = 0)

# tree.write() to save a xml tree to a .xml file
tree_starwars.write(
    f"{parent_dir}/new_written_starwars.xml", 
    encoding = 'utf-8', 
    xml_declaration = True,
)