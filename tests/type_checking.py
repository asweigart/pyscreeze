import os
import sys

returnCode = 0
returnCode += os.system("pyright pyscreeze")
returnCode += os.system("mypy pyscreeze --show-error-codes")
sys.exit(returnCode)
