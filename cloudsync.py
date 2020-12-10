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
FOLDER_LIST = (
    {
        'src': SPIDEROAK_HIVE + "/finance",
        'dst': INTERNXT_DRIVE,
        'options': ()
    },
    {
        'src': SPIDEROAK_HIVE + "/documents",
        'dst': INTERNXT_DRIVE,
        'options': ()
    },
    {
        'src': SPIDEROAK_HIVE + "/security",
        'dst': INTERNXT_DRIVE,
        'options': ("--exclude=security/archives", )
    },
    {
        'src': USER_HOME + "/dev/cloudsync",
        'dst': SPIDEROAK_HIVE + "/gitbackup",
        'options': (
            "--exclude=.git",
            "--exclude=.idea",
            "--exclude=venv",
            "--exclude=*.swp"
        )
    },
    {
        'src': USER_HOME + "/dev/joplinRevisionsCleanUp",
        'dst': SPIDEROAK_HIVE + "/gitbackup",
        'options': (
            "--exclude=.git",
            "--exclude=.idea",
            "--exclude=venv",
            "--exclude=*.swp"
        )
    },
    {
        'src': SPIDEROAK_HIVE + "/gitbackup",
        'dst': INTERNXT_DRIVE,
        'options': ()
    },
)


def filersync(src, dst):
    sync = subprocess.run(["rsync -pAXogEt '" + src + "' '" + dst + "'"], shell=True)
    if sync.returncode != 0:
        logging.error("ERROR (filersync): something went wrong when syncing " + os.path.basename(src) + "!")
        return False
    else:
        logging.info(src + " successfully synced to " + dst + ".")
    return True


def syncfile(src, dst):
    """The syncfile(src, dst) function synces a file specified as src with the dst directory (both ways).
    src (string) - the source file's full path (i.e. /path/filename)
    dst (string) - the destination directory's full path to rsync src to"""
    if not os.path.isfile(src):
        logging.error("ERROR (syncfile): " + src + " file not found!")
        return False
    if not os.path.isdir(dst):
        logging.error("ERROR (syncfile): the dst argument must be a directory.")
        return False
    srcpath, filename = os.path.split(src)
    if len(srcpath) == 0:
        srcpath = os.getcwd()  # precaution in case only a filename is passed see below line 56
    target = dst + "/" + filename
    if not os.path.isfile(target):  # the src file doesn't exist in the dst directory, initiate sync
        return filersync(src, dst)
    else:
        srcmodtime = os.path.getmtime(src)
        dstmodtime = os.path.getmtime(target)
        if srcmodtime == dstmodtime:
            logging.info(filename + " file already in sync, nothing to be done.")
            return True
        elif dstmodtime > srcmodtime:
            return filersync(target, srcpath)
        else:
            return filersync(src, dst)


def folderrsync(cmd, src, dst):
    sync = subprocess.run([cmd], shell=True)
    if sync.returncode == 0:
        logging.info(src + " directory successfully synced to " + dst + ".")
    else:
        logging.error("ERROR: something went wrong syncing SpiderOak's " + src + " directory.")


def syncfolder(src, dst, options):
    """The syncfolder() function keeps directories in sync (one way from src to dst)
    src (string) - the source directory's full path
    dst (string) - the destination directory's full path to rsync the src folder to
    options (list) - additional parameters (like exclusions) to pass to rsync"""
    if not os.path.isdir(dst):
        logging.error("ERROR (syncfolder): destination directory " + dst + " not found, aborting task!")
    elif not os.path.isdir(src):
        logging.error("ERROR (syncfolder): source directory " + src + " not found, skipping task!")
    else:
        rsynccmd = "rsync -rpAXogEtu --delete "  # only updates as it's a one way sync
        if len(options) > 0:
            rsynccmd += " ".join(options)
        rsynccmd += " '" + src + "' '" + dst + "'"
        logging.debug(rsynccmd)
        folderrsync(rsynccmd, src, dst)


logging.basicConfig(level=logging.INFO)  # systemd works fine with standard outputs (stdout, stderr)
option = "--all"  # default option
if len(sys.argv) > 1 and sys.argv[1] in ("--spideroak", "--internxt", "--all"):
    option = sys.argv[1]
if option in ("--spideroak", "--all"):
    for item in FILE_LIST:
        syncfile(item['src'], item['dst'])
if option in ("--internxt", "--all"):
    for item in FOLDER_LIST:
        syncfolder(item['src'], item['dst'], item['options'])
