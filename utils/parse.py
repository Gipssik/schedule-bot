import asyncio
import json
import logging

import requests

from bs4 import BeautifulSoup

from data.config import schedule_data_name, group_names_name


async def groups_list_forming(soup):
    groups_list = soup.find_all('a', class_='collection-item')
    for i, v in enumerate(groups_list):
        groups_list[i] = v.text.upper()
    return groups_list


async def group_schedule_dict_forming(groups_list, url, headers):
    async def dict_operating(blocks, local_schedule):
        for block in blocks:
            # Собираем название предметов
            subj = block.find_all('div', class_='subject')
            # room = block.find('span', class_='room').text.strip()
            rooms = [room.text.strip() for room in block.find_all('span', class_='room')]
            class_type = block.find('span', class_='room').find_parent().text.split(',')[0]
            # Если есть раздел на подгруппы, то делаем элемент с рассчетом на них
            try:
                groups = block.find('div', class_='subgroups').find_all('div', class_='one')
                g = []  # Список с цифрами подгрупп
                for group in groups:
                    try:
                        g.append(group.find('div').text[-2:-1])  # Вырезаем номер подгруппы из строки
                    except AttributeError:
                        continue  # если нету пар в подгруппе
            # Если нету, то создаем элемент только с временем и названием предмета
            except AttributeError:
                for s in subj:
                    t = s.find_parent('tr').find('th').text  # находим время
                    local_schedule[block.find_parent('td').get('day')].append((t, s.text, rooms[0], class_type))
                continue
            else:
                for index, s in enumerate(subj):
                    t = s.find_parent('tr').find('th').text
                    local_schedule[block.find_parent('td').get('day')].append((t, s.text, g[index], rooms[index], class_type))

        return local_schedule

    group_schedule_dict = {}
    for group in groups_list:
        group_url = url + f'schedule/group/{group}/'
        req = requests.get(group_url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')

        if 'Сторінку не з' in soup.find('h1').text:
            logging.error(f'Error 404: page "{group}" not found')
            continue

        tables = soup.find_all('table', class_='schedule')
        schedule = {}
        trs = []
        for table in tables:
            trs.append(table.find('tr').find_next_sibling())
        tds = []
        for tr in trs:
            tds.append(tr.find_all('td'))
        for td in tds:
            for day in td:
                schedule[day.get('day')] = []

        blocks = soup.find_all('div', class_='variative')
        schedule = await dict_operating(blocks, schedule)
        group_schedule_dict[group] = schedule

    return group_schedule_dict


async def parse():
    url = 'https://rozklad.ztu.edu.ua/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    try:
        if 'Сторінку не з' in soup.find('h1').text:
            logging.error('Error 404 while parsing')
            return
    except AttributeError:
        pass

    groups_list = await groups_list_forming(soup)
    group_schedule_dict = await group_schedule_dict_forming(groups_list, url, headers)
    with open(schedule_data_name, "w") as json_file:
        json.dump(group_schedule_dict, json_file, indent=4)
    with open(group_names_name, "w") as txt_file:
        txt_file.writelines(','.join(group_schedule_dict.keys()))
