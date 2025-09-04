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
    parser.add_argument("-s", "--search", help="models(s) to read")
    # parser.add_argument("-p", "--plottype", help="plot type(s) to plot", nargs="+")
    # parser.add_argument(
    #     "-l", "--list", help="list supported plot types", action="store_true"
    # )
    # parser.add_argument(
    #     "-s",
    #     "--startyear",
    #     help="startyear to read",
    # )
    # parser.add_argument(
    #     "-e", "--endyear", help="endyear to read; defaults to startyear.", nargs="?"
    # )
    # parser.add_argument("-v", "--variables", help="variable(s) to read", nargs="+")
    # parser.add_argument(
    #     "--tstype",
    #     help=f"tstype to read; defaults to {colors['BOLD']}{DEFAULT_TS_TYPE}{colors['END']}",
    #     nargs="?",
    # )
    # parser.add_argument(
    #     "-o",
    #     "--outdir",
    #     help=f"output directory for the plot files; defaults to {DEFAULT_OUTPUT_DIR}",
    #     default=".",
    # )

    args = parser.parse_args()
    options = {}
    if "search" in args:
        options["search"] = args.search


    pass

if __name__ == "__main__":
    run()