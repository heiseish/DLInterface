#cython: language_level=3, c_string_type=unicode, c_string_encoding=utf8, boundscheck=False, cdivision=True, wraparound=False
# distutils: language=c++

cpdef object init_logger(str name)
cpdef object get_logger()
