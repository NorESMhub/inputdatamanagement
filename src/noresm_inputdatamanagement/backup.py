from noresm_inputdatamanagement.const import SOURCE_PATH, NCAR_COPY_PATH, BACKUP_DESTINATION_PATH

class Backup:
    __version__ = "0.0.1"

    def __init__(self, options):
        self.options = options
        if "dryrun" in options:
            self.dryrun = True
        else:
            self.dryrun = False

    def get_file_to_copy(self):
        """find files that are in the source file list, but not the NCAR copy """

    def get_file_lists(self):
        """read all necessary file lists, either from the file system or by
        user provided text files"""


        if "sourcefile" in self.options:
            with open(self.options["sourcefile"], "r") as source:
                self.sourcefiles = set(source.read().splitlines())
        else:
            raise NotImplementedError

        if "ncarfile" in self.options:
            with open(self.options["ncarfile"], "r") as ncar:
                self.ncarfiles = set(ncar.read().splitlines())
        else:
            raise NotImplementedError

        if "backupfile" in self.options:
            with open(self.options["backupfile"], "r") as backup:
                self.backupfiles = set(backup.read().splitlines())
        else:
            raise NotImplementedError

        if self.dryrun:
            print("dryrun")