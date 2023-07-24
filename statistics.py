class Property(object):
    def __init__(self, name: str):
        self.name = name
        self.abbr = None
        self.is_stat = False
        self.value = None


class Stat(Property):
    def __init__(self, name: str, abbr: str, max_value: int=200):
        self.name = name
        self.abbr = abbr
        self.max_value = max_value
        self.is_stat = True
        self.value = None


props = [
    Property('number'),
    Property('name'),
    Property('seen'),
    Property('owned'),
    Stat('hp', 'HP', 250),
    Stat('attack', 'ATK'),
    Stat('defense', 'DEF'),
    Stat('sp_defense', 'Sp. DEF'),
    Stat('sp_attack', 'Sp. ATK'),
    Stat('speed', 'SPD')
]

type_colors = {
    'normal': 'grey54',
    'fire': 'red',
    'water': 'deep_sky_blue3',
    'electric': 'bright_yellow',
    'grass': 'green',
    'ice': 'sky_blue1',
    'fighting': 'indian_red',
    'poison': 'purple',
    'ground': 'sandy_brown',
    'flying': 'orchid1',
    'psychic': 'pink1',
    'bug': 'spring_green1',
    'rock': 'tan',
    'ghost': 'blue_violet',
    'dragon': 'slate_blue3'
}
