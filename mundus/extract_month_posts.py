import argparse
import os
import pandas as pd

import sys
sys.path.append(os.path.dirname(__file__))
from utils import get_data_dir

GAME_TYPES = ['Total War', 'Grande Stratégie', 'Gestion', 'STR']

def get_args():
    parser = argparse.ArgumentParser(description='Extract posts of a month to help to write the Diarium Strategorum.')
    parser.add_argument('csv', type=str, help='Relative data path (.csv)')
    parser.add_argument('month', type=str, help='Month of the extraction in YYYY-MM format')
    return parser.parse_args()

def game_type_to_bbcode(game_type: str, data: pd.DataFrame):
    """
    Export in a string the BBcode of the dataframe with games sorted alphabetically
    """
    res = f'[b]{game_type}[/b]\n'
    for game in sorted(data['game'].unique()):
        res += game_post_to_bbcode(game, data[data['game'] == game])
    return res

def game_post_to_bbcode(game: str, posts: pd.DataFrame):
    """
    Export in a string the BBcode of the dataframe of the posts of a game
    """
    res = f'[b]{game}[/b]\n'
    res += '[list]\n'
    for i in reversed(range(len(posts))):
        post = posts.iloc[i]
        res += f'[*] [url={post["url"]}]{post["title"]}[/url]\n'
    res += '[/list]\n\n'
    return res


def main(args):
    relative_csv_path = args.csv
    csv_path = os.path.join(get_data_dir(), relative_csv_path)
    print(f'Read the file {csv_path}')
    data = pd.read_csv(csv_path, sep=';')
    data['game'].fillna('', inplace=True)
    data['game_type'].fillna('', inplace=True)
    month_data = data[data['date'] >= f'{args.month}-01']
    res = ''
    for game_type in GAME_TYPES:
        res += game_type_to_bbcode(game_type.upper(), month_data[month_data['game_type'] == game_type])
    res += game_type_to_bbcode('DIVERS', month_data[~month_data['game_type'].isin(GAME_TYPES)])
    output_file = f'Diarium_Strategorum_{args.month}.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(res)
    print(f'{output_file} written')

if __name__ == "__main__":
    # execute only if run as a script
    args = get_args()
    main(args)
