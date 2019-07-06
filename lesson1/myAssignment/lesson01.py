# coding=utf-8
# 课堂代码复现
import random

simple_grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>  蓝色的 | 好看的 | 小小的
"""


def create_grammar(grammar_str, split='=>', line_split='\n'):
    grammar = {}
    for line in grammar_str.split(line_split):
        if not line.strip():
            continue
        exp, stmt = line.split(split)
        grammar[exp.strip()] = [s.split() for s in stmt.split('|')]
    return grammar


def generate(grammar, target):
    if target not in grammar:
        return target
    expanded = [generate(grammar, t) for t in random.choice(grammar[target])]
    return ''.join(e for e in expanded if e!= 'null' and e!='/n')


print(generate(create_grammar(simple_grammar), 'sentence'));

