import typing, re
import tokens, lang_wrappers

class Tokenize:
    """
    types:int, bool, str, float, callable, object
    empty pointer:null
    """
    grammer = r'@|\bfunc\b|\bclass\b|\battr\b|\bhook\b|\bstr\b|\bbool\b|\bint\b|\bfloat\b|\bcallable\b|\bobject\b|\bnull\b|\bTrue\b|\bFalse\b|\bswitch\b|\bcase\b|\bif\b|\belif\b|\belse\b|\bwhile\b|\bfor\b|\bin\b|\-\>|\+\+|\-\-|[\*\-\+]{1}\=|\=\=|\<\=|\>\=|\=|\<|\>|\+|\-|\*|/|:|\(|\)|\[|\]|\{|\}|\.|^\s+|,|"[\w\W]+"|\b\d+\.\d+\b|\b\d+\b|\b\w+\b'
    token_list = [['at', 'denote', r'@'], ['identifier', 'func', r'\bfunc\b'], ['identifier', 'class', r'\bclass\b'], ['identifier', 'attr', r'\battr\b'], ['identifier', 'hook', r'\bhook\b'], ['lang_type', 'str', r'\bstr\b'], ['lang_type', 'bool', r'\bbool\b'], ['lang_type', 'int', r'\bint\b'], ['lang_type', 'float', r'\bfloat\b'], ['lang_type', 'callable', r'\bcallable\b'], ['lang_type', 'object', r'\bobject\b'], ['pointer', 'null', r'\bnull\b'], ['boolean', 'True', r'\bTrue\b'], ['boolean', 'False', r'\bFalse\b'], ['boolean', 'False', r'\bFalse\b'], ['control', 'switch', r'\bswitch\b'], ['control', 'case', r'\bcase\b'], ['control', 'if', r'\bif\b'], ['control', 'elif', r'\belif\b'], ['control', 'else', r'\belse\b'], ['repetitive', 'while', r'\bwhile\b'], ['repetitive', 'for', r'\bfor\b'], ['loop_control', 'in', r'\bin\b'], ['operation', 'arrow', r'\-\>'], ['operator', 'increment', r'\+\+'], ['operator', 'decrement', r'\-\-'], ['operator', 'inplace', r'[\*\-\+]{1}\='], ['operator', 'equals', r'\=\='], ['operator', 'le', r'\<\='], ['operator', 'ge', r'\>\='], ['operation', 'assign', r'\='], ['operator', 'lt', r'\<'], ['operator', 'gt', r'\>'], ['operator', 'add', r'\+'], ['operator', 'sub', r'\-'], ['operator', 'mul', r'\*'], ['operator', 'div', r'/'], ['operation', 'colon', r':'], ['brace', 'lparen', r'\('], ['brace', 'rparen', r'\)'], ['brace', 'lsqure', r'\['], ['brace', 'rsquare', r'\]'], ['brace', 'lcurly', r'\{'], ['brace', 'rcurly', r'\}'], ['operation', 'dot', r'\.'], ['whitespace', 'space', r'^\s+'], ['comma', 'comma', r','], ['value', 'string', r'"[\w\W]+"'], ['value', 'float', r'\b\d+\.\d+\b'], ['value', 'integer', r'\b\d+\b'], ['name', 'variable', r'\b\w+\b']]
    @classmethod
    def _tokenize_line(cls, _line:str) -> typing.List[typing.Any]:
        
        _result = []
        for i in re.findall(cls.grammer, _line):
            print(i)
            _r = [[*c, i] for c in cls.token_list if re.findall(c[-1], i)][0]
            print(_r)
            _result.append(tokens.Token(*_r))
        return _result
        #return [tokens.Token(*[[*c, i] for c in cls.token_list if re.findall(c[-1], i)][0]) for i in re.findall(cls.grammer, _line)]

    @classmethod
    @lang_wrappers.to_iter(True)
    def tokenize(cls, _filename:str) -> typing.List[typing.List[typing.Any]]:
        return list(filter(None, [cls._tokenize_line(i.strip('\n')) for i in open(_filename)]))

if __name__ == "__main__":
    print(Tokenize.tokenize('testing_file.txt'))
