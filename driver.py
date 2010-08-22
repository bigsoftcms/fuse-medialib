#!/usr/bin/python
from fuse import Fuse
import fuse
from time import time

import stat
import os
import errno
import sys

from flibrary.library import Library
from flibfs.structure import Structure

fuse.fuse_python_api = (0, 2)

class StatInfo(object):
    def __init__(self, statdict):
        self.st_mode = statdict["st_mode"]
        self.st_ino = statdict["st_ino"]
        self.st_dev = statdict["st_dev"]
        self.st_nlink = statdict["st_nlink"]
        self.st_uid = statdict["st_uid"]
        self.st_gid = statdict["st_gid"]
        self.st_size = statdict["st_size"]
        self.st_atime = statdict["st_atime"]
        self.st_mtime = statdict["st_mtime"]
        self.st_ctime = statdict["st_ctime"]

class LibraryFS(Fuse):
    """
    """

    def __init__(self, *args, **kw):
        Fuse.__init__(self, *args, **kw)
        self.parse()
        
        self.lib = Library("mysql://fuselib@localhost/fuselib")
        self.structure = Structure(open("music.xml", "r"), self.lib)

        print 'Init complete.'
        sys.stdout.flush()
        
    def _stattuple(self, statmap):
        return statmap["st_mode"], statmap["st_ino"], statmap["st_dev"], statmap["st_nlink"], statmap["st_uid"], statmap["st_gid"], statmap["st_size"], statmap["st_atime"], statmap["st_mtime"], statmap["st_ctime"]

    def getattr(self, path):
        """
        - st_mode (protection bits)
        - st_ino (inode number)
        - st_dev (device)
        - st_nlink (number of hard links)
        - st_uid (user ID of owner)
        - st_gid (group ID of owner)
        - st_size (size of file, in bytes)
        - st_atime (time of most recent access)
        - st_mtime (time of most recent content modification)
        - st_ctime (platform dependent; time of most recent metadata change on Unix,
                    or the time of creation on Windows).
        """

        pathTuple = tuple(path.split("/"));
        try:
            stat = self.structure[pathTuple].getStat()
            return StatInfo(stat)
        except AttributeError:
            return -errno.ENOENT
        

    def readdir(self, path, offset):
        """
        return: [[('file1', 0), ('file2', 0), ... ]]
        """
        """pathTuple = tuple(path.split("/"));
        try:
            fsnode = self.structure[pathTuple]
            if fsnode.isLeaf():
                return -errno.ENOSYS
            else:
                dirlist = self.structure[pathTuple].getDir()
                return dirlist
        except AttributeError:
            return -errno.ENOENT"""
        pathTuple = tuple(unicode(path, "utf-8").split("/"));
        for direntry in self.structure[pathTuple].getDir():
            yield direntry

    def mythread ( self ):
        pass

    def chmod ( self, path, mode ):
        print '*** chmod', path, oct(mode)
        sys.stdout.flush()
        return -errno.ENOSYS

    def chown ( self, path, uid, gid ):
        print '*** chown', path, uid, gid
        sys.stdout.flush()
        return -errno.ENOSYS

    def fsync ( self, path, isFsyncFile ):
        print '*** fsync', path, isFsyncFile
        sys.stdout.flush()
        return -errno.ENOSYS

    def link ( self, targetPath, linkPath ):
        print '*** link', targetPath, linkPath
        sys.stdout.flush()
        return -errno.ENOSYS

    def mkdir ( self, path, mode ):
        print '*** mkdir', path, oct(mode)
        sys.stdout.flush()
        return -errno.ENOSYS

    def mknod ( self, path, mode, dev ):
        print '*** mknod', path, oct(mode), dev
        sys.stdout.flush()
        return -errno.ENOSYS

    def open ( self, path, flags ):
        print '*** open', path, flags
        sys.stdout.flush()
        return -errno.ENOSYS

    def read ( self, path, length, offset ):
        print '*** read', path, length, offset
        sys.stdout.flush()
        return -errno.ENOSYS

    def readlink ( self, path ):
        pathTuple = tuple(unicode(path, "utf-8").split("/"));
        try:
            return self.structure[pathTuple].readLink().encode("utf-8")
        except AttributeError:
            return -errno.ENOENT

    def release ( self, path, flags ):
        print '*** release', path, flags
        sys.stdout.flush()
        return -errno.ENOSYS

    def rename ( self, oldPath, newPath ):
        print '*** rename', oldPath, newPath
        sys.stdout.flush()
        return -errno.ENOSYS

    def rmdir ( self, path ):
        print '*** rmdir', path
        sys.stdout.flush()
        return -errno.ENOSYS

    def statfs ( self ):
        print '*** statfs'
        sys.stdout.flush()
        return -errno.ENOSYS

    def symlink ( self, targetPath, linkPath ):
        print '*** symlink', targetPath, linkPath
        sys.stdout.flush()
        return -errno.ENOSYS

    def truncate ( self, path, size ):
        print '*** truncate', path, size
        sys.stdout.flush()
        return -errno.ENOSYS

    def unlink ( self, path ):
        print '*** unlink', path
        sys.stdout.flush()
        return -errno.ENOSYS

    def utime ( self, path, times ):
        print '*** utime', path, times
        sys.stdout.flush()
        return -errno.ENOSYS

    def write ( self, path, buf, offset ):
        print '*** write', path, buf, offset
        sys.stdout.flush()
        return -errno.ENOSYS

if __name__ == "__main__":
    fs = LibraryFS()
    fs.flags = 0
    fs.multithreaded = 0
    fs.main()