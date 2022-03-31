import telebot
import conf
import requests
import random

vowels = ['а', 'о', 'и', 'э', 'у', 'я', 'ю', 'е', 'ы']
pairs = {'в':'ф', 'ф':'в', 'б':'п', 'п':'б', 'г':'к', 'к':'г', 'з':'с', 'с':'з', 'д':'т', 'т':'д', 'ж':'ш', 'ш':'ж'}
voiceless = ['ф', 'п', 'к', 'с', 'т', 'ш']
voice = ['в', 'б', 'г', 'з', 'б', 'ж']
sonorants = ['л', 'м', 'р', 'н']

bot = telebot.TeleBot(conf.TOKEN)

@bot.message_handler(commands=['start', 'help'])

def send_welcome(message):
    bot.send_message(message.chat.id,
    'Здравствуйте! Это бот, который в ответ на слова или его часть ответит вам в рифму строчкой Некрасова. Вы можете похвалить меня, нажав команду well_done и сообщить мне о плохом качестве работы с помощью команды bad.')
    bot.send_photo(message.chat.id,
    'https://i.pinimg.com/736x/63/e8/a9/63e8a973ea4a2d275296edbc878be4cd--pembroke-welsh-corgi-dog-videos.jpg')

@bot.message_handler(commands=['well_done'])
def good_note(message):
    bot.send_message(message.chat.id, 'Спасибо, мне очень приятно')
    bot.send_photo(message.chat.id,
    'https://i.pinimg.com/736x/cc/bc/08/ccbc086f637f654c436aa2af029a585c.jpg')

@bot.message_handler(commands=['bad'])
def good_note(message):
    bot.send_message(message.chat.id,
    'Жаль, что Вам не понравилось, но критику нужно уметь принимать. Если у Вас есть идеи или советы по улучшению бота, можете писать моему создателю.')
    bot.send_photo(message.chat.id,
    'https://sun9-11.userapi.com/impf/3yoc8-s72NGCpZ9uxt-8-xYXihFlFELdIlJ7IQ/5dB10wtDhNo.jpg?size=900x1600&quality=95&sign=f4e091ca7f0f113c575ac7a24918f426&type=album')

@bot.message_handler(func=lambda m: True)

def send_poem(message):
    mes = message.text
    rhyme_word = []
    rhyme_sim = []

    with open('one_poem_full.txt', encoding = 'utf8') as file:
        poems = file.readlines()
        for line in poems:
            # Я решила, что наилучшая рифма - это рифма с тем же словом
            if line[:-1].endswith(mes):
                rhyme_word.append(line[:-1])             
    if rhyme_word:
        ri = random.randint(0, len(rhyme_word) - 1)
        bot.send_message(message.chat.id, rhyme_word[ri])
    else:
        # Если этого слова в такой форме нет, то пытаемся найти более-менее похожие слова
        for line in poems:
            count_sim = 0
            for i in range(-1, 0 - min(len(mes), len(line)), -1):
                #Я предполагаю, что слова точно не рифмуются, если в словах не совпадают слоговые схемы
                if (line[:-1][i] in vowels and mes[i] not in vowels) or (mes[i] in vowels and line[:-1][i] not in vowels)::
                    break
                if line[:-1][i] == mes[i]:
                    count_sim += 1
                # Для улучшения соответствия я добавила немного фонетики в виде озвончения/оглушения
                elif (line[:-1][i] == 'о' and mes[i] == 'а') or (line[:-1][i] == 'а' and mes[i] == 'о'):
                    count_sim += 1
                elif line[:-1][i] in pairs.keys() and mes[i] in pairs[line[:-1][i]]:
                    if mes[i] in voiceless:
                        if i != -1 and mes[i + 1] in voice:
                            count_sim += 1
                    elif line[:-1][i] in voiceless:
                        if i != -1 and mes[i + 1] in voice:
                            count_sim += 1
                    elif line[:-1][i] in voice:
                        if i == -1 or line[:-1][i + 1] in voiceless:
                            count_sim += 1
                    elif mes[i] in voice:
                        if i == -1 or mes[i + 1] in voiceless:
                            count_sim += 1
                if count_sim > 3:
                    rhyme_sim.append(line)     
        if rhyme_sim:
            ri = random.randint(0, len(rhyme_sim) - 1)
            bot.send_message(message.chat.id, rhyme_sim[ri])
        else:
            bot.send_message(message.chat.id,
            'Простите, не нашел ни одной строчки Некрасова, которая могла бы хоть как-то отдалено быть рифмоваться с тем, что Вы прислали')
            

bot.polling(none_stop=True)

if __name__ == '__main__':
    bot.polling(none_stop=True)
