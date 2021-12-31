import pandas as pd
import os
import argparse


GAMES = ['Age of Empires III : Definitive Edition', 'Age of Empires II', 'Age of Empires IV', 'Ancient Cities', 'Ancient Worlds : Egypt',
         'Builder Simulator', 'Builders of China', 'Builders of Egypt',
         'Chernobyl Liquidators Simulator', 'Chinese City Constructor ', 'Crusader Kings 3',
         'Crusader Kings III', 'Decisive Campaigns : Ardennes Offensive', 'Distant Kingdoms',
         'El Dorado: The Golden City Builder', 'Empire : Total War', 'Europa Universalis IV', 'Espresso Tycoon',
         'Field of Glory II : Medieval', 'Fields of History: The Great War', 'Going Medieval',
         'Hearts of Iron', 'HOI4', 'Hegemony III', 'Hellish Quart', 'Hellish quart', 'Humankind', 'Imperator : Rome', 'Knights of Honor 2',
         'La Porte des Fauconniers', 'Medieval II - Total War', 'Medieval II : Total War', 'Monuments Flipper', 'Mount & Blade II',
         'Nebuchadnezzar', 'Patron', 'Pharaoh : A New Era', 'Pizza Simulator', 'Project Wunderwaffe', 'Rome : Total War', 'Stadium Renovator', 'Stellaris', 'Sumerians',
         'Supermarket Manager', 'The Troop', 'Three Kingdoms', 'Timberborn', 'Total War : Troy', 'Total War : Warhammer',
         'Total War : WARHAMMER', 'Troy : Total War', 'Victoria 3', 'Victoria III ', 'Viking City Builder', 'Wargame Red Dragon']

GAME_MAPPING = {'Crusader Kings III': 'Crusader Kings 3', 'Hearts of Iron': 'Hearts of Iron IV', 'Hellish Quart': 'Hellish quart', 'HOI4': 'Hearts of Iron IV',
                'Mount & Blade II': 'Mount & Blade II : Bannerlord', 'Three Kingdoms': 'Total War : Three Kingdoms',
                'Total War : Warhammer': 'Total War : Warhammer II', 'Total War : WARHAMMER': 'Total War : Warhammer II',
                'Medieval II - Total War': 'Medieval II : Total War', 'Total War : Troy': 'Troy : Total War', 'Victoria III': 'Victoria 3'}

def get_args():
    parser = argparse.ArgumentParser(description='Convert JSON result to CSV and try inferring games')
    parser.add_argument('json', type=str, help='Relative data path (.json)')
    return parser.parse_args()


def get_data_dir():
    if 'data' in os.listdir('.'):
        return 'data'
    return os.path.join('..', 'data')


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
    if game in ['Ancient Cities', 'Ancient Worlds : Egypt', 'Builder Simulator',
                'Builders of China', 'Builders of Egypt', 'Chernobyl Liquidators Simulator', 'Chinese City Constructor ', 'Distant Kingdoms',
                'El Dorado: The Golden City Builder', 'Espresso Tycoon', 'Going Medieval',
                'Monuments Flipper', 'Nebuchadnezzar', 'Patron', 'Pharaoh : A New Era', 'Pizza Simulator', 'Project Wunderwaffe',
                'Stadium Renovator', 'Sumerians', 'Supermarket Manager', 'Timberborn', 'Viking City Builder']:
        return 'Gestion'
    if game in ['Crusader Kings 3', 'Europa Universalis IV', 'Fields of History: The Great War', 'Hearts of Iron IV',
                'Imperator : Rome', 'Stellaris', 'Victoria 3']:
        return 'Grande Stratégie'
    if game in ['Hellish quart', 'La Porte des Fauconniers', 'Mount & Blade II : Bannerlord']:
        return 'RPG'
    if game in ['Humankind']:
        return '4X'
    if game in ['Age of Empires II', 'Age of Empires III : Definitive Edition', 'Age of Empires IV', 'Hegemony III', 'Knights of Honor 2', 'Wargame Red Dragon']:
        return 'STR'
    if 'Total' in game:
        return 'Total War'
    if game in ['Decisive Campaigns : Ardennes Offensive', 'Field of Glory II : Medieval', 'The Troop']:
        return 'Stratégie Tour par Tour'
    return None


def main(args):
    relative_json_path = args.json
    json_path = os.path.join(get_data_dir(), relative_json_path)
    print(f'Read the file {json_path}')
    data = pd.read_json(json_path, encoding='utf-8', keep_default_dates=False)
    data['date'] = pd.to_datetime(data['date'], dayfirst=True)
    if os.path.exists(os.path.join(get_data_dir(), 'url_to_game.csv')):
        df = pd.read_csv(os.path.join(get_data_dir(), 'url_to_game.csv'), encoding='ISO-8859-1')
        url_to_game = df[['url', 'game']].set_index('url').to_dict()['game']
        data['game'] = data['url'].apply(lambda url: url_to_game[url] if url in url_to_game else None)
    else:
        data['game'] = data['title'].apply(extract_game)
    data['game_type'] = data['game'].apply(add_game_category)
    data.to_csv(f'{json_path[:-5]}.csv', index=None, sep=';')
    print(f'{json_path[:-5]}.csv written')



if __name__ == "__main__":
    # execute only if run as a script
    args = get_args()
    main(args)
