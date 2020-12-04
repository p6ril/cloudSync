#!/usr/bin/env python3

import sys
import os
import os.path
import subprocess
import logging

USER_HOME = "/home/gandalf"
DOCUMENTS = USER_HOME + "/Documents"
SPIDEROAK_HIVE = USER_HOME + "/SpiderOak Hive"
INTERNXT_DRIVE = USER_HOME + "/Internxt Drive"
FILE_LIST = (
    {'src': DOCUMENTS + "/KeePassXC.kdbx", 'dst': SPIDEROAK_HIVE + "/security"},
)
SPIDEROAK_LIST = (
    {'dir': SPIDEROAK_HIVE + "/finance", 'options': ()},
    {'dir': SPIDEROAK_HIVE + "/documents", 'options': ()},
    {'dir': SPIDEROAK_HIVE + "/security", 'options': ("--exclude=security/archives", )},
)


def filersync(src, dst):
    sync = subprocess.run(["rsync -pAXogEt '" + src + "' '" + dst + "'"], shell=True)
    if sync.returncode != 0:
        logging.error("ERROR (filersync): something went wrong when syncing " + os.path.basename(src))
        return False
    else:
        logging.info(src + " successfully synced to " + dst)
    return True


def syncfile(src, dst):
    """The syncfile(src, dst) function synces a file specified as src to the dst directory.
    src (string) - source file full path (i.e. /path/filename)
    dst (string) - the destination directory full path to rsync src to"""
    if not os.path.isfile(src):
        logging.error("ERROR (syncfile): " + src + " file not found!")
        return False
    if not os.path.isdir(dst):
        logging.error("ERROR (syncfile): the sync destination must be a directory.")
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
            logging.info(filename + " is already in sync.")
            return True
        elif dstmodtime > srcmodtime:
            return filersync(target, srcpath)
        else:
            return filersync(src, dst)


def folderrsync(cmd, srcdir):
    sync = subprocess.run([cmd], shell=True)
    if sync.returncode == 0:
        logging.info("SpiderOak's " + srcdir + " directory successfully synced to Internxt Drive.")
    else:
        logging.error("ERROR: something went wrong syncing SpiderOak's " + srcdir + " directory.")


def internxtrsync():
    """The internxtrsync() function keeps SpiderOak Hive and Internxt Drive in sync"""
    for item in SPIDEROAK_LIST:
        shellcmd = "rsync -rpAXogEt --delete "
        if len(item['options']) > 0:
            shellcmd += " ".join(item['options'])
        shellcmd += " '" + item['dir'] + "' '" + INTERNXT_DRIVE + "'"
        logging.debug(shellcmd)
        folderrsync(shellcmd, os.path.basename(item['dir']))


logging.basicConfig(level=logging.INFO)
option = "--all"  # default option
if len(sys.argv) > 1 and sys.argv[1] in ("--spideroak", "--internxt", "--all"):
    option = sys.argv[1]
if option in ("--spideroak", "--all"):
    for elm in FILE_LIST:
        syncfile(elm['src'], elm['dst'])
if option in ("--internxt", "--all"):
    internxtrsync()
