import asyncio
import time
import logging
import aiohttp

from bs4 import BeautifulSoup

from data.config import Config


async def groups_list_forming(soup):
    groups_list = soup.find_all('a', class_='collection-item')
    for i, v in enumerate(groups_list):
        groups_list[i] = v.text.upper()
    return groups_list


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


async def get_group_data(session, url, headers, group_name):
    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')

        if 'Сторінку не з' in soup.find('h1').text:
            return

        tables = soup.find_all('table', class_='schedule')

        trs = [table.find('tr').find_next_sibling() for table in tables]
        tds = [tr.find_all('td') for tr in trs]
        schedule = {day.get('day'):[] for td in tds for day in td}

        blocks = soup.find_all('div', class_='variative')
        schedule = await dict_operating(blocks, schedule)
        Config.get_schedule_data()[group_name] = schedule


async def gather_data():
    url = 'https://rozklad.ztu.edu.ua/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')

        try:
            if 'Сторінку не з' in soup.find('h1').text:
                logging.error('Error 404 while parsing')
                return
        except AttributeError:
            pass

        groups_list = await groups_list_forming(soup)

        tasks = []

        for group in groups_list:
            task = asyncio.create_task(get_group_data(session, url + f'schedule/group/{group}/', headers, group))
            tasks.append(task)

        await asyncio.gather(*tasks)


async def parse():
    print('Starting parsing...')
    start = time.time()
    await gather_data()
    Config.set_group_names(list(Config.get_schedule_data().keys()))
    print(f'Ended in: {time.time() - start}')
