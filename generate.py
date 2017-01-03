#!/opt/local/bin/python3
# must use python 3
# usage: 
#
# ./generate [starting IPv4 Address] [input file]
#
# Example: 
#
# ./generate 10.101.6.1 sourcedata.txt
#
#
# Input file should be plain text (no header line) with format: 
#
# <computer name><tab><MAC Address>
#
#

import sys
import uuid
import re
import string


# take arg1 and split into octets
(octet1, octet2, octet3, octet4) = sys.argv[1].split('.', maxsplit=4)

# convert third and fourth octets into ints so we can do addition
octet3num = int(octet3)
octet4num = int(octet4)
counter = 0

# template for plist file that will go into /private/var/db/dslocal/nodes/Default/computers
compTemplate = string.Template(
'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>en_address</key>
	<array>
		<string>$EN_ADDRESS</string>
	</array>
	<key>generateduid</key>
	<array>
		<string>$UUID</string>
	</array>
	<key>ip_address</key>
	<array>
		<string>$IP_ADDRESS</string>
	</array>
	<key>ipaddressandenetaddress</key>
	<array>
		<string>$IP_ADDRESS/$EN_ADDRESS</string>
	</array>
	<key>name</key>
	<array>
		<string>$COMPUTER_NAME</string>
	</array>
</dict>
</plist>''')

# Process source file
infile = open( sys.argv[2] )
for oneline in infile:

    (computerName, macAddress) = oneline.strip().split( "\t" )
    
    # make sure computer name has only letters, numbers, and dashes
    computerNameClean = re.sub( "[^0-9A-Za-z]", "-", computerName )
    outputFileName = computerNameClean + ".plist"
    uniqueId = uuid.uuid4()
    
    # generate IPv4 address
    ipAddress = ".".join( [ octet1, octet2, str(octet3num), str(octet4num) ] )
    
    
#    print( compTemplate.safe_substitute( EN_ADDRESS=macAddress, UUID=uniqueId, 
#        IP_ADDRESS=ipAddress, COMPUTER_NAME=computerNameClean ) )
    
    # open an output file, write the template, close it
    oneOutput = open( outputFileName, "w" )
    oneOutput.writelines( compTemplate.safe_substitute( EN_ADDRESS=macAddress, UUID=uniqueId, 
        IP_ADDRESS=ipAddress, COMPUTER_NAME=computerNameClean ) )
    oneOutput.close()
    
#     print( computerName )
#     print( outputFileName )
#     print( macAddress )
#     print( ipAddress )
#     print( uniqueId )

    # increment IP address, halt if we exceed 2 octets worth
    octet4num += 1
    if octet4num > 255:
        octet4num = 0
        octet3num += 1
    if octet3num > 255:
        sys.exit()

