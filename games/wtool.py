from logic import *

adw = ADW('SPOON', 'LADLE')

def val(a, g):
    return adw.validate(a, g)

def rem(ans, g, fb):
    r = []
    for a in ans:
        if val(a, g) == fb:
            r.append(a)
    return r

    
