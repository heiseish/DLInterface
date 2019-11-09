''' Logger class'''
import logging
import os
import inspect
import shutil

__all__ = [
    'init_logger',
    'get_logger'
]

class ColorSequence:
    ''' Contains basic ansii escape sequences
    '''
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(90,98)
    BOLD_SEQ = '\033[1m'
    RESET_SEQ = '\033[0m'
    COLOR_SEQ = '\033[6;{}m'
    


class ColoredFormatter(logging.Formatter):
    _COLORS = {
        'WARNING': ColorSequence.YELLOW,
        'INFO': ColorSequence.GREEN,
        'DEBUG': ColorSequence.BLUE,
        'CRITICAL': ColorSequence.YELLOW,
        'ERROR': ColorSequence.RED
    }
    def __init__(self, msg: str, use_color:bool = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        raw_levelname = record.levelname
        record.levelname = record.levelname.center(7, ' ')
        if self.use_color and raw_levelname in self._COLORS:
            record.levelname = ColorSequence.COLOR_SEQ.format(self._COLORS[raw_levelname]) + '[ '+ record.levelname + ' ]' + \
                ColorSequence.RESET_SEQ
            record.filename = ColorSequence.COLOR_SEQ.format(ColorSequence.CYAN) + record.filename + ColorSequence.RESET_SEQ
            record.name = ColorSequence.COLOR_SEQ.format(ColorSequence.MAGENTA) + record.name + ColorSequence.RESET_SEQ
        return logging.Formatter.format(self, record)


class Logger(logging.Logger):
    _LOGGERS = {
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR
    }
    def __init__(self, name: str, level: str, use_color: bool):
        ''' Create a logger based on logging.Logger
        Args:
        - name (str) name of the logger
        - level (str) default level for logging. one of WARNING | INFO | DEBUG | CRITICAL | ERROR
        - use_color (bool) Whether this logger should print out color
        '''
        FORMAT = '%(name)s - %(asctime)s - [ %(levelname)s ] - %(filename)s - $BOLD%(lineno)4d:%(funcName)s$RESET: %(message)s'
        if level not in self._LOGGERS:
            raise ValueError('level {} is not one of supported logging level'.format(level))
        self.use_color = use_color
        if use_color:
            FORMAT = FORMAT.replace('[', '') \
                .replace(']', '')
            FORMAT = FORMAT.replace('$RESET', ColorSequence.RESET_SEQ) \
                .replace('$BOLD', ColorSequence.BOLD_SEQ)
        else:
            FORMAT = FORMAT.replace('$BOLD', '') \
                .replace('$RESET', '')

            
        logging.Logger.__init__(self, name, self._LOGGERS[level])                
        color_formatter = ColoredFormatter(FORMAT, use_color)
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return

    
    def get_terminal_width(self) -> int:
        ''' Get the width of the console terminal at run time
        '''
        return shutil.get_terminal_size((80, 20)).columns

    def end_section(self, separator='-'):
        ''' Print out a dash line to separate logging in command-line
        The separator line will fit the width of the terminal window
        Returns:
        - None
        '''
        col = self.get_terminal_width()
        print('\n{}\n\n'.format(separator * (col // len(separator)) + separator[:col % len(separator)]))

    def title(self, message:str, filler:str=' '):
        ''' Print out the title of an important process
        Args:
        - message: title to be printed
        - filler: character to filled on 2 sides of the title message
        '''
        message = ' [ {} ] '.format(message)
        col = self.get_terminal_width()
        if self.use_color:
            message = ColorSequence.BOLD_SEQ + message + ColorSequence.RESET_SEQ
            col += len(ColorSequence.BOLD_SEQ) + len(ColorSequence.RESET_SEQ)
        message = ' {} '.format(message) # Add spaces to 2 sides of the message
        print('{}\n\n'.format(message.center(col, filler)))



# default logger is color
my_logger = Logger('DawnAI', 'INFO', use_color = True)

def init_logger(name, level = 'INFO', use_color = True):
    global my_logger 
    my_logger = Logger(name, level, use_color)
    return my_logger

def get_logger():
    global my_logger 
    return my_logger