''' Ex1 - use string methods only

Given this poem "Je n’ai pas oublié, voisine de la ville" of Charles Baudelair:

poem = """
I’ve not forgotten, near to the town,
our white house, small but alone:
its Pomona of plaster, its Venus of old
hiding nude limbs in the meagre grove,
and the sun, superb, at evening, streaming,
behind the glass, where its sheaves were bursting,
a huge eye in a curious heaven, present
to gaze at our meal, lengthy and silent,
spreading its beautiful candle glimmer
on the frugal cloth and the rough curtain.
"""

Q1: how many letter "s" there are in the poem?
Q2: how many lines does the poem have?
Q3: replace all space characters with '_'
Q4: capitalize all characters of the poem
'''

###################################################

''' Ex2 - use Regular Expression only (import re)

Given this log server data:

log_server = """
127.0.0.1 - - [12/May/2023:06:25:24 +0000] "GET /index.html HTTP/1.1" 200 1043
192.168.0.5 - - [13/May/2023:14:02:01 +0000] "POST /login.php HTTP/1.1" 403 721
10.0.0.2 - - [14/May/2023:19:45:09 +0000] "GET /dashboard HTTP/1.1" 500 2101
203.0.113.4 - - [15/May/2023:21:12:43 +0000] "DELETE /account/12345 HTTP/1.1" 200 0
"""

Q1: Write a regular expression pattern to extract all the IP addresses
=> Expected output: ['127.0.0.1', '192.168.0.5', '10.0.0.2', '203.0.113.4']

Q2: Write a regular expression pattern to extract full date and time
=> Expected output: ['12/May/2023:06:25:24', '13/May/2023:14:02:01', '14/May/2023:19:45:09', '15/May/2023:21:12:43']

Q3: Write a regular expression pattern to extract URLs
=> Expected output: ['/index.html', '/login.php', '/dashboard', '/account/12345']
'''
