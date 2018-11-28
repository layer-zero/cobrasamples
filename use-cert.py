#!/usr/bin/env python
from cobra.mit.session import CertSession
from cobra.mit.access import MoDirectory
from cobra.mit.request import ClassQuery

from requests.packages.urllib3 import disable_warnings
disable_warnings()

def readFile(fileName=None, mode="r"):
    if fileName is None:
        return ""
    fileData = ""
    with open(fileName, mode) as aFile:
        fileData = aFile.read()
    return fileData

pkey = readFile("cobra.key")
csession = CertSession("https://sandboxapicdc.cisco.com/",
                       "uni/userext/user-cobra/usercert-cobra", pkey)

modir = MoDirectory(csession)

cq = ClassQuery('fvTenant')
tenants = modir.query(cq)

for tenant in tenants:
        print tenant.name

modir.logout()
