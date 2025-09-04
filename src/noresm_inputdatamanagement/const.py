# main discussion is here:
# https://github.com/NorESMhub/NorESM/discussions/712

# path with files to checked if backup is needed
SOURCE_PATH = "/cluster/shared/noresm/inputdata"
# path with NCAR copy
# if a file from SOURCE_PATH is listed here, it will NOT be copied
# to BACKUP_DESTINATION_PATH
NCAR_COPY_PATH = "/nird/datalake/NS12077K/CESM-input-data"
# destination of the backup
# files below SOURCE_PATH, that are NOT present at NCAR_COPY_PATH will be
# copied here
BACKUP_DESTINATION_PATH = "/nird/projects/NS9560K/www/inputdata"
