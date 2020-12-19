#!/usr/bin/env python3

import sys
import os
import os.path
import subprocess
import logging

from conf import FILE_LIST as FILE_LIST
from conf import FOLDER_LIST as FOLDER_LIST


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
    if not isinstance(src, str) or (isinstance(src, str) and len(src) == 0):
        logging.error("ERROR (syncfile): improper mandatory src file argument! Skipping sync task.")
        return False
    if not isinstance(dst, str) or (isinstance(dst, str) and len(dst) == 0):
        logging.error("ERROR (syncfile): improper mandatory dst argument! Skipping file sync task.")
        return False
    if not os.path.isfile(src):
        logging.error("ERROR (syncfile): " + src + " file not found!")
        return False
    if not os.path.isdir(dst):
        logging.error("ERROR (syncfile): the dst argument must be an existing directory.")
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
        logging.error("ERROR: something went wrong syncing the " + src + " directory.")


def syncfolder(config):
    """The syncfolder() function keeps 2 directories in sync (one way only: from src to dst)
    config (dict) - rsync configuration information as the following keys:
        src (string) - the source directory's full path
        dst (string) - the destination directory's full path to rsync the src folder to
        options (tuple) - rsync full parameter list"""
    if not isinstance(config, dict):
        logging.error("ERROR (syncfolder): wrong argument type! A dictionary is expected.")
        return False
    if not all(k in config for k in ('src', 'dst', 'options')):
        logging.error("ERROR (syncfolder): missing mandatory keys in dictionary argument!")
        return False
    src, dst, options = config.values()
    if not isinstance(src, str) or (isinstance(src, str) and len(src) == 0):
        logging.error("ERROR (syncfolder): improper mandatory src key argument! Canceling task.")
        return False
    if not isinstance(dst, str) or (isinstance(dst, str) and len(dst) == 0):
        logging.error("ERROR (syncfolder): improper mandatory dst key argument! Canceling task.")
        return False
    if not isinstance(options, tuple) or (isinstance(options, tuple) and len(options) == 0):
        logging.error("ERROR (syncfolder): improper mandatory options key argument! Canceling task.")
        return False
    for o in options:
        if not isinstance(o, str) or (isinstance(o, str) and not o.startswith("-")):
            logging.error("ERROR (syncfolder): incorrect rsync option! Canceling task.")
            return False
    if not os.path.isdir(dst):
        logging.error("ERROR (syncfolder): destination directory " + dst + " not found, aborting task!")
    elif not os.path.isdir(src):
        logging.error("ERROR (syncfolder): source directory " + src + " not found, skipping task!")
    else:
        rsynccmd = "rsync  " + " ".join(options) + " '" + src + "' '" + dst + "'"
        logging.debug(rsynccmd)
        folderrsync(rsynccmd, src, dst)


logging.basicConfig(level=logging.INFO)  # systemd works fine with standard outputs (stdout, stderr)
clarg = "--all"  # default command line argument
if len(sys.argv) > 1 and sys.argv[1] in ("--file",  "--folder", "--all"):
    clarg = sys.argv[1]
if clarg in ("--file", "--all"):
    for item in FILE_LIST:
        syncfile(item['src'], item['dst'])
if clarg in ("--folder", "--all"):
    for item in FOLDER_LIST:
        syncfolder(item)
