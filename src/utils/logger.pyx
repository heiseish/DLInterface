#cython: language_level=3, c_string_type=unicode, c_string_encoding=utf8, boundscheck=False, cdivision=True, wraparound=False
# distutils: language=c++
import logging
import sys
import os
import inspect
import shutil
import pyparsing
from libcpp cimport bool as bool_t
from libcpp.vector cimport vector
from libcpp.string cimport string
from .color cimport ColorSequence

__all__ = ['init_logger', 'get_logger', 'GenericLogger', 'ResultTable']

cdef ColorSequence _tempCS = ColorSequence()
cdef dict _COLORS = {
    'WARNING': _tempCS.YELLOW,
    'INFO': _tempCS.GREEN,
    'DEBUG': _tempCS.BLUE,
    'CRITICAL': _tempCS.YELLOW,
    'ERROR': _tempCS.RED
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, str msg, bool_t use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, object record):
        raw_levelname = record.levelname
        record.levelname = record.levelname.center(7, ' ')
        if self.use_color and raw_levelname in _COLORS:
            record.levelname = _COLORS[raw_levelname] + '[ '+ record.levelname + ' ]' + \
                _tempCS.RESET_SEQ
            record.filename = ColorSequence.color_cyan(record.filename)
            record.name = ColorSequence.color_magenta(record.name)
        return logging.Formatter.format(self, record)

cdef dict _LOGGERS = {
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR
}

class GenericLogger(logging.Logger):
    def __init__(self, str name, str level, bool_t use_color):
        ''' Create a logger based on logging.Logger
        Args:
        - name (str) name of the logger
        - level (str) default level for logging. one of WARNING | INFO | DEBUG | CRITICAL | ERROR
        - use_color (bool) Whether this logger should print out color
        '''
        cdef:
            str FORMAT

        FORMAT = '%(name)s - %(asctime)s - [ %(levelname)s ] - %(filename)s - $BOLD%(lineno)4d:%(funcName)s$RESET: %(message)s'
        if level not in _LOGGERS:
            raise ValueError(
                'level {} is not one of supported logging level'.format(level)
            )
        self.use_color = use_color
        self.log_level = level
        if use_color:
            FORMAT = FORMAT.replace('[', '') \
                .replace(']', '')
            FORMAT = FORMAT.replace('$RESET', _tempCS.RESET_SEQ) \
                .replace('$BOLD', _tempCS.BOLD_SEQ)
        else:
            FORMAT = FORMAT.replace('$BOLD', '') \
                .replace('$RESET', '')

        logging.Logger.__init__(self, name, _LOGGERS[level])
        color_formatter = ColoredFormatter(FORMAT, use_color)
        console = logging.StreamHandler(stream=sys.stdout)
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return

    def get_terminal_width(self):
        ''' Get the width of the console terminal at run time
        '''
        return shutil.get_terminal_size((80, 20)).columns

    def end_section(self, str separator = '-'):
        ''' Print out a dash line to separate logging in command-line
        The separator line will fit the width of the terminal window
        Returns:
        - None
        '''
        col = self.get_terminal_width()
        print(
            '\n{}\n'.format(
                separator * (col // len(separator)) +
                separator[:col % len(separator)]
            ),
            flush=True
        )

    def title(self, str message, str filler = ' '):
        ''' Print out the title of an important process
        Args:
        - message: title to be printed
        - filler: character to filled on 2 sides of the title message
        '''
        col = self.get_terminal_width()
        if self.use_color:
            message = ColorSequence.BOLD_SEQ + message + ColorSequence.RESET_SEQ
            col += len(ColorSequence.BOLD_SEQ) + len(ColorSequence.RESET_SEQ)
        message = ' [ {} ] '.format(
            message
        )  # Add spaces to 2 sides of the message
        print('\n\n{}\n\n'.format(message.center(col, filler)), flush=True)


# default logger is color
cdef object singletonLogger = GenericLogger('DawnAI', 'ERROR', use_color=True)


cpdef object init_logger(str name):
    ''' Initialize global logger. Subsequence use of the logger can be retrieved with `get_logger()`
    Args:
    - name (str) name of the logger
    - log_level (str) minimum log level to print out logging
    - use_color (bool) whether logger use color
    
    Returns:
    - Logger class withe the configs
    '''
    cdef:
        string log_level
    global singletonLogger
    log_level =  b'INFO'
    singletonLogger = GenericLogger(
        name, log_level, use_color=True
    )
    return singletonLogger


cpdef object get_logger():
    ''' Return current logger with current context
    '''
    global singletonLogger
    return singletonLogger


cdef class ResultTable(object):
    cdef int rows, cols, terminal_width, col_width
    cdef vector[string] headers
    cdef str title

    ''' Simple class to print out results in table format. 
    This class does not hold any data in memory, to prevent memory bloat. 
    So data is printed out immediately
    This class is row-major order. We can continue to add rows to the table, but not columns
    '''
    def __cinit__(self, int cols = 1, str title = ''):
        self.rows = 1
        self.cols = cols
        self.terminal_width = shutil.get_terminal_size((120, 20)).columns
        self.col_width = int((self.terminal_width - 2 - self.cols) // self.cols)
        self.title = title

        ESC = pyparsing.Literal('\033')
        integer = pyparsing.Word(pyparsing.nums)
        self.escapeSeq = pyparsing.Combine(
            ESC + '[' +
            pyparsing.Optional(pyparsing.delimitedList(integer, ';')) +
            pyparsing.oneOf(list(pyparsing.alphas))
        )

    cdef str nonAnsiString(self, str s):
        return pyparsing.Suppress(self.escapeSeq).transformString(s)

    cdef void print_horizontal(self) except *:
        print('-' * (self.terminal_width - self.cols), flush=True)

    def set_headers(self, list headers):
        assert len(headers) == self.cols, 'len(headers) != self.cols {} vs {}'.format(
                      len(headers), self.cols
                  )
        for header in headers:
            self.headers.push_back(headers.encode())

    def add_row(self, list data):
        assert len(data
                  ) == self.cols, ' len(data) != self.cols {} vs {}'.format(
                      len(data), self.cols
                  )
        row_str = ''
        for entry in data:
            word_true_len = len(self.nonAnsiString(entry))
            row_str += '|' + entry.center(
                max(0,
                    len(entry) - word_true_len + self.col_width)
            )
        row_str += '|\n'
        print(row_str, flush=True)

    def present(self):
        ''' Start print table'''
        assert not self.headers.empty(), "Headers are not set"
        print(
            '{}\n'.format(
                ' [ {} ] '.format(self.title
                                 ).center(2 + self.cols * self.col_width)
            ),
            flush=True
        )
        self.print_horizontal()
        self.add_row(self.headers)
        self.print_horizontal()

    def close(self):
        self.print_horizontal()
