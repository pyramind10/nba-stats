# NBA-Stats
NBA-Stats includes python scripts to obtain stats for specific NBA players for easy access and manipulation. Example usage: Viewing stats of Dirk Nowitzki for his last five games played. Made and meant for fantasy basketball and easy access to useful statistical information.

## Packages required

- lxml
- requests

## Usage

### Player by player

To get information about one player against a certain team for the last X games.
```
py main.py
```

### List

To get information and averages of multiple players over multiple games.
```
py list.py PLAYERS.txt
```

*PLAYERS.txt* is any list of players.

#### Format of list

Example for John Wall playing against the Brooklyn Nets:
```
john wall, brk
```

## Todo

- Add player to player matchups for starters

## Notes

Usage requires *private.py*
