#cython: language_level=3

from argparse import Namespace, ArgumentParser
import logging
from libcpp cimport bool as bool_t


__all__ = ['Context', 'get_context', 'init_context', 'generate_context_params']

global_params = ['debug', 'no_color']

cdef class ContextCy(object):
    cdef bool_t debug
    cdef bool_t no_color
    cdef bool_t logging_off

    def __cinit__(self):
        self.debug = False
        self.no_color = False
        self.logging_off = False

    @classmethod
    def from_arg(cls, args: Namespace):
        ctx = cls()
        ctx.debug = getattr(args, 'debug', False)
        ctx.no_color = getattr(args, 'no_color', False)
        ctx.logging_off = getattr(args, 'logging_off', False)
        if ctx.logging_off:
            logging.disable(logging.CRITICAL)
        return ctx

    @staticmethod
    def register_context_params(parser: ArgumentParser):
        parser.add_argument(
            '--debug',
            dest='debug',
            action='store_true',
            help='Run in debug mode'
        )
        parser.add_argument(
            '--no_color',
            dest='no_color',
            action='store_true',
            help='Dont use color logging'
        )
        parser.add_argument(
            '--logging_off',
            dest='logging_off',
            action='store_true',
            help=
            'Turn off logging completely. This is usually used during unittesting'
        )
        return parser

    def __hash__(self):
        return hash(self.debug) ^ hash(self.no_color)

class Context(ContextCy):
    pass

    
context = Context()


def get_context():
    global context
    return context


def init_context(args: Namespace):
    global context
    context = Context.from_arg(args)
    return context


def generate_context_params():
    ''' Generate context params to pass down to child process
    Returns:
    - An args-parser formatted string which contain the context information
    '''
    global context
    attr_list = [
        a for a in dir(context)
        if not a.startswith('__') and not callable(getattr(context, a))
    ]
    params = ' '
    for attr in attr_list:
        if attr not in global_params:
            continue
        att = getattr(context, attr)
        if isinstance(att, bool):
            if att:
                params += '--{} '.format(attr)
        else:
            params += '--{} {} '.format(attr, att)
    return params

