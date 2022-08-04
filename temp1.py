from bs4 import BeautifulSoup
import requests
import csv
import lxml

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
candidate_level = [39, 40, 41]
candidate_status = ['GRADUATED', 'INTERNSHIP_IN_PROGRESS', 'INTERNSHIP_COMPLETED', 'RESUME_COMPLETED', 'LOOKING_FOR_JOB', 'HAVE_JOB']

link_list = []
main_dict = {}
main_link_list =[]

#Cоздаем комбинации первоначальных страниц
for i in candidate_level:
    for n in candidate_status:
        link_list.append(f'https://javarush.ru/users?level={i}&status={n}')

print(f'Основные URL собраны. Получено {len(link_list)} страниц')
print()

#Удаляем пустые страницы, которые дают баги.
link_list.pop(3)
link_list.pop(14)

print('Пустые URL удалены. Начинаю пагинацию..')
print()

#Пагинация. Комбинируем список всех страниц для парсинга.
for link in link_list:
    for k in range(1, 3):
        line = link + f'&page={k}'
        if requests.get(line).status_code == 200:
            main_link_list.append(line)
            print(line)
        else:
            break

print(f'Пагинация страниц закончена. Собрано {len(main_link_list)} URL')
print('Начинаю парсинг')
print()

k = 1

#Цикл сбора данных с каждой страницы.
for site_url in main_link_list:
    r = requests.get(site_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml').find('div', class_='feed__content ng-star-inserted')

    list_users_links = []
    list_users_name = []

    for link in soup.find_all('a'):
        list_users_links.append('https://javarush.ru' + str(link.get('href')))

    for i in soup.find_all('div', class_='user-card__name'):
        list_users_name.append(i.get_text())

    dic = {}

    for j in range(0, len(list_users_name)):
        dic[list_users_name[j]] = list_users_links[j]

    main_dict.update(dic)

    print(f'Спарсено {k} \ {len(main_link_list)} страниц..  Получено + {len(dic)} новых записей. Всего записей получено: {len(main_dict)}')
    k += 1


print()

for key,value in main_dict.items():
    print(key, ':', value)

print()
print(f'Парсинг закончен. Получено {len(main_dict)} значений. Начинаю запись в CSV')
print()

with open('JRSpider.csv', 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in main_dict.items():
        writer.writerow([key, value])

print('Запись данных закончена')