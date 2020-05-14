#cython: language_level=3, c_string_type=unicode, c_string_encoding=utf8, boundscheck=False, cdivision=True, wraparound=False
# distutils: language=c++

from libcpp.vector cimport vector
from libcpp.string cimport string
cimport cython

__all__ = ['ColorSequence']

cdef string CS_BOLD_SEQ = b'\033[1m'
cdef string CS_RESET_SEQ = b'\033[0m'
cdef string CS_BLACK = b'\033[6;90m'
cdef string CS_RED = b'\033[6;91m'
cdef string CS_GREEN = b'\033[6;92m'
cdef string CS_YELLOW = b'\033[6;93m'
cdef string CS_BLUE = b'\033[6;94m'
cdef string CS_MAGENTA = b'\033[6;95m'
cdef string CS_CYAN = b'\033[6;96m'
cdef string CS_WHITE = b'\033[6;97m'

cdef class ColorSequence:
    @property
    def BOLD_SEQ(self):
        return CS_BOLD_SEQ

    @property
    def RESET_SEQ(self):
        return CS_RESET_SEQ

    @property
    def BLACK(self):
        return CS_BLACK

    @property
    def RED(self):
        return CS_RED

    @property
    def GREEN(self):
        return CS_GREEN

    @property
    def YELLOW(self):
        return CS_YELLOW

    @property
    def BLUE(self):
        return CS_BLUE

    @property
    def MAGENTA(self):
        return CS_MAGENTA

    @property
    def CYAN(self):
        return CS_CYAN

    @property
    def WHITE(self):
        return CS_WHITE
        

    @staticmethod
    @cython.binding(True)
    cdef string color_cyan(const string& text) nogil:
        cdef:
            string res = CS_CYAN
        res.append(text)
        res.append(CS_RESET_SEQ)
        return res

    @staticmethod
    @cython.binding(True)
    cdef string color_green(const string& text) nogil:
        cdef:
            string res = CS_GREEN
        res.append(text)
        res.append(CS_RESET_SEQ)
        return res

    @staticmethod
    @cython.binding(True)
    cdef string color_red(const string& text) nogil:
        cdef:
            string res = CS_RED
        res.append(text)
        res.append(CS_RESET_SEQ)
        return res

    @staticmethod
    @cython.binding(True)
    cdef string color_blue(const string& text) nogil:
        cdef:
            string res = CS_BLUE
        res.append(text)
        res.append(CS_RESET_SEQ)
        return res


    @staticmethod
    @cython.binding(True)
    cdef string color_yellow(const string& text) nogil:
        cdef:
            string res = CS_YELLOW
        res.append(text)
        res.append(CS_RESET_SEQ)
        return res

    @staticmethod
    @cython.binding(True)
    cdef string color_magenta(const string& text) nogil:
        cdef:
            string res = CS_MAGENTA
        res.append(text)
        res.append(CS_RESET_SEQ)
        return res

    @staticmethod
    @cython.binding(True)
    cdef string color_white(const string& text) nogil:
        cdef:
            string res = CS_WHITE
        res.append(text)
        res.append(CS_RESET_SEQ)
        return res

    @staticmethod
    @cython.binding(True)
    cdef string color_bold(const string& text) nogil:
        cdef:
            string res = CS_BOLD_SEQ
        res.append(text)
        res.append(CS_RESET_SEQ)
        return res

