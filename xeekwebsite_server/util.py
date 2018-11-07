import os
import functools

def execption_handle(view):
    @functools.wraps(view)
    def ex_handle(*args,**kargs):
        try:
            return view(*args,**kargs)
        except Exception as e:
            print('An exception happenning: %s' % str(e))
    return ex_handle