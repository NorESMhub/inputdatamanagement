import os

from noresm_inputdatamanagement.const import (SOURCE_PATH,
                                              NCAR_COPY_PATH, BACKUP_DESTINATION_PATH, FIND_CMD, SOURCE_PATH_GROUPS_TO_COPY,
                                              SOURCE_PATH_EXCLUDE_LIST, COLORS)
from pathlib import Path
import subprocess
import sys



class CreateFileLists:
    """class for file list generation

    used to make a --dryrun switch for the backup possible

    """
    __version__ = "0.0.1"

    def __init__(self, options):
        self.options = options
        self.cmd_source_arr = []
        self.cmd_dest_arr = []
        self.cmd_ncar_arr = []
        # set of source files
        self.sourcefiles = set()
        # set of files in the NCAR copy (relative to the NCAR directory)
        self.ncarfiles = set()
        # set of files in the destination directory
        self.backupfiles = set()
        if "dryrun" in options:
            self.dryrun = True
        else:
            self.dryrun = False

        if "sourcedir" in self.options:
            sourcedir = self.options["sourcedir"]
        else:
            sourcedir = SOURCE_PATH

        if "ncardir" in self.options:
            ncardir = self.options["ncardir"]
        else:
            ncardir = NCAR_COPY_PATH

        if "backupdir" in self.options:
            backupdir = self.options["backupdir"]
        else:
            backupdir = BACKUP_DESTINATION_PATH

        # piece find command for finding the source files together
        self.cmd_source_arr = self.cmd_source_arr + [FIND_CMD, sourcedir]
        # add the groups
        for _grp in SOURCE_PATH_GROUPS_TO_COPY:
            self.cmd_source_arr = self.cmd_source_arr + ["-group", _grp]
        # add search for files only
        self.cmd_source_arr = self.cmd_source_arr + ["-type", "f"]

        # piece together the command to search for the files in the directory of the NCAR copy
        self.cmd_ncar_arr = self.cmd_ncar_arr + [FIND_CMD, ncardir, "-type", "f"]

        # piece together the command to search for the files in the destination directory
        self.cmd_dest_arr = self.cmd_dest_arr + [FIND_CMD, backupdir, "-type", "f"]

    def get_source_files_ncar(self, ):
        """get ncar files
        """
        # get ncar files
        print(f"running command {' '.join(map(str, self.cmd_ncar_arr))}...")
        print("This might take a while...")
        sh_result = subprocess.run(self.cmd_ncar_arr, capture_output=True)
        if sh_result.returncode != 0:
            print(f"return code: {sh_result.returncode}")
            print(f"{sh_result.stderr}")
            sys.exit(-1)
        else:
            ncarfiles = set(sh_result.stdout.decode("utf-8").splitlines())
            print(f"success... Found {len(self.ncarfiles)} files")
        return ncarfiles

    def get_source_files_backup(self,):
        """get files in the backup directory
        """
        # get destination files
        print(f"running command {' '.join(map(str, self.cmd_dest_arr))}...")
        print("This might take a while...")
        sh_result = subprocess.run(self.cmd_dest_arr, capture_output=True)
        if sh_result.returncode != 0:
            print(f"return code: {sh_result.returncode}")
            print(f"{sh_result.stderr}")
            sys.exit(-1)
        else:
            backupfiles = set(sh_result.stdout.decode("utf-8").splitlines())
            print(f"success... Found {len(self.backupfiles)} files")
        
        return backupfiles

    def get_source_files_source(self, ):
        """get files from the source directory
        """

        # get source  files
        print(f"running command {' '.join(map(str, self.cmd_source_arr))}...")
        print("This might take a while...")
        sh_result = subprocess.run(self.cmd_source_arr, capture_output=True)
        if sh_result.returncode != 0:
            print(f"return code: {sh_result.returncode}")
            print(f"{sh_result.stderr.decode("utf-8").splitlines()}")
            try:
                sourcefiles = set(sh_result.stdout.decode("utf-8").splitlines())
            except Exception:
                sys.exit(-1)
        else:
            sourcefiles = set(sh_result.stdout.decode("utf-8").splitlines())
            
        print(f"success... Found {len(sourcefiles)} files")

        return sourcefiles

    def get_source_files(self, ):
        """find files"""

        if self.dryrun:
            print(f"{COLORS['UNDERLINE']}command for source file list:{COLORS['END']}")
            print(" ".join(map(str, self.cmd_source_arr)))
            print("")
            print(f"{COLORS['UNDERLINE']}command for creating the file list of the NCAR archive{COLORS['END']}")
            print(" ".join(map(str, self.cmd_ncar_arr)))
            print("")
            print(f"{COLORS['UNDERLINE']}command for creating the file list of the destination folder:{COLORS['END']}")
            print(" ".join(map(str, self.cmd_dest_arr)))
            print("")
        else:
            self.ncarfiles = self.get_source_files_ncar()
            self.backupfiles = self.get_source_files_backup()
            self.sourcefiles = self.get_source_files_source()            
            
            


