#!/usr/bin/env python

"""Obtain serial numbers of ACI fabric nodes using the Cobra SDK"""

from cobra.mit.access import MoDirectory
from cobra.mit.request import ClassQuery
from cobra.mit.session import LoginSession

from requests.packages.urllib3 import disable_warnings

disable_warnings()

apic_url = 'https://apic1.dcloud.cisco.com'
apic_user = 'admin'
apic_password = 'C1sco12345'

login_session = LoginSession(apic_url, apic_user, apic_password)
md = MoDirectory(login_session)
md.login()

cq = ClassQuery('fabricNode')
nodes = md.query(cq)

sorted_nodes = sorted(nodes, key=lambda node: node.name)

print '\nNode name : Serial number\n'

for node in sorted_nodes:
    print '{0:9} : {1} '.format(node.name, node.serial)

md.logout()
