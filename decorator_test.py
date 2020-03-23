'''
referencia:
https://stackoverflow.com/questions/14703310/how-can-i-get-a-python-decorator-to-run-after-the-decorated-function-has-complet
'''


# def audit_action(function_to_decorate):
#     def wrapper(*args, **kw):
#         # Calling your function
#         output = function_to_decorate(*args, **kw)
#         # Below this line you can do post processing
#         print("In Post Processing....")
#         args[0].inicial_um = 2
#         return output
#     return wrapper

def audit_action():
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            # Invoke the wrapped function first
            retval = func(*args, **kwargs)
            # Now do something here with retval and/or action
            print('In wrapper_func, handling action  after wrapped function returned {!r}'.format(retval))
            args[0].inicial_um = 2
            return retval
        return wrapper_func
    return decorator_func


class Teste():

    def __init__(self):
        self.inicial_um = 1

    @audit_action()
    def do_something(self, *args, **kwargs):
        if args[0] == 'foo':
            return 'bar'
        else:
            return 'baz'

t = Teste()
t.do_something('asd')
print(t.inicial_um)
