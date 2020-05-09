from .context import get_context
__all__ = ['ColorSequence']


class ColorSequence(object):
    ''' Contains basic ansii escape sequences
    '''
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(90, 98)
    BOLD_SEQ = '\033[1m'
    RESET_SEQ = '\033[0m'
    COLOR_SEQ = '\033[6;{}m'

    @classmethod
    def color_red(cls, text: str) -> str:
        if get_context().no_color:
            return text
        return '{}{}{}'.format(
            cls.COLOR_SEQ.format(cls.RED), text, cls.RESET_SEQ
        )

    @classmethod
    def color_blue(cls, text: str) -> str:
        if get_context().no_color:
            return text
        return '{}{}{}'.format(
            cls.COLOR_SEQ.format(cls.BLUE), text, cls.RESET_SEQ
        )

    @classmethod
    def color_green(cls, text: str) -> str:
        if get_context().no_color:
            return text
        return '{}{}{}'.format(
            cls.COLOR_SEQ.format(cls.GREEN), text, cls.RESET_SEQ
        )

    @classmethod
    def color_yellow(cls, text: str) -> str:
        if get_context().no_color:
            return text
        return '{}{}{}'.format(
            cls.COLOR_SEQ.format(cls.YELLOW), text, cls.RESET_SEQ
        )

    @classmethod
    def color_magenta(cls, text: str) -> str:
        if get_context().no_color:
            return text
        return '{}{}{}'.format(
            cls.COLOR_SEQ.format(cls.MAGENTA), text, cls.RESET_SEQ
        )

    @classmethod
    def color_cyan(cls, text: str) -> str:
        if get_context().no_color:
            return text
        return '{}{}{}'.format(
            cls.COLOR_SEQ.format(cls.CYAN), text, cls.RESET_SEQ
        )

    @classmethod
    def color_black(cls, text: str) -> str:
        if get_context().no_color:
            return text
        return '{}{}{}'.format(
            cls.COLOR_SEQ.format(cls.BLACK), text, cls.RESET_SEQ
        )

    @classmethod
    def color_white(cls, text: str) -> str:
        if get_context().no_color:
            return text
        return '{}{}{}'.format(
            cls.COLOR_SEQ.format(cls.WHITE), text, cls.RESET_SEQ
        )
