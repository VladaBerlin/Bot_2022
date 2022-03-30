import os
import re

punctuation = ['.', ',', '!', '?', '—', ';', ':', ')', '»', '…']

texts = []
for poem in os.listdir('./texts'):
    new_text = []
    with open('./texts/' + poem, encoding='utf8') as file:
        text = file.readlines()
        i = 0
        for l in text:
            l = re.sub(r"\d+", "",l, flags=re.UNICODE)  # Если есть число, то убираем

            if not l.endswith('\n'):    #Если на конце нет переноса строки, то вставляем
                l += '\n'

            if l == '\n':   #Если строка состоит только из знака переноса, то переходим к следующей строке
                i += 1
                continue

            while l[-2] in punctuation: #Если на конце строки есть пунктуация, то убираем
                l = l[:-2] + l[-1:]

            if l[-2] == ' ':    #Мне приходится убирать пробел здесь, а не в предыдущем цикле, тк иначе питон ругается
                l = l[:-2] + l[-1:]

            while l[-2] in punctuation: #Бывают случаи, где знаки пунктуации разделены пробелами
                l = l[:-2] + l[-1:]

            new_text.append(l)
            i += 1
        texts.extend(new_text)

with open('one_poem_full.txt', 'w', encoding='utf8') as new_file:
    new_file.writelines(texts)
