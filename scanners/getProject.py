import zipfile
import re
import os
import sys


# OpeHub helper

def getProject(packagepath):
    verifypkg(packagepath)
    return readzip(packagepath)

def readzip(packagepath):
    zipreader = zipfile.ZipFile(packagepath, 'r')
    name_list = zipreader.namelist()
    raw_name = name_list[0]
    projectname = raw_name.split("_")[0].split("-")[0]
    return projectname
        

def verifypkg(packagepath):
    if not zipfile.is_zipfile(packagepath):
        sys.stderr.write("[-] Package not supported")
	sys.exit(-1)
    else:
        pass


if __name__ == '__main__':
    sys.stdout.write(getProject(os.path.abspath(sys.argv[1])))
