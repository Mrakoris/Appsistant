import hashlib
import os
import openai

openai.api_key = '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'

messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

def check_topic_filter(message):
    allowed_topics = ["рф", "Законодательство", "Закон", "РФ", "Российская федерация", "законодательство",]
    if any(topic in message for topic in allowed_topics):
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        print(f"ChatGPT: {reply}")
        messages.append({"role": "assistant", "content": reply})
    else:
        print("Извините, это не входит в компетенцию")

def check_topic_filter(message_2):
    allowed_topics = ["РФ", "рф", "льготы", "сфера", "сферы", "бизнес", "бизнеса","Хлеб"]
    if any(topic in message_2 for topic in allowed_topics):
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        print(f"ChatGPT: {reply}")
        messages.append({"role": "assistant", "content": reply})
    else:
        print("Извините, это не входит в компетенцию")

file_name = "user_actions.txt"

NAME = "Register"
def init_file():
    if not os.path.exists('Users.txt'):
        with open('Users.txt', 'w'):
            pass


def add_user(login: str, password: str) -> bool:

    with open('Users.txt', 'r') as f:
        users = f.read().splitlines()

    for user in users:
        args = user.split(':')
        if login == args[0]:
            return False

    with open('Users.txt', 'a') as f:
        f.write(f'{login}:{password}\n')
    return True


def get_user(login: str, password: str) -> bool:
    with open('Users.txt', 'r') as f:
        users = f.read().splitlines()

    for user in users:
        args = user.split(':')
        if login == args[0] and password == args[1]:
            return True
    return False


def main_loop(login: str):
    print(f'Привет, {login}!')


init_file()

while True:
    print('''Добро пожаловать! Выберите пункт меню:
    1. Вход
    2. Регистрация
    3. Выход''')

    user_input = input()
    if user_input == '1':
        print('Введите логин:')
        login = input()

        print('Введите пароль:')
        password = input()

        result = get_user(login, hashlib.sha256(password.encode()).hexdigest())

        if result:
            print('Вы вошли в систему\n')
            with open ('user_actions.txt', "a") as file:
                while True:
                    print('Выберите, что вы хотите:\n' +
                      '1. Получение информации по действующему законодательству РФ (не более 3-х запросов в минуту),\n' +
                      '2. Получение информации по доступным в России льготам для определенных категорий бизнеса (не более 3-х запросов в минуту)')
                    user_input = input()

                    if user_input == '1':
                        while True:
                            message = input(f"{login}: ")
                            if message:
                                file.write(f"{login}: {message}\n")
                                messages.append({"role": "user", "content": message})
                                check_topic_filter(message)
                    elif user_input == '2':
                        while True:
                            message_2 = input(f"{login}: ")
                            if message_2:
                                file.write(f"{login}: {message_2}\n")
                                messages.append({"role": "user", "content": message_2})
                                check_topic_filter(message_2)
                else:
                    print('Неверный логин или пароль')

    elif user_input == '2':
        print('Введите логин:')
        login = input()

        print('Введите пароль:')
        password = input()

        print('Повторите пароль:')
        password_repeat = input()

        if password != password_repeat:
            print('Пароли не совпадают!')
            continue

        result = add_user(login, hashlib.sha256(
            password.encode()).hexdigest())  # Вызываем функцию добавления пользователя. И хешируем пароль(безопасность)

        if not result:
            print('Пользователь с таким логином уже существует')
        else:
            print('Регистрация прошла успешно!')

    elif user_input == '3':
        print('Завершение работы')
        break  # Выходим из цикла