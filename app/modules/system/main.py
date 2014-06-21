# -*- coding: utf-8 -*-

# Create new vhost conf for any distro
# detect web service
# add gzip

#modules
from netifaces import interfaces, ifaddresses, AF_INET
from app import db, models
from sqlalchemy import func
import os
import platform
import subprocess
import shutil
import psutil
import socket
import errno
import pwd
import sys


class System():
    def __init__(self):
        self.disk_usage = self.getDiskUsage()

    def runCommand(self, command):
        """
        run shell command
        """

        cmd = subprocess.Popen(command.split(),
                                stdout=subprocess.PIPE,
                               )
        output, error = cmd.communicate()
        return output

    def getKernel(self):
        """
        Get Kernel Version
        """
        return platform.release()

    def getOs(self):
        """
        Get Operating System
        """
        return self.runCommand('cat /etc/system-release')

    def getHostname(self):
        """
        get servers hostname
        """
        return socket.gethostname()

    def getWebService(self):
        """
        returns web service installed
        """
        return 'httpd'

    def getDatabaseService(self):
        """
        returns web service installed
        """
        return 'mariadb'

    def getNumberOfDomains(self):
        """
        returns the number of domains configured on the server
        """
        return len(models.Domain.query.all())

    def getNumberOfDatabases(self):
        """
        returns the number of databases configured on the server
        """
        return '3'

    def getNumberOfUsers(self):
        """
        returns the number of users configured on the server
        """
        return len(models.User.query.all())
        #return '7'

    def getZcpVersion(self):
        """
        Get Physical Memory
        """
        return '0.1a'

    def getRamUsage(self):
        """
        """
        return psutil.phymem_usage()

    def getTotalPhyMemory(self):
        """
        Get Physical Memory
        """
        return self.getRamUsage().total / 1024 / 1024

    def getUsedPhyMemory(self):
        """
        Get Physical Memory
        """
        return self.getRamUsage().used / 1024 / 1024

    def getPercentPhyMemory(self):
        """
        Get Physical Memory
        """
        return self.getRamUsage().percent

    def getDiskUsage(self):
        """
        Get Physical Memory
        """
        return psutil.disk_usage('/')

    
    def getDiskUsed(self):
        """
        Get Physical Memory
        """
        return self.disk_usage.used / 1024 / 1024

    def getDiskFree(self):
        """
        Get Physical Memory
        """
        return self.disk_usage.free / 1024 / 1024

    def getDiskTotal(self):
        """
        Get Physical Memory
        """
        return self.disk_usage.total / 1024 / 1024

    def getDiskPartitions(self):
        """
        Get Physical Memory
        """
        return psutil.disk_partitions()

    def getIps(self):
        ip_list = []
        for interface in interfaces():
            for link in ifaddresses(interface)[AF_INET]:
                ip_list.append(link['addr'])
        string = ''.join(str(e+"  ") for e in ip_list)
        return string


if __name__ == '__main__':
    system = System()
    print system.getKernel()
    print system.getOs()
    print system.getDiskUsed()
    print system.getDiskFree()
    print system.getDiskTotal()
    print system.getDiskPartitions()
    print system.getIps()
