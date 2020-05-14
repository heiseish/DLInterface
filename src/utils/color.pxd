#cython: language_level=3, c_string_type=unicode, c_string_encoding=utf8, boundscheck=False, cdivision=True, wraparound=False
# distutils: language=c++

from libcpp.vector cimport vector
from libcpp.string cimport string


cdef class ColorSequence:

    @staticmethod
    cdef string color_cyan(const string& text) nogil
    @staticmethod
    cdef string color_green(const string& text) nogil
    @staticmethod
    cdef string color_red(const string& text) nogil
    @staticmethod
    cdef string color_blue(const string& text) nogil
    @staticmethod
    cdef string color_yellow(const string& text) nogil
    @staticmethod
    cdef string color_magenta(const string& text) nogil
    @staticmethod
    cdef string color_white(const string& text) nogil
    @staticmethod
    cdef string color_bold(const string& text) nogil
        