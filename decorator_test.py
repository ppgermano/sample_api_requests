'''
referencia:
https://stackoverflow.com/questions/14703310/how-can-i-get-a-python-decorator-to-run-after-the-decorated-function-has-complet
'''

def audit_action(action):
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            print(args)
            # Invoke the wrapped function first
            retval = func(*args, **kwargs)
            # Now do something here with retval and/or action
            print('In wrapper_func, handling action {!r} after wrapped function returned {!r}'.format(action, retval))
            args[0].inicial_um = 2
            return retval
        return wrapper_func
    return decorator_func


class Teste():

    def __init__(self):
        self.inicial_um = 1

    @audit_action(action='did something')
    def do_something(*args, **kwargs):
        if args[0] == 'foo':
            return 'bar'
        else:
            return 'baz'

t = Teste()
t.do_something('')
print(t.inicial_um)
