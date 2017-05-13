#!/bin/bash

# reorganize python module imports, as specified
isort -rc --atomic .

# autoclean most of the common code errors
autopep8 -v -r -i --exclude './*/migrations/*' --select=E251,E231,E303,E261,E272,E201,E222,E302,E225,E111,E221,E202,E203,E703,E271,E301,E701,E241 .
