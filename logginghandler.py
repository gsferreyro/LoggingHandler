# Logging Handler copyright 2023-2023 by Gustavo S. Ferreyro. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Gustavo S. Ferreyro
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# GUSTAVO S. FERREYRO DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# GUSTAVO S. FERREYRO BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Copyright (C) 2023-2023 Gustavo S. Ferreyro. All Rights Reserved.

To use, copy this module and 'import logginghandler' or 'from logginghandler import LoggingHandler'

This Logging Handler uses the Logging package for Python. Copyright 2001-2022 by Vinay Sajip. All Rights Reserved.
https://github.com/python/cpython/tree/main/Lib/logging
"""

import os
import errno
import logging


class LoggingHandler(logging.Logger):
    def __init__(
        self,
        name: str,
        folder_path: str,
        level: str = "NOTSET",
        format: str = "%(asctime).19s | %(levelname).4s | %(message)s",
        filemode: str = "a+",
    ):
        super().__init__(name=name, level=level)
        self.name = name
        folder_path = os.path.normpath(folder_path)
        self.folder_path = folder_path
        if not name.lower().endswith(".log"):
            name += ".log"
        self.filename = name
        self.file_path = os.path.normpath(os.path.join(folder_path, name))
        self.filemode = filemode
        self.format = format
        self.strLevel = level
        self.init()

    def __del__(self):
        self.close()

    def init(self):
        try:
            os.makedirs(self.folder_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            pass
        file_handler = logging.FileHandler(filename=self.file_path, mode=self.filemode)
        formatter = logging.Formatter(self.format)
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)
        self.critical(f"** Starting...")
        self.critical(f"** Log Level: {self.strLevel}")

    def close(self):
        self.critical(f"** Ending...")
        if self.hasHandlers():
            self.handlers[0].close()
