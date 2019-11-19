import os
import functools
from xeekwebsite_server.LogFactory import LogInfo

def execption_handle(view):
    @functools.wraps(view)
    def ex_handle(*args,**kargs):
        try:
            return view(*args,**kargs)
        except Exception as e:
            LogInfo().logger.error('An exception happenning: %s' % str(e))
    return ex_handle