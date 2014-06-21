#!/usr/bin/env python

# create user if not exists
import re
import subprocess
import fileinput
import os
import errno
import shutil
import sys
import time
import crypt


class User():
    def __init__(self, username, domain, web_root, passwd=None, home=None, shell=None):
        self.username = username
        self.domain = domain
        self.web_root = web_root
        self.passwd = passwd
        self.home = home
        self.shell = shell
        self.array = []
        self.backups = ['/etc/pam.d/sshd',
                        '/etc/ssh/sshd_config',
                        '/etc/fstab']

    def checkRoot(self):
            """
            check to make sure its ran as root
            """
            user = os.geteuid()
            if user != 0:
                print "You must be logged in as root or use sudo to run me"
                sys.exit(0)
            else:
                return True

    def scanFile(self, file, string, array=None):
        """
        open specific file and find exact matches of $string, returns boolean
        """
        self.array = []
        regex = re.compile('\\b'+string+'\\b')
        with open(file, 'r') as lines:
            for line in lines:
                match = regex.findall(line)
                if len(match) > 0:
                    if array:
                        self.array.append(line)
                    return True
        return False

    def addField(self, string):
        """
        main function for creating for executing shell commands
        accepts string only format, eg:
        'useradd -G sftponly -s /bin/false username'
        """
        add = subprocess.Popen(string.split(),
                               stdout=subprocess.PIPE,
                               )
        output, error = add.communicate()

    def appendToFile(self, file, append):
        """
        appends Match Group sftponly fields to /etc/ssh/sshd_config
        """
        with open(file, 'a') as insert:
            insert.write(append)
            insert.close()

    def mkBackup(self, file_name):
        """
        make backup of file before editing
        """
        shutil.copyfile(file_name, "{0}.sftp.bak".format(file_name))

    def getHomeDir(self):
        """
        Gets users home dir if user is already created
        """
        self.checkUser()
        self.home = self.array[0].split(':')[5]

    def checkUser(self):
        """
        returns boolean if user exists
        """
        match = "\A{0}".format(self.username)
        return self.scanFile('/etc/passwd', match, array=1)

    def checkGroup(self):
        """
        returns boolean if group exists
        """
        return self.scanFile('/etc/group', 'sftponly')

    def checkMatchGroup(self):
        """
        returns boolean if sftponly match group has been created
        """
        self.scanFile('/etc/ssh/sshd_config',
                      "Subsystem\s+sftp\s+internal-sftp", array=1)
        if len(self.array) > 0:
            return True
        return False

    def checkFstab(self):
        """
        check to see if the bindmount is already added in fstab
        BROKEN
        """
        bind = "{0}\s+{1}/{2}\s+none\s+bind\s+0\s+0".format(
            self.web_root,
            self.home,
            self.domain,
            )
        self.scanFile('/etc/fstab',
                      bind,
                      array=1
                      )
        if len(self.array) > 0:
            return True
        return False

    def checkPam(self):
        """
        returns boolean if umask is set for pam.d
        """
        self.scanFile('/etc/pam.d/sshd',
                      "session\s+optional\s+pam_umask.so\s+umask=0002",
                      array=1
                      )
        if len(self.array) > 0:
            return True
        return False

    def createBackups(self):
        for backup in self.backups:
            self.mkBackup(backup)

    def createGroup(self):
        """
        creates sftponly group
        """
        self.addField("groupadd sftponly")

    def createUser(self):
        """
        creates ftp user
        """
        passwd = self.createPasswd()
        if not self.home:
            useradd = "useradd -g apache -G sftponly -s {2} \
-p {0} {1}".format(passwd,
                   self.username,
                   self.shell,
                   )
        else:
            useradd = "useradd -g apache -G sftponly -d {0} -s {3} \
-p {1} {2}".format(self.home,
                   passwd,
                   self.username,
                   self.shell,
                   )
        self.addField(useradd)
        self.getHomeDir()

    def createPasswd(self):
        """
        Set passwd for user
        """
        return crypt.crypt(self.passwd, "22")

    def createChrootDir(self):
        """
        create domains dir in users home dir
        """
        chroot = "{0}/{1}".format(self.home,
                                  self.domain
                                  )
        try:
            os.makedirs(chroot)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise exception

    def setDirPerms(self):
        """
        set home dir to root: and 755
        """
        self.addField("chown root: {0}".format(self.home))
        self.addField("chmod 755 {0}".format(self.home))

    def addGroupToUser(self):
        """
        adds user to group, sftponly
        """
        self.addField("usermod -g apache -G sftponly {0} -s {1}".format(
            self.username,
            self.shell,)
            )

    def disableDefaultSubsystem(self):
        """
        disables default Subsystem in /etc/ssh/sshd_config
        """
        self.scanFile('/etc/ssh/sshd_config',
                      "Subsystem\s+sftp\s+/usr/libexec/openssh/sftp-server",
                      array=1
                      )
        find = self.array[0]
        for line in fileinput.FileInput('/etc/ssh/sshd_config', inplace=1):
            line = line.replace(find, "#{0}".format(find))
            print line,

    def appendMatchGroup(self):
        """
        appends sftp chrooting info to /etc/ssh/sshd_config
        """
        subsystem = """
Subsystem   sftp    internal-sftp

UsePAM yes

Match Group sftponly
    ChrootDirectory %h
    ForceCommand internal-sftp
    AllowTcpForwarding no
"""
        self.appendToFile('/etc/ssh/sshd_config',
                          subsystem)

    def appendFstab(self):
        """
        appends mount info for chroot
        """
        bind = "{0}\t{1}/{2}\tnone\tbind\t0 0\n".format(self.web_root,
                                                        self.home,
                                                        self.domain,
                                                        )
        self.appendToFile('/etc/fstab',
                          bind)

    def appendUmask(self):
        """
        appends umask details so that 664 and 775 are default perms
        """

        pamd = "/etc/pam.d/sshd"
        session = "session optional pam_umask.so umask=0002"
        self.appendToFile(pamd,
                          session
                          )

    def restartSshd(self):
        """
        restarts sshd
        """
        self.addField("/etc/init.d/sshd restart")

    def mountFstab(self):
        """
        remounts fstab to use new mount points
        """
        self.addField("mount -a")

    def run(self):
        """
        does all of the magic
        """
        self.createBackups()
        if not self.checkUser():
            if not self.checkGroup():
                self.createGroup()
            self.createUser()
        else:
            if self.home is None:
                self.getHomeDir()
            self.addGroupToUser()
        if not self.checkMatchGroup():
            self.disableDefaultSubsystem()
            self.appendMatchGroup()
        time.sleep(1)
        self.createChrootDir()
        self.setDirPerms()
        if not self.checkFstab():
            self.appendFstab()
        if not self.checkPam():
            self.appendUmask()
        self.restartSshd()
        self.mountFstab()


