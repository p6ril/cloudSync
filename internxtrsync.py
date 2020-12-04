#!/usr/bin/env python3

import os
import os.path
import subprocess

USER_HOME = "/home/gandalf"
DOCUMENTS = USER_HOME + "/Documents"
SPIDEROAK_HIVE = USER_HOME + "/SpiderOak Hive"
INTERNXT_DRIVE = USER_HOME + "/Internxt Drive"
FILE_LIST = (
    {'src': DOCUMENTS + "/KeePassXC.kdbx", 'dst': SPIDEROAK_HIVE + "/security"},
)


def filersync(src, dst):
    sync = subprocess.run(["rsync -pAXogEt '" + src + "' '" + dst + "'"], shell=True)
    if sync.returncode != 0:
        print("ERROR (filersync): something went wrong when syncing " + os.path.basename(src))
        return False
    else:
        print(src + " successfully synced to " + dst)
    return True


def syncfile(src, dst):
    if not os.path.isfile(src):
        print("ERROR (syncfile): " + src + " file not found!")
        return False
    if not os.path.isdir(dst):
        print("ERROR (syncfile): the sync destination must be a directory.")
        return False
    srcpath, filename = os.path.split(src)
    if len(srcpath) == 0:
        srcpath = os.getcwd()
    target = dst + "/" + filename
    if not os.path.isfile(target):  # target doesn't exist, initiate sync
        return filersync(src, dst)
    else:
        srcmodtime = os.path.getmtime(src)
        dstmodtime = os.path.getmtime(target)
        if srcmodtime == dstmodtime:
            print(filename + " is already in sync.")
            return True
        elif dstmodtime > srcmodtime:
            return filersync(target, srcpath)
        else:
            return filersync(src, dst)


for element in FILE_LIST:
    syncfile(element['src'], element['dst'])
