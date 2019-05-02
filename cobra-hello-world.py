#!/usr/bin/env python

"""Demo some basic tasks in ACI using the Cobra SDK"""

from cobra.mit.access import MoDirectory
from cobra.mit.request import ClassQuery
from cobra.mit.request import ConfigRequest
from cobra.mit.session import LoginSession
from cobra.model.fv import Tenant

from requests.packages.urllib3 import disable_warnings
disable_warnings()

# Define the URL and credentials for the APIC
apic_url = 'https://apic1.dcloud.cisco.com'
apic_user = 'admin'
apic_password = 'C1sco12345'

# Login to the APIC
loginSession = LoginSession(apic_url, apic_user, apic_password)
md = MoDirectory(loginSession)
md.login()

# Obtain the list of tenants and print their names
cq = ClassQuery('fvTenant')
tenants = md.query(cq)

for tenant in tenants:
        print tenant.name

raw_input('Press Enter to continue...')

# Define a new tenant
polUni = md.lookupByDn('uni')
tenant = Tenant(polUni, 'Some-New-Tenant')
tenant.descr = 'This tenant was created by cobra'

# Push the new tenant configuration to the APIC
cr = ConfigRequest()
cr.addMo(polUni)
md.commit(cr)

raw_input('Press Enter to continue...')

# Delete the newly created tenant
tenant.delete()

cr = ConfigRequest()
cr.addMo(polUni)
md.commit(cr)

# Log out of the APIC
md.logout()
