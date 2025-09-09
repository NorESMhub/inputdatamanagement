# main discussion is here:
# https://github.com/NorESMhub/NorESM/discussions/712

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
