#
# This file is part of pySMT.
#
#   Copyright 2014 Andrea Micheli and Marco Gario
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import os

from pysmt.exceptions import PysmtImportError
#
# Try to import the Cython version of the parser.
# Fall-back on the pure-python version if:
#  - Cython is not installed
#  - There is an error in the handling of the pyx file and the use of
#    Cython was not specified (unset env variable)
#
ENV_USE_CYTHON = os.environ.get("PYSMT_CYTHON")
if ENV_USE_CYTHON is not None:
    ENV_USE_CYTHON = ENV_USE_CYTHON.lower() in ["true", "1"]

HAS_CYTHON = False
try:
    import pyximport
    HAS_CYTHON = True
except ImportError as ex:
    if ENV_USE_CYTHON:
        raise PysmtImportError(str(ex))

if HAS_CYTHON and (ENV_USE_CYTHON or ENV_USE_CYTHON is None):
    USE_CYTHON = True
else:
    USE_CYTHON = False

if USE_CYTHON:
    try:
        pyximport.install()
        from pysmt.smtlib.parser.parser import *
    except ImportError as ex:
        if ENV_USE_CYTHON is None:
            # If not specified, fall-ack
            USE_CYTHON = False
        else:
            raise PysmtImportError(str(ex))

if not USE_CYTHON:
    print("*****", "Regular module")
    from pysmt.smtlib.parser.parser_py import *
else:
    print("****", "Cython Parser")
