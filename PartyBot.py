#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, LinearSVC

PARTY_INTENT = "go_party"

BOT_CONFIG = {
    "intents": {
        "hello": {
            "examples": ["Привет", "Шалом", "Приветики", "Хеллоу", "Привет, друг"],
            "responses": ["Привет, человек", "Оххайо гудзаймас!", "Че как оно"],
        },
        "bye": {
            "examples": [
                "Я не приду",
                "Не смогу сегодня",
                "Сегодня пас",
                "Сори не смогу",
                "Не прийду",
                "Сегодня не смогу",
                "Без меня",
                "Простите, не прийду",
                "на сегодня уже естть планы",
            ],
            "responses": ["Еще увидимся", "Ты чё, пёс!", "Ну и лох", "А жаль:("],
        },
        PARTY_INTENT: {
            "examples": [
                "Кто сегодня в офис",
                "захвати",
                "Сегодня туса",
                "делаем заказ",
                "заказываем в фарфор" "афтерпарти",
                "туса",
                "Сегодня хакатон",
                "хакатон",
                "Заказываем",
                "Заказали",
                "Закажите",
                "Натаныча",
                "Междубулками",
                "Я собираюсь выезжать",
                "Выезжаю",
                "Во сколько движ",
                "движ",
                "афтерпати",
                "заказываем в фарфор",
                "кто собирается",
                "останется на афтерпати",
                "придешь в офис",
                "на тусич",
                "можно подтягиваться",
                "мы в офисе",
                "возьми калик свой",
                "И табак",
                "угли",
                "кальян",
                "калик",
                "хакатонная туса",
                "Откройте",
                "подсветку взял кальянную",
                "кальян будет",
                "калик пакую и буду выезжат до восьми",
                "Купи мне пива",
                "КБ",
                "кому нибудь че нибудь надо захватить?",
                "Идешь сегодня?",
                "курить калик",
                "бухич в офисе",
                "Ждем",
                "На тинькофф",
                "Скидываем на табак",
                "Скидываем за табак",
                "пиццу",
                "бухаем",
                "не забудьте позвонить в охрану",
                "в бар",
                "спик изи",
                "в мечтах",
                "чике пита",
                "филку",
                "сет",
                "филадельфия лайт",
                "калифорния",
                "зоинразмерчик",
                "няняйказавернула",
                "комбо",
                "гавайская",
                "цезарь",
                "сливочный цыпленок",
                "четыре сыра",
                "чикен чиз",
                "мясная",
                "карбонара",
                "том-ям",
                "том ям",
                "техасская резня",
                "хоккайдо",
                "капоэйра",
                "карамельный лосось",
                "локи",
                "биф пита",
                "креветка в деле",
                "лосось в деле",
                "выдвигаемся",
                "биф пита",
                "шаурма",
                "пепперони",
                "темпурный цезарь запеченный",
                "в джаст дэнс",
                "кто придет",
                "Офис",
                "потанцевать джастденс",
                "тусы в офисе",
                "Ещё не закончили ты придешь?",
                "Сколько людей соберется?",
                "Калик курить",
                "Чо за движ пятничный?",
                "Тусим?",
                "Кому чо брать",
                "Возьмите мне сидр какой-нибудь",
                "вино",
                "алкашка",
                "Есть кто в офисе?",
                "Мы в течении часа приедем",
                "Во скок собраться планируете",
                "еду",
                "го парти",
                "уже еду",
                "тусич",
                "бухич",
                "Шо, кто в офисе",
                "кому что купить?",
                "захвати угли",
                "калик подымим",
                "хукатон",
                "приветик, кальян будет?",
                "пиво",
                "пить пиво",
                "бухать пиво",
            ],
            "responses": ["Позвони в охрану, пёс", "Не забудь позвонить в охрану"],
        },
    },
    "failure_phrases": [
        "Все хуйня",
        "Ты пьян, отоспись",
        "Ты на пенек сел, должен был касарь отдать",
    ],
}

X_texts = []  # реплики
y = []  # классы, если класс не подходит не нужно отправлять ответ, не ддосить чат

for intent, intent_data in BOT_CONFIG["intents"].items():
    for example in intent_data["examples"]:
        X_texts.append(example)
        y.append(intent)


# Мы не можем работать с текстом напрямую при использовании алгоритмов машинного обучения
# нужно преобразовать текст в числа
def filter_text(X_texts):
    X_texts = text.lower()
    X_texts = [c for c in text if c in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя- "]


vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
X = vectorizer.fit_transform(X_texts)
print(len(vectorizer.get_feature_names()))


# обучение support vector classifier
clf = LinearSVC().fit(X, y)


clf.predict(vectorizer.transform(["го парти"]))


def get_intent(question):
    question_vector = vectorizer.transform([question])
    intent = clf.predict(question_vector)[0]

    examples = BOT_CONFIG["intents"][intent]["examples"]
    for example in examples:
        dist = nltk.edit_distance(question, example)
        dist_percentage = dist / len(example)
        if dist_percentage < 0.4:
            return intent


def get_answer_by_intent(intent):
    if intent in BOT_CONFIG["intents"]:
        phrases = BOT_CONFIG["intents"][intent]["responses"]
        return random.choice(phrases)


def get_failure_phrase():
    phrases = BOT_CONFIG["failure_phrases"]
    return random.choice(phrases)


def get_answer(question):
    # NLU
    intent = get_intent(question)
    # ищем готовый ответ из конфига
    if intent:
        answer = get_answer_by_intent(intent)
        if answer:
            return answer, intent
