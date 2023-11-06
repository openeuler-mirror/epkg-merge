# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

# 使用ply库实现一个DSL解释器，能够执行条件语句

from ply.lex import lex
from ply.yacc import yacc

from distutils.version import LooseVersion

from src.log import log



# 定义词法分析器
tokens = (
    'VERSION', 'NAME', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUAL', 'EQUAL2',
    'LPAREN', 'RPAREN', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'NOT_EQUAL',
    'AND', 'AND2', 'OR', 'OR2', 'NOT', 'NOT2', 'STRING', 'LSQUARE', 'RSQUARE',
    'IN', 'NOTIN', 'FALSE', 'TRUE',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'='
t_EQUAL2 = r'=='
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_GREATER = r'>'
t_LESS = r'<'
t_GREATER_EQUAL = r'>='
t_LESS_EQUAL = r'<='
t_NOT_EQUAL = r'!='
t_AND2 = r'&&'
t_OR2 = r'\|\|'
t_NOT2 = r'!'
t_STRING = r'\".*?\"'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'


def t_NOTIN(t):
    r'not\s+in\s*'
    t.value = str(t.value).strip()
    return t


def t_IN(t):
    r'in\s*'
    t.value = str(t.value).strip()
    return t


def t_NOT(t):
    r'not'
    return t


def t_OR(t):
    r'or'
    return t


def t_AND(t):
    r'and'
    return t


def t_TRUE(t):
    r'(TRUE)|(True)|(true)'
    t.value = True
    return t


def t_FALSE(t):
    r'(FALSE)|(False)|(false)'
    t.value = False
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_-]*\s*'
    t.type = 'NAME'
    t.value = str(t.value).strip()
    return t


def t_VERSION(t):
    r'\d*\.[\d*\.]+[-+.\d]*'
    t.type = 'VERSION'
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    log.debug("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


t_ignore = ' \t'

lexer = lex()

# 定义语法分析器
precedence = (
    ('left', 'OR', 'OR2', 'AND', 'AND2'),
    ('left', 'NOT'),
    ('left', 'NOT2'),
    ('nonassoc', 'EQUAL', 'EQUAL2', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
    ('nonassoc', 'STRING'),
    ('left', 'LSQUARE'),
    ('left', 'IN'),
    ('left', 'NOTIN'),
)


def p_statement_expr(p):
    '''statement : expression'''
    p[0] = p[1]


# Define a new production rule for parsing list literals
def p_expression_list(p):
    "expression : LSQUARE expression_list RSQUARE"
    p[0] = p[2]


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression GREATER expression
                  | expression LESS expression
                  | expression GREATER_EQUAL expression
                  | expression LESS_EQUAL expression
                  | expression EQUAL expression
                  | expression EQUAL2 expression
                  | expression NOT_EQUAL expression
                  | expression AND expression
                  | expression AND2 expression
                  | expression OR expression
                  | expression OR2 expression
                  | NOT expression
                  | NOT2 expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            p[0] = None
        else:
            p[0] = p[1] / p[3]
    elif p[2] == '>':
        p[1], p[3] = convert(p[1], p[3])
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[1], p[3] = convert(p[1], p[3])
        p[0] = p[1] < p[3]
    elif p[2] == '>=':
        p[1], p[3] = convert(p[1], p[3])
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[1], p[3] = convert(p[1], p[3])
        p[0] = p[1] <= p[3]
    elif p[2] == '=' or p[2] == '==':
        p[1], p[3] = convert(p[1], p[3])
        p[0] = p[1] == p[3]
    elif p[2] == 'and' or p[2] == '&&':
        p[0] = p[1] and p[3]
    elif p[2] == 'or' or p[2] == '||':
        p[0] = p[1] or p[3]
    elif p[1] == 'not' or p[1] == '!':
        p[0] = not p[2]
    elif p[2] == '!=':
        p[0] = (p[1] != p[3])

def convert(p1,p2):
    if type(p1)==type(p2):
        return p1, p2
    return str(p1), str(p2)


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    if type(p[2]) is str:
        p[0] = "-{}".format(p[2])
        return
    p[0] = -p[2]


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]


def p_expression_version_binop(p):
    '''expression :  expression_version GREATER expression_version
                  | expression_version LESS expression_version
                  | expression_version GREATER_EQUAL expression_version
                  | expression_version LESS_EQUAL expression_version
                  | expression_version EQUAL expression_version
                  | expression_version EQUAL2 expression_version
                  | expression_version NOT_EQUAL expression_version'''

    p[1] = LooseVersion(p[1])
    p[3] = LooseVersion(p[3])
    if p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '=' or p[2] == '==':
        p[0] = p[1] == p[3]


def p_expression_version(p):
    '''expression_version : VERSION'''
    p[0] = p[1]


def p_expression_name(p):
    '''expression : NAME'''
    p[0] = p[1]


def p_expression_string(p):
    '''expression : STRING'''
    p[0] = p[1]


def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = p[1]


def p_expression_list_items(p):
    '''expression_list_ex : expression_list_ex expression
                       | expression'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
        return

    if type(p[1]) == list:
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_expression_list_convert(p):
    '''expression_list : expression_list_ex
                       | LSQUARE expression_list_ex RSQUARE'''
    if len(p) == 4:
        p[0] = p[2]
        return

    p[0] = p[1]


def p_expression_in(p):
    "expression : expression IN expression_list"
    from src.core.config_space import config_space
    if p[1] == "arch":
        p[1] = config_space.arch
    p[0] = p[1] in p[3]


def p_expression_notin(p):
    "expression : expression NOTIN expression_list"
    from src.core.config_space import config_space
    if p[1] == "arch":
        p[1] = config_space.arch
    p[0] = p[1] not in p[3]


def p_error(p):
    log.debug("Syntax error in input! {}".format(str(p)))


parser = yacc()

if __name__ == '__main__':
    parser.parse("arch in x86_64 arm64", debug=True)
