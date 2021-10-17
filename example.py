
"""A good example to write PEG by pyparsing
"""

import pyparsing as pp

"""PEG:
L0 = <identifier> | ( L3 )
L1 = '-'? L0
L2 = L1 (('*'|'/')L1)*
L3 = L2 (('+'|'-')L2)*

Example: (a+b) * (c+d)+f
"""

class basic_code:
    # basic code for PEG
    L3 = pp.Forward()
    L0 = pp.pyparsing_common.identifier | pp.Suppress('(') + L3 + pp.Suppress(')')
    L1 = pp.Optional('-') + L0
    L2 = pp.delimitedList(L1, pp.oneOf(('*','/')))
    L3 <<= pp.delimitedList(L2, pp.oneOf(('+', '-')))

    result = L3.parseString('(a+b) * (c+d)')


class unwork_code:
    # code as CFG, but does not work
    S = pp.pyparsing_common.identifier | pp.Suppress('(') + S + pp.Suppress(')')
    S = pp.Optional('-') + S
    S = S + pp.oneOf(('*','/')) + S
    S = S + pp.oneOf(('+','-')) + S

    result = S.parseString('(a+b) * (c+d)')


class Action:
    terms = []
    def __init__(self, instring, loc, tokens):
        self.tokens = tokens

    def __contains__(self, name):
        return name in self.tokens


class MultiplyAction(Action):

    def get_terms(self):
        terms = []
        for t in self.tokens:
            if isinstance(t, str):
                terms.append(t)
            elif isinstance(t, PlusAction):
                ts = t.get_terms()
                if len(ts)==1:
                    if isinstance(ts[0], str):
                        terms.append(ts[0])
                    elif isinstance(ts[0], MultiplyAction):
                        terms.extend(ts[0].get_terms())
                else:
                    terms.append(t)
        return terms

    def __str__(self):
        return f'*({", ".join(map(str, self.get_terms()))})'


class PlusAction(Action):

    def get_terms(self):
        terms = []
        for t in self.tokens:
            if isinstance(t, str):
                terms.append(t.tokens[0])
            elif isinstance(t, MultiplyAction):
                ts = t.get_terms()
                if len(ts)==1:
                    if isinstance(ts[0], str):
                        terms.append(ts[0])
                    elif isinstance(ts[0], PlusAction):
                        terms.extend(ts[0].get_terms())
                else:
                    terms.append(t)
        return terms

    def __str__(self):
        ts = self.get_terms()
        if len(ts)==1:
            return ts[0]
        else:
            return f'{self.op}({", ".join(map(str, self.get_terms()))})'

L3 = pp.Forward()
L0 = pp.pyparsing_common.identifier('identifier') | pp.Suppress('(') + L3('block') + pp.Suppress(')')
L1 = pp.Combine(pp.Optional('-') + L0)
L2 = pp.delimitedList(L1, pp.oneOf(('*','/'))('op'))
L2.setParseAction(MultiplyAction)
L3 <<= pp.delimitedList(L2, pp.oneOf(('+', '-'))('op'))
L3.setParseAction(PlusAction)

result = L3.parseString('a+((b+c)*t*(k*g)+d)')

pr = result[0]
print(pr)
