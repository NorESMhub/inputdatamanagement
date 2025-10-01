# inputdatamanagement
collection of Python scripts (just one for the moment) for NorESM inputdata management for the different sigma2 machines

## Purpose
This project provides a command line tool for inputdata management for the NorESM model. As a first step it will facilitate 
the syncing between the HPCs (`betzy` for now) and the `nird` storage infrastructure according this discussion 
https://github.com/NorESMhub/NorESM/discussions/712

It's mainly a frontend for the tools `find` and `rsync` and will 
- create a rsync suitable file list file containing the files to sync using rsync's `--files-from` option
- set permissions right (`--chmod=Dg+s,ug+w,Fo-w,+X`) in rsync terms
- set group ownership right (`--chown :ns16001b`)

It also provides a dryrun option with and some information about which commands are run in the background.

## Installation
Standard installation is done via pip:

```
python -m pip install 'git+https://github.com/NorESMhub/inputdatamanagement.git'
```

For a different branch than main

```
python -m pip install 'git+https://github.com/NorESMhub/inputdatamanagement.git@<branch name>'
```


## Prerequests
Python >= 3.11

## Minimal documentation
```
usage: noresm_inputdata [-h] {createfilelists,backup} ...

manage noresm inputdata

positional arguments:
  {createfilelists,backup}
                        subcommands help
    createfilelists     createfilelists help
    backup              backup help

options:
  -h, --help            show this help message and exit
  
Example usages:
        - dryrun for input data backup on betzy using the defaults:
          noresm_inputdata backup --dryrun
    
          This will search the filesystems and therefore take some time. 
    
        - dryrun for input data backup file lists: 
          noresm_inputdata backup --dryrun --sourcefile source_files.txt --ncarfile NCAR_files.txt --backupfile destination_files.txt
    
          Files are in the current directories, paths are from the default paths. 
          For custom paths please add the --sourceignoredirs, --ncarignoredirs and --backupignoredirs switches if needed. 
    
        - dryrun for creating file lists:
          noresm_inputdata createfilelists --dryrun
    
          This will show the find commands to create file lists used for the backup

```

### noresm_inputdata backup
```bash
[jang@login-1.BETZY ~]$ noresm_inputdata backup -h
usage: noresm_inputdata backup [-h] [--dryrun] [--sourcefile SOURCEFILE] [--sourceignoredirs SOURCEIGNOREDIRS] [--ncarfile NCARFILE] [--ncarignoredirs NCARIGNOREDIRS] [--backupfile BACKUPFILE]
                               [--backupignoredirs BACKUPIGNOREDIRS] [--sourcedir SOURCEDIR] [--ncardir NCARDIR] [--backupdir BACKUPDIR]

options:
  -h, --help            show this help message and exit
  --dryrun              dryrun; just show what would be done
  --sourcefile SOURCEFILE
                        text file with paths of the source directory
  --sourceignoredirs SOURCEIGNOREDIRS
                        nb of directories in the file list to ignore
  --ncarfile NCARFILE   text file with paths of the NCAR backup directory
  --ncarignoredirs NCARIGNOREDIRS
                        nb of directories in the NCAR file list to ignore
  --backupfile BACKUPFILE
                        text file with paths of the destination directory
  --backupignoredirs BACKUPIGNOREDIRS
                        nb of directories in the backup file list to ignore
  --sourcedir SOURCEDIR
                        source folder; defaults to /cluster/shared/noresm/inputdata
  --ncardir NCARDIR     NCAR folder; defaults to /nird/datalake/NS12077K/CESM-input-data
  --backupdir BACKUPDIR
                        backup (destination) folder; defaults to /nird/datalake/NS16001B/cdl-ns16001b-NorESMInputdata
                        
```
### noresm_inputdata createfilelists
This is mainly useful for testing during development or when setting up backup on a new machine.

```bash
[jang@login-1.BETZY ~]$ noresm_inputdata createfilelists -h
usage: noresm_inputdata createfilelists [-h] [-o OUTPUTFOLDER] [--sourcedir SOURCEDIR] [--ncardir NCARDIR] [--backupdir BACKUPDIR] [--dryrun]

options:
  -h, --help            show this help message and exit
  -o OUTPUTFOLDER, --outputfolder OUTPUTFOLDER
                        output folder
  --sourcedir SOURCEDIR
                        source folder; defaults to /cluster/shared/noresm/inputdata
  --ncardir NCARDIR     NCAR folder; defaults to /nird/datalake/NS12077K/CESM-input-data
  --backupdir BACKUPDIR
                        backup (destination) folder; defaults to /nird/datalake/NS16001B/cdl-ns16001b-NorESMInputdata
  --dryrun              dryrun; just show what would be done
```

Example:
- most likely command you want to run
```
noresm_inputdata backup
```
This will gather all information online (search for all files) and backup everything the default backup location

## Development process
-  no committing to main branch; use PRs for that.
