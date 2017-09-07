#!/usr/bin/env python

"""Obtain serial numbers of ACI fabric nodes using the Cobra SDK"""

from cobra.mit.access import MoDirectory
from cobra.mit.request import ClassQuery
from cobra.mit.session import LoginSession

from requests.packages.urllib3 import disable_warnings

__author__ = 'Tom Lijnse'
__version__ = '0.1'

disable_warnings()

apic_url = 'https://192.168.221.2'
apic_user = 'admin'
apic_password = '1234QWer'

login_session = LoginSession(apic_url, apic_user, apic_password)
md = MoDirectory(login_session)
md.login()

cq = ClassQuery('fabricNode')
nodes = md.query(cq)

sorted_nodes = sorted(nodes, key = lambda node: node.name)

print '\nNode name : Serial number\n'

for node in sorted_nodes:
    print '{0:9} : {1} '.format(node.name, node.serial)

md.logout()
