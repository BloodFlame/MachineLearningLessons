# coding=utf-8
# 课堂代码复现
import random
import pandas
import re
from collections import Counter
import jieba

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


# print(generate(create_grammar(simple_grammar), 'sentence'));


human = """
human = 自己 寻找 活动
自己 = 我 | 俺 | 我们 
寻找 = 找找 | 想找点 
活动 = 乐子 | 玩的    
"""
host = """
host = 寒暄 报数 询问 业务相关 结尾 
报数 = 我是 数字 号 ,
数字 = 单个数字 | 数字 单个数字 
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 先生 | 女士 | 小朋友
打招呼 = 你好 | 您好 
询问 = 请问你要 | 您需要
业务相关 = 玩玩 具体业务
玩玩 = null
具体业务 = 喝酒 | 打牌 | 打猎 | 赌博
结尾 = 吗？
"""
# for i in range(10):
#     print(generate(create_grammar(human, '='), target='human'));
#     print(generate(create_grammar(host, '='), target='host'));


def token(string):
    return re.findall('\w+', string)


def cut(string):
    return list(jieba.cut(string))


douban = pandas.read_csv('movie_comments.csv', encoding='utf-8', low_memory=False)

articles = douban['comment'].tolist()

articles_clean = [''.join(token(str(e))) for e in articles]

print(cut(articles_clean[1]))