if __name__ == '__main__':
    from optparse import OptionParser, OptionGroup
    parser = OptionParser()
    required = OptionGroup(parser, "REQUIRED")
    required.add_option('-u', '--username',
                        help="FTP Username",
                        metavar="USERNAME",
                        )
    required.add_option('-d', '--domain',
                        help='Domain to chroot',
                        metavar='DOMAIN',
                        )
    required.add_option('-w', '--web-root',
                        help='Domains doc root in VirtualHost',
                        metavar='/path/to/domains/web/root',
                        )
    required.add_option('-p', '--passwd',
                        help="Set users passwd",
                        metavar="Passwd",
                        )
    parser.add_option('--home-dir',
                      help="Specify users home directory",
                      metavar="/path/to/home/dir",
                      )
    parser.add_option_group(required)
    options, args = parser.parse_args()
    if not options.username:
        parser.error("Username not specified")
    if not options.domain:
        parser.error("Domain not specified")
    if not options.web_root:
        parser.error("Domain's web root not specified")
    if not options.passwd:
        parser.error("User's passwd not specified")

    if options.home_dir:
        ftp = User(username=options.username,
                  domain=options.domain,
                  web_root=options.web_root,
                  passwd=options.passwd,
                  home=options.home_dir,
                  )
    else:
        ftp = User(username=options.username,
                  domain=options.domain,
                  web_root=options.web_root,
                  passwd=options.passwd,
                  )
    ftp.checkRoot()
    ftp.run()
