#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import LogisticRegression


# In[2]:


BOT_CONFIG = {
    'intents': {
        'hello': {
            'examples': ['Привет', 'Шалом','Приветики','Хеллоу'],
            'responses': ['Привет, человек', 'Оххайо гудзаймас!', 'Че как оно']
        },
        'bye': {
            'examples': ['Я не прийду', 'Не смогу сегодня', 'Сегодня пас', 'Сори не смогу'],
            'responses': ['Еще увидимся', 'Ты чё, пес!', 'Ну и лох', 'А жаль:(']
        },
        'go_party': {
            'examples': ['Кто сегодня в офис', 'Сегодня туса','Сегодня хакатон', 'Заказываем', 'Заказали', 'Закажите','Натаныча','Междубулками', 'Я собираюсь выезжать', 'Выезжаю', 'Во сколько движ', 'движ', 'афтерпати','заказываем в фарфор', 'кто собирается', 'останется на афтерпати', 'придешь в офис', 'на тусич', 'можно подтягиваться', 'мы в офисе', 'возьми калик свой', 'И табак', 'угли', 'кальян', 'хакатонная туса', 'Откройте',  'подсветку взял кальянную', 'калик пакую и буду выезжат до восьми', 'должен приехать', 'приеду', 'Купи мне пива', 'Я пошёл в КБ', 'кому нибудь че нибудь надо захватить?',' Идешь сегодня?', 'курить калик', 'бухич в офисе', 'Ждем', 'в джаст дэнс', 'кто придет', 'Офис', 'потанцевать джастденс', 'тусы в офисе', 'Ещё не закончили ты придешь?', 'Сколько людей соберется?', 'Калик курить', 'Чо за движ пятничный?', 'Тусим?', 'Кому чо брать', 'Возьмите мне сидр какой-нибудь', 'вино', 'алкашка', 'Есть кто в офисе?', 'Мы в течении часа приедем', 'Во скок собраться планируете', 'еду', 'уже еду', 'тусич', 'бухич', 'Шо, кто в офисе'],
            'responses': ['Позвони в охрану, пёс', 'Не забудь позвонить в охрану']
        },
    },
    'failure_phrases': [
        'Все хуйня','Ты пьян, отоспись',
        'Ты на пенек сел, должен был касарь отдать',
    ]
}
X_texts = [] # реплики
y = [] # классы, если класс не подходит нужно не отправлять ответ, не ддосить чат

for intent, intent_data in BOT_CONFIG['intents'].items():
    for example in intent_data['examples']:
        X_texts.append(example)
        y.append(intent)

        
vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2,4))
X = vectorizer.fit_transform(X_texts)
clf = LinearSVC().fit(X,y)
clf_proba = SVC(probability = True).fit(X,y)


# In[3]:


def get_intent(question):
        question_vector = vectorizer.transform([question])
        intent = clf.predict(question_vector)[0]
        
        examples = BOT_CONFIG['intents'][intent]['examples']
        for example in examples:
            dist = nltk.edit_distance(question, example)
            dist_percentage = dist / len(example)
            if dist_percentage < 0.2:
                return intent
        #index = list(clf_proba.classes_).index(intent)
        #proba = clf_proba.predict_proba(question_vector)[0][index]
        #print(intent, proba)
        #if proba > 0.20: # если класс не подходит нужно не отправлять ответ, не ддосить чат
            #return intent
get_intent('Выехал')


# In[4]:


def qet_answer_by_intent(intent):
    if intent in BOT_CONFIG['intents']:
        phrases = BOT_CONFIG['intents'][intent]['responses']
        return random.choise(phrases)
    


# In[5]:


#def filter_text(text):
    #text = text.lower()
    #text = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- ']
    #text = ''.join(text)
   # return text


# In[6]:


def get_failure_phrase():
    phrases = BOT_CONFIG['failure_phrases']
    return random.choice(phrases)


# In[7]:


#def get_intent(question):
   # for intent, intent_data in BOT_CONFIG['intents'].items():
   #     for example in intent_data['examples']:
   #         filtered_example = filter_text(example)
   #         dist = nltk.edit_distance(filtered_example, filter_text(question))
   #         if dist / len(filtered_example) < 0.4:
   #                 return intent


# In[8]:


def bot(question):
    # NLU
    intent = get_intent(question)
    # ищем готовый ответ из конфига
    if intent:
        answer = get_answer_by_intent(intent)
        if answer:
            return answer
    # Генерируем ответ по контексту из файла
    answer = generate_answer_by_text(question)
    if answer:
        return answer

#answer = get_failure_phrase()
#return answer


# In[9]:


question = None
while question not in ['']:
    question = input()
    answer = bot(question)
    print(answer)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




