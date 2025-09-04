#!/usr/bin/env python3
"""
pyaerocom plot: crerate plots using the pyaerocom API
"""

import argparse
import subprocess
import sys
from pathlib import Path
from tempfile import mkdtemp

from noresm_inputdatamanagement.const import SOURCE_PATH, NCAR_COPY_PATH, BACKUP_DESTINATION_PATH
from noresm_inputdatamanagement.createfilelists import CreateFileLists
from noresm_inputdatamanagement.backup import Backup



def run():
    colors = {
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

    parser = argparse.ArgumentParser(
            description="manage noresm inputdata",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""{colors['BOLD']}Example usages:{colors['END']}
    \t{colors['UNDERLINE']}- basic usage:{colors['END']}
    \t  The following line bla bla 
    \t  noresm_inputdata -c blubb
    
    """,
    )
    subparsers = parser.add_subparsers(help='subcommands help')
    parser_createfl = subparsers.add_parser('createfilelists', help='createfilelists help')
    parser_createfl.add_argument("-o", "--outputfolder", help="output folder")
    parser_createfl.add_argument("--sourcedir", help=f"source folder; defaults to {SOURCE_PATH}",
                                 default=SOURCE_PATH)
    parser_createfl.add_argument("--ncardir", help=f"NCAR folder; defaults to {NCAR_COPY_PATH}",
                                 default=NCAR_COPY_PATH)
    parser_createfl.add_argument("--backupdir",
                                 help=f"backup (destination) folder; defaults to {BACKUP_DESTINATION_PATH}",
                                 default=BACKUP_DESTINATION_PATH)

    parser_createfl.add_argument("--dryrun", help="dryrun; just show what would be done", action="store_true")



    parser_backup = subparsers.add_parser('backup', help='backup help')

    parser_backup.add_argument("--dryrun", help="dryrun; just show what would be done", action="store_true")
    parser_backup.add_argument("--sourcefile", help="text file with paths of the source directory", )
    parser_backup.add_argument("--ncarfile", help="text file with paths of the NCAR backup directory", )
    parser_backup.add_argument("--backupfile", help="text file with paths of the destination directory", )
    parser_backup.add_argument("--sourcedir", help=f"source folder; defaults to {SOURCE_PATH}",
                                 default=SOURCE_PATH)
    parser_backup.add_argument("--ncardir", help=f"NCAR folder; defaults to {NCAR_COPY_PATH}",
                                 default=NCAR_COPY_PATH)
    parser_backup.add_argument("--backupdir",
                                 help=f"backup (destination) folder; defaults to {BACKUP_DESTINATION_PATH}",
                                 default=BACKUP_DESTINATION_PATH)

    args = parser.parse_args()
    options = {}
    # Because we have sub parsers, only the attributes from the supplied sub parser
    # are part of args
    if sys.argv[1] == "backup":
        backup_options = {}
        if args.dryrun:
            backup_options["dryrun"] = True
        else:
            backup_options["dryrun"] = False
        if args.sourcedir:
            backup_options["sourcedir"] = args.sourcedir
        if args.ncardir:
            backup_options["ncardir"] = args.ncardir
        if args.backupdir:
            backup_options["backupdir"] = args.backupdir
        if args.sourcefile:
            backup_options["sourcefile"] = args.sourcefile
        if args.ncarfile:
            backup_options["ncarfile"] = args.ncarfile
        if args.backupfile:
            backup_options["backupfile"] = args.backupfile
        # apply some logic to the options:
        # if files are supplied, the directories are ignored
        backup = Backup(backup_options)
        backup.get_file_lists()

    elif sys.argv[1] == "createfilelists":
        createfl_opt = {}
        if args.sourcedir:
            createfl_opt["sourcedir"] = args.sourcedir
        if args.ncardir:
            createfl_opt["ncardir"] = args.ncardir
        if args.backupdir:
            createfl_opt["backupdir"] = args.backupdir
        if args.dryrun:
            createfl_opt["dryrun"] = True
        else:
            createfl_opt["dryrun"] = False
        if args.outputfolder:
            createfl_opt["outputfolder"] = args.outputfolder

        createfl = CreateFileLists(createfl_opt)
        createfl.get_source_files()
    else:
        parser.print_help()
        sys.exit(1)


    if "search" in args:
        options["search"] = args.search


    pass

if __name__ == "__main__":
    run()