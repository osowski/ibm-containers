## extract-vcap.py
##
## Usage: python extract-vcap.py <service name> <index> <json-formatted property name>
##
## This script will extract the specified parameter information from the VCAP_SERVICES environment
## variable that is embedded in the container instance, when it is started and bound to an IBM Bluemix
## application.  If the parameter is found, the script returns a return code of 0 and outputs the value
## to STDOUT.  If the parameter is not found, the script returns a return code of 1 and outputs the
## failure to STDERR.
## Example:
##		$ TEMP=`python extract-vcap.py DataWorks 0 credentials.password`
##		$ echo $?
##		0
##		$ export DW_PASSWORD=${TEMP}
##		$ echo $DW_PASSWORD
##		XYZ123abc789
##
##

import sys
import os
import json


if len(sys.argv)!=4:
  sys.stderr.write(("Required parameters missing.  4 parameters are required. {0} paremeters provided.").format(len(sys.argv)))
  sys.stderr.write("Usage:  python extract-vcap.py <service_name> <service_index> <property_name in dot syntax>")
  sys.exit(1);
  
servicename = sys.argv[1]
serviceindex = int(sys.argv[2])
propertystring = sys.argv[3]

if "VCAP_SERVICES" in os.environ:
  vcaps = json.loads(os.environ["VCAP_SERVICES"])
  if servicename in vcaps:
    #print "Found service {0}".format(servicename)
    if len(vcaps[servicename]) > serviceindex:
      #print "Found service index {0} for service {1}".format(serviceindex, servicename)
      ## Convert json-formatted property string to extrapolated values
      props = propertystring.split(".")
      obj = vcaps[servicename][serviceindex]
      try:
        for element in props:
          obj = obj[element]
        sys.stdout.write(obj)
      except:
        sys.stderr.write("Element {0} not found in property {1}".format(element, propertystring))
        sys.exit(1)
    else:
      sys.stderr.write("Service index {0} not found for service {1}".format(serviceindex, servicename))
      sys.exit(1)
  else:
    sys.stderr.write("Service {0} not found".format(servicename))
    sys.exit(1)
else:
  sys.stderr.write("VCAP_SERVICES not found")
  sys.exit(1)

