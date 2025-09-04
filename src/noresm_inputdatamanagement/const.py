# main discussion is here:
# https://github.com/NorESMhub/NorESM/discussions/712

#

# path with files to checked if backup is needed
SOURCE_PATH = "/cluster/shared/noresm/inputdata"
# only files owned by one of these groups are considered for backup
# will be used for the -group option of the find command
SOURCE_PATH_GROUPS_TO_COPY = ["noresm"]

# list of exclude patterns (file notation at this point)
# Will be applied even when supplying a file list of the source files
# might become a regular expression in the future
SOURCE_PATH_EXCLUDE_LIST = ["*/.svn/*", "*.lock"]
# path with NCAR copy
# if a file from SOURCE_PATH is listed here, it will NOT be copied
# to BACKUP_DESTINATION_PATH
NCAR_COPY_PATH = "/nird/datalake/NS12077K/CESM-input-data"

# destination of the backup
# files below SOURCE_PATH, that are NOT present at NCAR_COPY_PATH will be
# copied here
BACKUP_DESTINATION_PATH = "/nird/projects/NS9560K/www/inputdata"

# find command
FIND_CMD = "find"

# rsync command
RSYNC_CMD = "rsync"
