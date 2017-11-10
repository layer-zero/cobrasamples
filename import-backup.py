#!/usr/bin/env python

"""Import a backup file through SCP"""

from getpass import getpass
from cobra.mit.access import MoDirectory
from cobra.mit.request import ConfigRequest
from cobra.mit.session import LoginSession
from cobra.model.file import RemotePath
from cobra.model.config import ImportP, RsImportSource

from requests.packages.urllib3 import disable_warnings
disable_warnings()

default_url = 'https://192.168.221.2'
default_user = 'admin'
default_backuphost = '192.168.221.1'
default_backupuser = 'tom'
default_path = '/Users/tom/Downloads/'
default_filename = 'ce_sim-config-backup.tar.gz'

def get_parameters():
    apic_url = raw_input('Target APIC URL [{}]: '.format(default_url)) or default_url
    apic_user = raw_input('APIC user name [{}]: '.format(default_user)) or default_user
    apic_password = getpass('APIC password: ')
    backup_host = raw_input('Backup host [{}]: '.format(default_backuphost)) or default_backuphost
    backup_user = raw_input('Backup user name [{}]: '.format(default_backupuser)) or default_backupuser
    backup_password = getpass('Backup password: ')
    backup_path = raw_input('Backup path [{}]: '.format(default_path)) or default_path
    backup_filename = raw_input('Backup file name [{}]: '.format(default_filename)) or default_filename
    parameters = {'apic-url': apic_url,
                    'apic-user': apic_user,
                    'apic-password': apic_password,
                    'backup-user': backup_user,
                    'backup-host': backup_host,
                    'backup-password': backup_password,
                    'backup-path': backup_path,
                    'backup-filename': backup_filename}
    return parameters

def create_remote_scp_location(md, target_ip, backup_user, backup_password, backup_path):
    fabricInst = md.lookupByDn('uni/fabric')
    remotepath = RemotePath(fabricInst, 'tmp_location')
    remotepath.protocol = 'scp'
    remotepath.remotePort = '22'
    remotepath.host = target_ip
    remotepath.userName = backup_user
    remotepath.userPasswd = backup_password
    remotepath.remotePath = backup_path
    cr = ConfigRequest()
    cr.addMo(fabricInst)
    md.commit(cr)

def import_backup(md, backup_filename):
    fabricInst = md.lookupByDn('uni/fabric')
    importpolicy = ImportP(fabricInst, 'tmp_import_policy')
    importpolicy.fileName = backup_filename
    importpolicy.importMode = 'atomic'
    importpolicy.importType = 'replace'
    importpolicy.adminSt = 'triggered'
    importsource = RsImportSource(importpolicy, tnFileRemotePathName = 'tmp_location')
    cr = ConfigRequest()
    cr.addMo(fabricInst)
    md.commit(cr)

def delete_backup_location(md, name):
    fabricInst = md.lookupByDn('uni/fabric')
    remotepath = RemotePath(fabricInst, name)
    remotepath.delete()
    cr = ConfigRequest()
    cr.addMo(remotepath)
    md.commit(cr)

def delete_import_policy(md, name):
    fabricInst = md.lookupByDn('uni/fabric')
    importpolicy = ImportP(fabricInst, name)
    importpolicy.delete()
    cr = ConfigRequest()
    cr.addMo(importpolicy)
    md.commit(cr)

def main():
    params = get_parameters()
    loginSession = LoginSession(params['apic-url'], params['apic-user'], params['apic-password'])
    md = MoDirectory(loginSession)
    md.login()
    create_remote_scp_location(md, params['backup-host'], params['backup-user'], params['backup-password'], params['backup-path'])
    print 'Created temporary backup location.'
    import_backup(md, params['backup-filename'])
    print 'Created and triggered import job'
#    delete_import_policy(md, 'tmp_import_policy')
    print 'Deleted import job'
#    delete_backup_location(md, 'tmp_location')
    print 'Deleted temporary backup location'
    md.logout()

if __name__ == '__main__':
    main()