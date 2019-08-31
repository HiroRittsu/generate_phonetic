# coding: utf-8
from janome.tokenizer import Tokenizer
import jctconv
import re
import os
import sys
import docx2txt


def disassembly(token):
    chinese_flag = False
    before_kana = ''
    chinese = ''
    feed = ''
    read = jctconv.kata2hira(token.reading)
    for i in token.surface:
        if re.search('[\u4E00-\u9FD0]', i):
            chinese = chinese + i
            chinese_flag = True
        elif chinese_flag:
            feed = feed + i
        elif not chinese_flag:  # 漢字の前にある、送り仮名以外の文字
            before_kana = before_kana + i
    read = re.sub(feed, '', read)
    read = re.sub(before_kana, '', read)
    return before_kana, chinese, read, feed


def add_phonetic(token):
    if re.search('[0-9a-zA-Zあ-んア-ン]', token.surface):  # 漢字以外が含まれている場合
        result = disassembly(token)
        return result[0] + '｜' + result[1] + '（' + result[2] + '）' + result[3]
    else:
        return '｜' + token.surface + '（' + jctconv.kata2hira(token.reading) + '）'


def anaryze(sentence):
    print("解析中...")
    output = ''
    t = Tokenizer()
    tokens = t.tokenize(sentence)
    for token in tokens:
        if re.search('[\u4E00-\u9FD0]', token.surface):
            output = output + add_phonetic(token)
        else:
            output = output + token.surface
    print(output)
    return output


def main(file):
    result = ''
    name = file.split('\\')[-1]
    PATH = re.sub(name, '', file)
    name = name.replace(".docx", ".txt")

    folder = PATH + name.replace(".txt", "") + '_img'
    os.mkdir(folder)
    text = docx2txt.process(file, folder)
    text = jctconv.h2z(text, kana=False, digit=True,
                       ascii=False)  # 数字を全角に変換
    result = anaryze(text)

    with open(PATH+'new_'+name, mode='w') as f:
        f.write('[simpleruby]\n')
        f.write(result)
        f.write('\n[/simpleruby]')


if __name__ == '__main__':
    args = sys.argv
    print("変換対象 → ", args[1])

    if args[1].split(".")[-1] == 'docx':
        main(args[1])
    else:
        print("")
        print("Wordファイルのみ受け付けます。")
        print("")
