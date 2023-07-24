'''

Termidex
--------

Look up gen 1 Pokémon by name or number from a
Terminal app

Created 2023 by Andrew Lawler

'''


import argparse
import json
import time

from math import ceil, floor
from random import randint

from rich import print
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn
)
from rich.table import Column

from pokemon import Pokemon
from statistics import props, type_colors


class Pokedex(object):
    def __init__(self):
        self.filepath = 'gen1_dex.json'

        self.load_pokemon()
        self.set_current_pokemon(1)
        self.setup_stat_panel()

    def animate(self):
        for task in self.stat_bar.tasks:
            current = task.completed
            goal = int(task.fields['fields']['target'])
            if current < goal:
                value = ceil((goal - current) / 35)
                self.stat_bar.update(task.id, advance=value)
            elif not task.fields['fields']['complete']:
                task.fields['fields']['complete'] = True

    def get_number_from_name(self, name: str) -> int | None:
        try:
            pokemon = [p.number for p in self.dex if p.name == name.title()]
            return pokemon[0]
        except IndexError:
            return None

    def load_pokemon(self):
        self.dex = []

        with open(self.filepath) as f:
            self.dex = [Pokemon(obj) for obj in json.load(f)]

    def render(self):
        pok = self.current_pokemon
        name = pok.name.upper().ljust(10)

        color1 = type_colors[pok.types[0].lower()]
        if len(pok.types) == 2:
            color2 = type_colors[pok.types[1].lower()]
            type_display = f'[{color1}]{pok.types[0]}[/{color1}]' \
                           f' / [{color2}]{pok.types[1]}[/{color2}]'
        else:
            type_display = f'[{color1}]{pok.types[0]}[/{color1}]'

        self.stat_bar.add_task(
            name='HP',
            description=f'[light_goldenrod2]{pok.hp}[/light_goldenrod2]',
            total=next(p.max_value for p in props if p.abbr == 'HP'),
            fields={'info': '', 'target': pok.hp, 'complete': False})

        self.stat_bar.add_task(
            name='ATK',
            description=f'[light_goldenrod2]{pok.attack}[/light_goldenrod2]',
            total=next(p.max_value for p in props if p.abbr == 'ATK'),
            fields={
                'info': f'No {int(pok.number):03d} [grey54]{name}[/grey54]',
                'target': pok.attack,
                'complete': False
            }
        )

        self.stat_bar.add_task(
            name='DEF',
            description=f'[light_goldenrod2]{pok.defense}[/light_goldenrod2]',
            total=next(p.max_value for p in props if p.abbr == 'DEF'),
            fields={'info': '', 'target': pok.defense,
                    'complete': False})

        self.stat_bar.add_task(
            name='Sp. ATK',
            description=f'[light_goldenrod2]{pok.sp_attack}' \
                         '[/light_goldenrod2]',
            total=next(p.max_value for p in props if p.abbr == 'Sp. ATK'),
            fields={
                'info': f'  Type: {type_display}',
                'target': pok.sp_attack,
                'complete': False})

        self.stat_bar.add_task(
            name='Sp. DEF',
            description=f'[light_goldenrod2]{pok.sp_defense}' \
                         '[/light_goldenrod2]',
            total=next(p.max_value for p in props if p.abbr == 'Sp. DEF'),
            fields={
                'info': f'  Seen: [light_goldenrod2]{pok.seen}' \
                         '[/light_goldenrod2]',
                'target': pok.sp_defense,
                'complete': False
            }
        )

        self.stat_bar.add_task(
            name='SPD',
            description=f'[light_goldenrod2]{pok.speed}[/light_goldenrod2]',
            total=next(p.max_value for p in props if p.abbr == 'SPD'),
            fields={
                'info': f' Owned: [light_goldenrod2]{pok.owned}' \
                         '[/light_goldenrod2]',
                'target': pok.speed,
                'complete': False
            }
        )

        while not all(t.fields['fields']['complete'] \
                for t in self.stat_bar.tasks):
            self.animate()
            time.sleep(0.01)

    def set_current_pokemon(self, n: str | int):
        self.current_pokemon = next(p for p in self.dex if p.number == int(n))

    def setup_stat_panel(self):
        '''
        Set BarColumn finished_style to 'bar.complete'
        to prevent it from changing colors when a
        Pokémon is maxed out in some stat.
        '''
        self.stat_bar = Progress(
            TextColumn(
                '{task.fields[fields][info]}',
                table_column=Column(ratio=4)
            ),
            TextColumn(
                '{task.fields[name]}: ',
                table_column=Column(ratio=2),
                justify='right'
            ),
            TextColumn('{task.description}', table_column=Column(ratio=1)),
            BarColumn(
                bar_width=None,
                finished_style='bar.complete',
                table_column=Column(ratio=5)
            ),
            expand=True
        )

        self.stat_panel = Panel(
            self.stat_bar,
            width=80,
            title='[orange1]Pokédex[/orange1]',
            style='grey39 on grey11',
            border_style='blue'
        )


def as_ratio_to_max(value: float, max_value: int) -> int:
    return floor((int(value) / max_value) * 100)


def get_args(dex: Pokedex) -> dict | None:
    parser = argparse.ArgumentParser(
        prog='Pokédex',
        description='Gen 1 Pokédex terminal application')
    parser.add_argument('-l', '--lookup', default=0)
    parser.add_argument('-r', '--random', action='store_true')

    args = parser.parse_args()

    if args.lookup:
        number = try_parse_int(args.lookup)
        if number is None:
            number = dex.get_number_from_name(args.lookup)
            if number is None:
                print('Could not find a Pokémon called ' \
                     f'[orange1]{args.lookup}[/orange1].\n' \
                     '(Is this a gen [white]1[/white] Pokémon?)')
                return
        elif number < 1 or number > 151:
            print('This Pokédex only contains gen [white]1[/white] Pokémon (numbers 1-151)')
            return

    if bool(args.lookup) ^ args.random:
        return {
            'command': 'lookup',
            'number': number if args.lookup else randint(1, 151)
        }
    else:
        print('Use "--lookup" or "-l" to look up an entry in the Pokédex:')
        print('   >>> python /path/to/dex.py -l 58')
        print('   >>> python /path/to/dex.py -l growlithe')
        print(
            '[orange1]Or[/orange1] try "--random" / "-r" for a random entry')


def try_parse_int(n: str):
    try:
        return int(n)
    except ValueError:
        return None


def main():
    dex = Pokedex()

    # command = {'command': 'lookup', 'number': 149}
    command = get_args(dex)
    while command:
        with Live(dex.stat_panel, refresh_per_second=20):
            dex.set_current_pokemon(command['number'])
            dex.render()
            command = None


if __name__ == '__main__':
    main()
