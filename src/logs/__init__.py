import os
import sys

CWD = os.getcwd()
SRCDIR = os.path.join(CWD, "src")
LOGDIR = os.path.join(SRCDIR, "logs")

sys.path.extend([SRCDIR, LOGDIR])
