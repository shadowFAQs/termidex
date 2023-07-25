# Termidex

Look up gen 1 Pokémon by name or Pokédex number from your Terminal app.



https://github.com/shadowFAQs/termidex/assets/36905164/2e08c5ca-bab9-455a-86dd-45bab35459a3



Uses [Rich](https://github.com/Textualize/rich) for colorful displays and animated stat bars. I've only tested it on Windows Terminal, but Termidex should work on any OS as long as you have Python 3.7 or later.

### Dependencies

- rich (I'm using v13.4.2)

### Usage

Look up a Pokémon by name:

`>>> python /path/to/dex.py --lookup growlithe`

Look up a Pokémon by gen 1 Pokédex number:

`>>> python /path/to/dex.py -l 58`

See info for a random gen 1 Pokémon:

`>>> python /path/to/dex.py --random`

### Resources

- Pokédex JSON file from [smogon.com](https://smogon.com)
- Rich's ["Dynamic Progress" example](https://github.com/Textualize/rich/blob/master/examples/dynamic_progress.py)
