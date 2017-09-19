
def tokenizer(str):
    return str.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(tokenlist):
    '''simple parser, not complete! some parse error would not be find, eg: (345), will crash in runtime!'''
    if len(tokenlist) == 0:
        raise SyntaxError("Error! Unexpected EOF while reading")

    token = tokenlist.pop(0)
    if token == '(':
        if tokenlist[0] == ')':
            raise SyntaxError("Parse Error! Empty expression!") # "exclude () expression"

        L = []
        while tokenlist[0] != ')':
            L.append(parse(tokenlist))
        tokenlist.pop(0)
        return L
    elif token == ')':
        raise SyntaxError("Unexpected )")
    else:
        return atom(token)

def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

Symbol = str          # A Scheme Symbol is implemented as a Python str
List   = list         # A Scheme List is implemented as a Python list
Number = (int, float) # A Scheme Number is implemented as a Python int or float


import math
import operator as op

class Env(dict):
    def __init__(self, params, args, outer_env):
        self.update(zip(params, args))
        self.outer = outer_env

    def find(self, name):
        if name in self:
            return self #!!!
        elif self.outer == None:
            raise EnvironmentError("Error! Identifer " + name + " is undefined!")
        else:
            return self.outer.find(name)

def standard_env():
    env = Env((),(),None)
    env.update(vars(math))
    env.update({    # add build-in functions to initial environment!
        '+': op.add, '-':op.sub, '*':op.mul, # '/':op.div,
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
        'abs':     abs,
        'append':  op.add,  
        # 'apply':   apply,
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()

class closure(object):
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval(self.body, Env(self.params, args, self.env))


def eval(expr, env):
    if isinstance(expr, Symbol):    # Symbol
        return env.find(expr)[expr]
    
    if not isinstance(expr, List):  # Number (not Symbol, not List)
        return expr

    if expr[0] == 'quote':
        (_,expr1) = expr
        return expr1

    if expr[0] == 'set!':
        (_, var, expr1) = expr
        env.find(var)[var] = eval(expr1, env) 

    if expr[0] == 'lambda':
        (_, param, body) = expr
        return closure(param, body, env)

    if expr[0] == 'if':
        (_, test, expr1, expr2) = expr
        if eval(test, env):
            return eval(expr1, env)
        else:
            return eval(expr2, env)
    
    if expr[0] == 'define':
        (_, name, expr1) = expr
        env[name] = eval(expr1, env)
    else:
        proc = eval(expr[0], env)
        args = [eval(i, env) for i in expr[1:]]
        return proc(*args)

def repl(prompt = 'lispy>'):
    while True:
        try:
            prog = input(prompt).strip()
            if prog in ["exit","exit()","quit","quit()"]:
                return
            elif prog != "":
                val = eval(parse(tokenizer(prog)), global_env)
                if val != None:
                    print(val)
        except SyntaxError as e:
            print(e)
        except EnvironmentError as e:
            print(e)
