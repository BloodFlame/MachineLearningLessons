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


def get_tokens(articles):
    TOKEN = []
    for article in articles:
        TOKEN += cut(article)
    return TOKEN


def prepare_words(path):
    douban = pandas.read_csv(path, encoding='utf-8', low_memory=False)
    articles = douban['comment'].tolist()
    articles_clean = [''.join(token(str(e))) for e in articles]
    return get_tokens(articles_clean)


def prob_gram_1(word, words_count, len):
    return words_count[word]/len


def prob_gram_2(word1, word2, words_count, len):
    if word1+word2 in words_count:
        return words_count[word1+word2]/len
    else:
        return 1/len


def get_probablity(sentence, words_count, len):
    words = cut(sentence)
    sentence_pro = 1
    for i, word in enumerate(words[:-1]):
        probability = prob_gram_2(words[i], words[i+1], words_count, len)
        sentence_pro *= probability
    return sentence_pro


def generate_best(grammar, target, words_count, len): # you code here
    sentences = []
    for i in range(100):
        sentence = generate(create_grammar(grammar), target)
        probability = get_probablity(sentence, words_count, len)
        sentences.append([
            sentence,
            probability
        ])
    sorted(sentences, key=lambda x:x[1], reverse=True)
    return sentences[0]

TOKEN = prepare_words('movie_comments.csv')

words_count = Counter(TOKEN)

TOKEN_GRAM_2 = [''.join(TOKEN[i:i+2]) for i in range(len(TOKEN[:-2]))]

words_count2 = Counter(TOKEN_GRAM_2)

get_probablity('早上我在天安门看升旗', words_count2, len(TOKEN_GRAM_2))

best_sentence = generate_best(simple_grammar, 'sentence', words_count2, len(TOKEN_GRAM_2))
print(best_sentence)













