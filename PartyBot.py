

import random
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# In[86]:


BOT_CONFIG = {
    'intents': {
        'hello': {
            'examples': ['Привет', 'Шалом','Приветики','Хеллоу', 'Привет, друг'],
            'responses': ['Привет, человек', 'Оххайо гудзаймас!', 'Че как оно']
        },
        'bye': {
            'examples': ['Я не прийду', 'Не смогу сегодня', 'Сегодня пас', 'Сори не смогу','Не прийду', 'Сегодня не смогу',
                         'Без меня', 'Простите, не прийду', 'на сегодня уже естть планы'],
            'responses': ['Еще увидимся', 'Ты чё, пёс!', 'Ну и лох', 'А жаль:(']
        },
        'go_party': {
            'examples': ['Кто сегодня в офис', 'захвати', 'Сегодня туса','афтерпарти','туса','Сегодня хакатон', 
                         'хакатон', 'Заказываем', 'Заказали', 'Закажите','Натаныча','Междубулками', 'Я собираюсь выезжать',
                         'Выезжаю', 'Во сколько движ', 'движ', 'афтерпати','заказываем в фарфор', 'кто собирается',
                         'останется на афтерпати', 'придешь в офис', 'на тусич', 'можно подтягиваться', 'мы в офисе', 
                         'возьми калик свой', 'И табак', 'угли', 'кальян', 'калик', 'хакатонная туса', 'Откройте', 
                         'подсветку взял кальянную', 'кальян будет','калик пакую и буду выезжат до восьми', 'Купи мне пива', 'КБ',
                         'кому нибудь че нибудь надо захватить?',' Идешь сегодня?', 'курить калик', 'бухич в офисе',
                         'Ждем', 'в джаст дэнс', 'кто придет', 'Офис', 'потанцевать джастденс', 'тусы в офисе', 
                         'Ещё не закончили ты придешь?', 'Сколько людей соберется?', 'Калик курить', 'Чо за движ пятничный?', 
                         'Тусим?', 'Кому чо брать', 'Возьмите мне сидр какой-нибудь', 'вино', 'алкашка', 'Есть кто в офисе?', 
                         'Мы в течении часа приедем', 'Во скок собраться планируете', 'еду', 'го парти', 'уже еду', 'тусич', 'бухич', 
                         'Шо, кто в офисе', 'кому что купить?', 'захвати угли', 'калик подымим', 'хукатон', 'приветик, кальян будет?'],
            'responses': ['Позвони в охрану, пёс', 'Не забудь позвонить в охрану']
        },
    },
    'failure_phrases': [
        'Все хуйня','Ты пьян, отоспись',
        'Ты на пенек сел, должен был касарь отдать',
    ]
}
X_texts = [] # реплики
y = [] # классы, если класс не подходит не нужно отправлять ответ, не ддосить чат

for intent, intent_data in BOT_CONFIG['intents'].items():
    for example in intent_data['examples']:
        X_texts.append(example)
        y.append(intent)


# In[87]:


#Мы не можем работать с текстом напрямую при использовании алгоритмов машинного обучения
#нужно преобразовать текст в числа
def filter_text(X_texts):
    X_texts = text.lower()
    X_texts = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- ']


vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2,4))
X = vectorizer.fit_transform(X_texts)
print(len(vectorizer.get_feature_names()))


# In[88]:


#обучение support vector classifier
clf = LinearSVC().fit(X, y)


# In[89]:


#clf_proba = LinearSVC.fit(X, y)
#clf.score(X, y)


# In[90]:


#тест
clf.predict(vectorizer.transform(['го парти']))


# In[91]:




#def get_intent(question):
#    for intent, intent_data in BOT_CONFIG['intents'].items():
#        for example in intent_data['examples']:
#            filtered_example = filter_text(example)
#            dist = nltk.edit_distance(filtered_example, filter_text(question))
#            if dist / len(filtered_example) < 0.4:
#                    return intent

def get_intent(question):
        question_vector = vectorizer.transform([question])
        intent = clf.predict(question_vector)[0]
        
        examples = BOT_CONFIG['intents'][intent]['examples']
        for example in examples:
            dist = nltk.edit_distance(question, example)
            dist_percentage = dist / len(example)
            if dist_percentage < 0.4:
                return intent
            
get_intent('хуйня')
print(intent)


# In[92]:


def get_answer_by_intent(intent):
    if intent in BOT_CONFIG['intents']:
        phrases = BOT_CONFIG['intents'][intent]['responses']
        return random.choice(phrases)
    


# In[93]:


def get_failure_phrase():
    phrases = BOT_CONFIG['failure_phrases']
    return random.choice(phrases)


# In[94]:


def bot(question):
    # NLU
    intent = get_intent(question)
    # ищем готовый ответ из конфига
    if intent:
        answer = get_answer_by_intent(intent)
        if answer:
            return answer
#    answer = get_failure_phrase()
#    return answer


# In[95]:


print(bot('приветик, кальян будет?'))


# In[ ]:





# In[57]:


question = None
while question not in ['']:
    question = input()
    answer = bot(question)
    print(answer)



from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Функция будет вызвана при получении сообщения
def botMessage(update: Update, context: CallbackContext):
    answer = bot(update.message.text) # # Готовим ответ
    print(update.message.text, answer, get_intent(update.message.text))
    update.message.reply_text(answer) # Отправляем ответ обратно пользователю

    
#def main():
    
updater = Updater("5200811696:AAFRC17wCt9rJDepba4hGMOWkY8RLGGQoX0", use_context=True)

# Конфигурацию, при получении любого текстового сообщения будет вызвана функция botMessage
updater.dispatcher.add_handler(MessageHandler(Filters.text, botMessage))

updater.start_polling()
updater.idle()
