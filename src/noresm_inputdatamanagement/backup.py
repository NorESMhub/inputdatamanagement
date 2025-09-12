import fnmatch
import os
import shutil

import subprocess
from tempfile import mkdtemp


from noresm_inputdatamanagement.const import BACKUP_DESTINATION_PATH, \
    SOURCE_PATH_EXCLUDE_LIST, \
    TMP_DIR, RUN_UUID, RSYNC_CMD, RSYNC_CMD_ARR_START

from noresm_inputdatamanagement.createfilelists import CreateFileLists

class Backup:
    __version__ = "0.0.1"

    def __init__(self, options):
        self.options = options
        if "dryrun" in options:
            self.dryrun = True
        else:
            self.dryrun = False

        self.test_flag = True
        if self.test_flag:
            # create temp dir for rsync file
            self.tempdir = mkdtemp(dir=TMP_DIR)
            self.rsync_file = os.path.join(self.tempdir, f"rsync_file_list_{RUN_UUID}.txt")


        # the following is a dictionary with the relative source path as key. and the absolute source path
        # as value
        self.source_file_dict = {}
        # set of source files
        self.sourcefiles = set()
        # set of files in the NCAR copy (relative to the NCAR directory)
        self.ncarfiles = set()
        # set of files in the destination directory
        self.backupfiles = set()
        # dict of target backup files to copy
        # key is the absolute input file
        # value is the absolute destination file name
        self.target_file_dict = {}

    def run_backup(self, method="rsync"):
        """Method to actually run the backup

        the method switch allows for different ways of copying
        """
        self.get_target_files()
        if method == "shutil":
            # pure serial copying
            lastdir = ''
            for _source_file in self.target_file_dict:
                if not self.dryrun:
                    print(f"copying {_source_file} to {self.target_file_dict[_source_file]}")
                    currdir = os.path.dirname(self.target_file_dict[_source_file])
                    if currdir != lastdir:
                        os.makedirs(currdir, exist_ok=True)
                    lastdir = currdir
                    shutil.copy2(_source_file, self.target_file_dict[_source_file])
                else:
                    print(f"would copy {_source_file} to {self.target_file_dict[_source_file]}")

        elif method == "rsync":
            # use rsync to copy
            # write temporary file list to be used by the rsync command
            # add "./" between the source directory and the relative path
            # to make rsync's -R switch work
            with open(self.rsync_file, "w") as fh:
                for _line in sorted(self.sourcefiles):
                    fh.write(f"{os.path.join(self.options["sourcedir"], ".", _line)}\n")

            print(f"wrote rsync file list {self.rsync_file}")

            if self.dryrun:
                self.rsync_cmd_arr = ["rsync", "-avn", f"--files-from={self.rsync_file}", "/", self.options["backupdir"]]
            else:
                self.rsync_cmd_arr = ["echo", "rsync", "-avn", f"--files-from={self.rsync_file}", "/", self.options["backupdir"]]
            
            print(f"running command {' '.join(map(str, self.rsync_cmd_arr))}...")
            print("This might take a while...")
            subprocess.run(self.rsync_cmd_arr, shell=True)

            # raise NotImplementedError
        else:
            raise NotImplementedError

    def get_target_files(self):
        """small helper method to create a list of absolute target files"""
        for _file in self.sourcefiles:
            self.target_file_dict[self.source_file_dict[_file]] = os.path.join(BACKUP_DESTINATION_PATH, _file)


    def get_source_files_to_copy(self, ):
        """find files that are in the source file list, but not the NCAR copy
        or at the backup destination
        """

        # how to do it:
        # 1) remove files from source file list that are present already at the destination dir
        # 2) remove files from source file list that are at the NCAR backup location

        backup_files_removed = 0
        ncar_files_removed = 0
        inputfiles = len(self.sourcefiles)

        for _destfile in self.backupfiles:
            # print(_destfile)
            if _destfile in self.sourcefiles:
                self.sourcefiles.remove(_destfile)
                backup_files_removed += 1

        for _ncarfile in self.ncarfiles:
            if _ncarfile in self.sourcefiles:
                self.sourcefiles.remove(_ncarfile)
                ncar_files_removed += 1

        print(f"Info: {inputfiles} potential source files were found in the inputdata folder.")
        print(f"Info: {backup_files_removed} source files were found in the backup folder.")
        print(f"Info: {ncar_files_removed} source files were found in the NCAR archive folder.")
        print(f"Info: This leaves {len(self.sourcefiles)} source files to be copied.")

        return self.sourcefiles

    def get_rel_paths(self, paths:set[str], dirs_to_ignore:int = 0):
        """helper routine that removes a given number directories
        from a set of directories

        """
        outset = set()
        for path in paths:
            tmp_dummy = "/".join(path.split("/")[dirs_to_ignore:])
            outset.add(tmp_dummy)
            self.source_file_dict[tmp_dummy] = path
        return outset

    def remove_excluded_files(self, paths:set[str], exclude_patterns:list[str]):
        """small helper to remove files matching a list of file patterns
        from a list / set"""

        ret_set = paths
        # removals = []
        for _idx, pattern in enumerate(exclude_patterns):
            removals = fnmatch.filter(ret_set, pattern)
            for path in removals:
                ret_set.remove(path)
                del self.source_file_dict[path]

        return ret_set


    def get_file_lists(self):
        """read all necessary file lists, either from the file system or by
        user provided text files"""

        createfl = CreateFileLists(self.options)

        if "sourcefile" in self.options:
            with open(self.options["sourcefile"], "r") as source:
                self.sourcefiles = set(source.read().splitlines())
            
        else:
            self.sourcefiles = createfl.get_source_files_source()
        self.sourcefiles = self.get_rel_paths(self.sourcefiles, self.options["sourceignoredirs"])
        self.sourcefiles = self.remove_excluded_files(self.sourcefiles, SOURCE_PATH_EXCLUDE_LIST)

        if "ncarfile" in self.options:
            with open(self.options["ncarfile"], "r") as ncar:
                self.ncarfiles = set(ncar.read().splitlines())    
        else:
            self.ncarfiles = createfl.get_source_files_backup()
        self.ncarfiles = self.get_rel_paths(self.ncarfiles, self.options["ncarignoredirs"])

        if "backupfile" in self.options:
            with open(self.options["backupfile"], "r") as backup:
                self.backupfiles = set(backup.read().splitlines())
        else:
            self.backupfiles = createfl.get_source_files_source()
        self.backupfiles = self.get_rel_paths(self.backupfiles, self.options["backupignoredirs"])

