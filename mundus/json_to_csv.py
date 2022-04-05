import datetime
import pandas as pd
import os
import argparse

import sys
sys.path.append(os.path.dirname(__file__))
from constants import GAME_MAPPING, GAMES, GESTION, GRANDE_STATEGIE, RPG, STR, STRATEGIE_TOUR_PAR_TOUR
from utils import get_data_dir


def get_args():
    parser = argparse.ArgumentParser(description='Convert JSON result to CSV and try inferring games')
    parser.add_argument('json', type=str, help='Relative data path (.json)')
    return parser.parse_args()


def extract_game(title: str):
    for game in GAMES:
        if game in title:
            if game in GAME_MAPPING:
                return GAME_MAPPING[game]
            else:
                return game
    return ''


def add_game_category(game: str):
    if pd.isnull(game):
        return None
    if game in GESTION:
        return 'Gestion'
    if game in GRANDE_STATEGIE:
        return 'Grande Stratégie'
    if game in RPG:
        return 'RPG'
    if game in ['Humankind']:
        return '4X'
    if game in STR:
        return 'STR'
    if 'Total' in game:
        return 'Total War'
    if game in STRATEGIE_TOUR_PAR_TOUR:
        return 'Stratégie Tour par Tour'
    return None


def main(args):
    relative_json_path = args.json
    json_path = os.path.join(get_data_dir(), relative_json_path)
    print(f'Read the file {json_path}')
    data = pd.read_json(json_path, encoding='utf-8', keep_default_dates=False)
    today_datetime = datetime.datetime.now()
    yesterday_str = (today_datetime + datetime.timedelta(days=-1)).strftime('%d-%m-%Y')
    today_str = today_datetime.strftime('%d-%m-%Y')
    data['date'] = data['date'].apply(lambda date: date.replace('Hier', yesterday_str))
    data['date'] = data['date'].apply(lambda date: date.replace('Aujourd\'hui', today_str))
    data['date'] = pd.to_datetime(data['date'], dayfirst=True)
    if os.path.exists(os.path.join(get_data_dir(), 'url_to_game.csv')):
        df = pd.read_csv(os.path.join(get_data_dir(), 'url_to_game.csv'), encoding='ISO-8859-1')
        url_to_game = df[['url', 'game']].set_index('url').to_dict()['game']
        data['game'] = data['url'].apply(lambda url: url_to_game[url] if url in url_to_game else None)
    else:
        data['game'] = data['title'].apply(extract_game)
    data['game_type'] = data['game'].apply(add_game_category)
    data.to_csv(f'{json_path[:-5]}.csv', index=None, sep=';', encoding='utf-8')
    print(f'{json_path[:-5]}.csv written')



if __name__ == "__main__":
    # execute only if run as a script
    args = get_args()
    main(args)
