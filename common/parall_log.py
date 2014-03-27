"""ANSII Color formatting for output in terminal."""

import os
import common.mylogging  as mylogging
import time


__ALL__ = [ 'colored' ]


ATTRIBUTES = dict(
        zip([
            'bold',
            'dark',
            '',
            'underline',
            'blink',
            '',
            'reverse',
            'concealed'
            ],
            range(1, 9)
            )
        )
del ATTRIBUTES['']


HIGHLIGHTS = dict(
        zip([
            'on_grey',
            'on_red',
            'on_green',
            'on_yellow',
            'on_blue',
            'on_magenta',
            'on_cyan',
            'on_white'
            ],
            range(40, 48)
            )
        )


COLORS = dict(
        zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            ],
            range(30, 38)
            )
        )


RESET = '\033[0m'
 
def colored(text, color=None, on_color=None, attrs=None):
    """Colorize text.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')
    """
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        if on_color is not None:
            text = fmt_str % (HIGHLIGHTS[on_color], text)

        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)

        text += RESET
    return text

class splog(object):
    def __init__(self ,logger_name="parun.log"):
        self.logbuf = ""
        self.logger = mylogging.getLogger(logger_name)

    def update_kwargs(self):
        try:
            fn, lno, func = self.logger.findCaller()
            fn = os.path.basename(fn)
        except Exception:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        std_day = time.ctime(time.time())
        return fn,lno,func,std_day

    def raw(self,logformat,*args):
        if type(logformat) == "str":
            tmpstr = logformat % args
        else:
            tmpstr = str(logformat)
        self.logbuf = self.logbuf + "\n" + tmpstr
 
    def error(self,logformat,*args):
        fn,lno,func,std_day = self.update_kwargs()
        error = colored("ERROR    ",'red')
        formatstr = "[" + error + std_day + "  "+ fn + ":" + str(lno) + " " + func + "]"
        if type(logformat) == "str":
            logstr = logformat % args
        else:
            logstr = str(logformat)
        self.logbuf = self.logbuf + "\n" + formatstr + logstr

    def info(self,logformat,*args):
        fn,lno,func,std_day = self.update_kwargs()
        info = colored("INFO    ",'green')
        formatstr = "[" + info +  std_day + "  "+ fn + ":" + str(lno) + " " + func + "]"
        if type(logformat) == "str":
            logstr = logformat % args
        else:
            logstr = str(logformat)
        self.logbuf = self.logbuf + "\n" + formatstr + logstr
        
    def warning(self,logformat,*args):
        fn,lno,func,std_day = self.update_kwargs()
        info = colored("WARNING    ",'yellow')
        formatstr = "[" + info +  std_day + "  "+ fn + ":" + str(lno) + " " + func + "]"
        if type(logformat) == "str":
            logstr = logformat % args
        else:
            logstr = str(logformat)
        self.logbuf = self.logbuf + "\n" + formatstr + logstr
 
    def success(self,logformat,*args):
        if type(logformat) == "str":
            logstr = logformat % args
        else:
            logstr = str(logformat)
        tmpstr = colored(logstr, "green")
        self.logbuf = self.logbuf + "\n" + tmpstr

    def fail(self,logformat,*args):
        if type(logformat) == "str":
            logstr = logformat % args
        else:
            logstr = str(logformat)
        tmpstr = colored(logstr, "red",attrs=['blink'])
        self.logbuf = self.logbuf + "\n" + tmpstr
        
    def start(self,logformat,*args):
        fn,lno,func,std_day = self.update_kwargs()
        log = colored("START    " ,'magenta',attrs=['dark'])
        formatstr = "[" + log + std_day + "  "+ fn + ":" + str(lno) + " " + func + "]"
        logstr = logformat % args
        self.logbuf = self.logbuf + "\n" + formatstr + logstr
        
    def end(self,logformat,*args):
        fn,lno,func,std_day = self.update_kwargs()
        log = colored("END    " ,'magenta',attrs=['dark'])
        formatstr = "[" + log + std_day + "  "+ fn + ":" + str(lno) + " " + func + "]"
        logstr = logformat % args
        self.logbuf = self.logbuf + "\n" + formatstr + logstr
 
    def PrintParLog(self):
        print self.logbuf
        self.logbuf=""

autoParLog = splog()

