from requests import get, post, delete
from server import PORT

# Для пользователей
print('Users')
print('Correct')
print(get(f'http://localhost:{PORT}/api/users').json())
print(post(f'http://localhost:{PORT}/api/users',
           json={'email': 'mail@mail.ru',
                 'name': 'Ivan',
                 'surname': 'Ivanov',
                 'password': '123',
                 'password_again': '123',
                 'age': 23,
                 'about': 'My name is Ivan'}).json())
print(get(f'http://localhost:{PORT}/api/users/1').json())
print(delete(f'http://localhost:{PORT}/api/users/1').json())

print('Incorrect')
print(post(f'http://localhost:{PORT}/api/users').json())
print(post(f'http://localhost:{PORT}/api/users',
           json={'email': 'mail@mail.ru'}).json())
print(post(f'http://localhost:{PORT}/api/users',
           json={'name': 'Sasha'}).json())
print(get(f'http://localhost:{PORT}/api/users/999').json())
print(delete(f'http://localhost:{PORT}/api/users/999').json())


# Для задач
print('Tasks')
print('Correct')
print(get(f'http://localhost:{PORT}/api/tasks').json())
print(post(f'http://localhost:{PORT}/api/tasks',
           json={'name': 'Read book',
                 'about': 'Read book at the morning',
                 'is_finished': False,
                 'author': 'name@mail.ru',
                 'create_date': '2020.04.20'}).json())
print(get(f'http://localhost:{PORT}/api/tasks/1').json())
print(delete(f'http://localhost:{PORT}/api/tasks/1').json())

print('Incorrect')
print(post(f'http://localhost:{PORT}/api/tasks').json())
print(post(f'http://localhost:{PORT}/api/tasks',
           json={'name': 'Read book'}).json())
print(post(f'http://localhost:{PORT}/api/tasks',
           json={'about': 'Read book at the morning'}).json())
print(get(f'http://localhost:{PORT}/api/tasks/999').json())
print(delete(f'http://localhost:{PORT}/api/tasks/999').json())


# Для целей
print('Aims')
print('Correct')
print(get(f'http://localhost:{PORT}/api/aims').json())
print(post(f'http://localhost:{PORT}/api/aims',
           json={'name': 'Sit on quarantine',
                 'about': 'Stay at home!',
                 'is_finished': False,
                 'finish_date': '2020.05.01',
                 'author': 'name@mail.ru'}).json())
print(get(f'http://localhost:{PORT}/api/aims/1').json())
print(delete(f'http://localhost:{PORT}/api/aims/1').json())

print('Incorrect')
print(post(f'http://localhost:{PORT}/api/aims').json())
print(post(f'http://localhost:{PORT}/api/aims',
           json={'name': 'Sit on quarantine'}).json())
print(post(f'http://localhost:{PORT}/api/aims',
           json={'finish_date': '2020.05.01'}).json())
print(post(f'http://localhost:{PORT}/api/aims',
           json={'name': 'Sit on quarantine',
                 'about': 'Stay at home!',
                 'is_finished': 'False',
                 'finish_date': '2020.05.01'}).json())
print(get(f'http://localhost:{PORT}/api/aims/999').json())
print(delete(f'http://localhost:{PORT}/api/aims/999').json())


# Для привычек
print('Habits')
print('Correct')
print(get(f'http://localhost:{PORT}/api/habits').json())
print(post(f'http://localhost:{PORT}/api/habits',
           json={'name': 'Read book every day',
                 'author': 'name@mail.ru',
                 'day1': False,
                 'day2': False,
                 'day3': False,
                 'day4': False,
                 'day5': False,
                 'day6': False,
                 'day7': False}).json())
print(get(f'http://localhost:{PORT}/api/habits/1').json())
print(delete(f'http://localhost:{PORT}/api/habits/1').json())

print('Incorrect')
print(post(f'http://localhost:{PORT}/api/habits').json())
print(get(f'http://localhost:{PORT}/api/habits/999').json())
print(delete(f'http://localhost:{PORT}/api/habits/999').json())


# Для записей
print('Blogs')
print('Correct')
print(get(f'http://localhost:{PORT}/api/blogs').json())
print(post(f'http://localhost:{PORT}/api/blogs',
           json={'name': 'My project',
                 'about': 'I did my project',
                 'author': 'name@mail.ru'}).json())
print(get(f'http://localhost:{PORT}/api/blogs/1').json())
print(delete(f'http://localhost:{PORT}/api/blogs/1').json())

print('Incorrect')
print(post(f'http://localhost:{PORT}/api/blogs').json())
print(post(f'http://localhost:{PORT}/api/blogs',
           json={'about': 'I did my project'}).json())
print(get(f'http://localhost:{PORT}/api/blogs/999').json())
print(delete(f'http://localhost:{PORT}/api/blogs/999').json())