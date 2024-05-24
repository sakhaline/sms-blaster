import os
import sys

BASEDIR = os.getcwd()
SRCDIR = os.path.join(BASEDIR, "src")

DATADIR = os.path.join(SRCDIR, "data")
LOGSDIR = os.path.join(SRCDIR, "logs")
SERVICESDIR = os.path.join(SRCDIR, "services")
UTILSDIR = os.path.join(SRCDIR, "utils")

DIRS = [BASEDIR, SRCDIR, DATADIR, SERVICESDIR, UTILSDIR]

sys.path.extend(DIRS)