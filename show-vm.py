from cobra.mit.access import *
from cobra.mit.request import *
from cobra.mit.session import *

from getpass import *

from requests.packages.urllib3 import disable_warnings
disable_warnings()


apicUrl = raw_input("Target apic URL [https://192.168.10.1]: ") or "https://192.168.10.1"
apicUser = raw_input("Apic user name [admin]: ") or "admin"
apicPassword = getpass("Apic password: ")
vmName = raw_input("VM name [Web]: ") or "Web"

loginSession = LoginSession(apicUrl, apicUser, apicPassword)
md = MoDirectory(loginSession)
md.login()

cq = ClassQuery('compVm')
cq.subtree = 'full'
cq.propFilter = 'eq(compVm.name, "{}")'.format(vmName)
vms = md.query(cq)

for vm in vms:
    dnq = DnQuery(list(vm.rshv)[0].tDn)
    dnq.subtree = 'full'
    hv = md.query(dnq)[0]

    print '\nVirtual Machine Name:   {}'.format(vm.name)
    print 'Operating System:       {}'.format(vm.cfgdOs)
    print '\nHypervisor Name:        {}'.format(hv.name)
    print 'dvSwitch Name:          {}'.format(list(list(hv.dn.rns)[-2].namingVals)[0])

    vnics = list(vm.vnic)
    for vnic in vnics:        
        print '\nVnic {}'.format(vnics.index(vnic)+1)
        print '  Vnic Name:            {}'.format(vnic.name)
        print '  Vnic IP Adress:       {}'.format(vnic.ip)
        print '  Vnic MAC Address:     {}'.format(vnic.mac)
        cq = ClassQuery("fvCEp")
        cq.subtree = 'full'
#        cq.propFilter = 'eq(fvCEp.mac, "{}")'.format(vnic.mac)
#        Note: Normally it would be better to do this lookup by mac instead of IP, but in the FL lab the MACs are not unique, while the IP addresses are.
        cq.propFilter = 'eq(fvCEp.ip, "{}")'.format(vnic.ip)
        eps = md.query(cq)
        if len (eps)==0:
            print '  This Vnic is not currently present in the ACI fabric.'
        else:
            ep = eps[0]
            rns = list(ep.dn.rns)
            print '  Tenant:               {}'.format(list(rns[-4].namingVals)[0])
            print '  Application Profile:  {}'.format(list(rns[-3].namingVals)[0])
            print '  Endpoint Group:       {}\n'.format(list(rns[-2].namingVals)[0])

md.logout()
