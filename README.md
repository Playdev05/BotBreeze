# BotBreeze

A simple chess bot in python made just for fun :D

![Static Badge](https://img.shields.io/badge/BotBreeze-%20v.%200.0.1-blue) [![Static Badge](https://img.shields.io/badge/Elo%20-800-blue?logo=lichess)](https://lichess.org) ![Static Badge](https://img.shields.io/badge/Python%20Version-3.8%2B-blue) ![Static Badge](https://img.shields.io/badge/Status%20-Development-orange) ![Static Badge](https://img.shields.io/badge/License%20-BSD%203--clause-blue)




## Description

Botbreeze is a lightweight bot built in ~100 lines of code(excluding comments and line breaks)! It plays players up to 850 elo(Casual games with depth 12) in [Lichess.](https://lichess.org)

*BotBreeze is still in development version 0.0.1. Expect improvements and changes*
### Features:
- Negamax with alpha-beta prunning
- Quiescence search
- PSTs
- ... And many more!

## Instalation:
### Requirements:
- Python 3.8 or higher
- Pip(Python package installer)
The installation is really simple(for python):
```python
pip install botbreeze
```

## Playing BotBreeze
To play botbreeze, all you need to do is this(play as black):
```python
import botbreeze as bb
bb.engine.startboard(color="BLACK", depth=6)
```

## Documentation

**You can read the docs [here](https://pypi.org/project/botbreeze)**