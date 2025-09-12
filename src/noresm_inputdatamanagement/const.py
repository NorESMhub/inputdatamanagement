# main discussion is here:
# https://github.com/NorESMhub/NorESM/discussions/712

from uuid import uuid4


# some terminal colors
COLORS = {
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m",
        "END": "\033[0m",
        "PURPLE": "\033[95m",
        "CYAN": "\033[96m",
        "DARKCYAN": "\033[36m",
        "BLUE": "\033[94m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "RED": "\033[91m",
    }

TMP_DIR = "/tmp"
RUN_UUID = uuid4()

# path with files to checked if backup is needed
SOURCE_PATH = "/cluster/shared/noresm/inputdata"
# default number of directories to ignore in case we get supplied a text file
# with the files
SOURCE_PATH_BASE_LENGTH = len(SOURCE_PATH.split("/"))
# only files owned by one of these groups are considered for backup
# will be used for the -group option of the find command
SOURCE_PATH_GROUPS_TO_COPY = ["noresm"]

# list of exclude patterns (file notation at this point)
# Will be applied even when supplying a file list of the source files
# might become a regular expression in the future
SOURCE_PATH_EXCLUDE_LIST = [".svn/*", "*/.svn/*", "*.lock", "*cplhist/noresm3_0/*"]
# path with NCAR copy
# if a file from SOURCE_PATH is listed here, it will NOT be copied
# to BACKUP_DESTINATION_PATH
NCAR_COPY_PATH = "/nird/datalake/NS12077K/CESM-input-data"
NCAR_COPY_PATH_BASE_LENGTH = len(NCAR_COPY_PATH.split("/"))

# destination of the backup
# files below SOURCE_PATH, that are NOT present at NCAR_COPY_PATH will be
# copied here
BACKUP_DESTINATION_PATH = "/nird/projects/NS9560K/www/inputdata"
BACKUP_DESTINATION_PATH_BASE_LENGTH = len(BACKUP_DESTINATION_PATH.split("/"))

# find command
FIND_CMD = "find"

# rsync command
RSYNC_CMD = "rsync"
# these are the static parts of the issued rsync call
# in general the call is something like this (--files-from implies -R with rsync)
# rsync -avn --files-from=FILE --rsync-path="cd /foo; rsync" <target directory>
# in FILE are the realtive file names from SOURCE_PATH
# from the rsync man page:
# It is also possible to limit the amount of path information that is sent as implied directories for each path you specify.
# With a modern rsync on the sending side (beginning with 2.6.7), you can insert a dot and a slash into the source path, like
# this:
#
# rsync -avR /foo/./bar/baz.c remote:/tmp/
#
# That  would  create /tmp/bar/baz.c on the remote machine. (Note that the dot must be followed by a slash, so "/foo/." would
# not be abbreviated.) For older rsync versions, you would need to use a chdir to limit the source path.
# rsync -avR --rsync-path="cd /a/b && rsync" host:c/d /e/
# rsync -avR --rsync-path="cd /foo; rsync" remote:bar/baz.c /tmp/
RSYNC_CMD_ARR_START = ["rsync", "-"]
