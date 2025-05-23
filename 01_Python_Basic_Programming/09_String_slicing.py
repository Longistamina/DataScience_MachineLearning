name = "Le Anh Thu"
l = len(name)
first_element = name[0] #---> L
fourth_element = name[3] #---> A

last_element = name[-1] #---> u
name[l-1] #---> u

#Python considers 0 as the index of the first element of an iterator

family_name = name[0:2] #stop at element of index 2, but not include it 
family_name = name[:2]

middle_name = name[3:6]

given_name = name[7:]

strNumbers="123456789"
strOdd = strNumbers[0::2] # slice from start to end, but with index step = 2, return "13579"
strEven = strNumbers[1::2]  # slice from the second element to end, but with index step = 2, return "2468"

print("-"*50) #print character '-' 50 times
print()