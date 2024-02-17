# Tetris
This project is a simple implementation of the Tetris game using Python and Pygame. I used the TetrisFriends rules (since I like them), which specifically means you can hold blocks.

## Install
First, install [Conda](https://docs.conda.io/projects/miniconda/en/latest/) and then run:

```bash
conda create -n mario python=3.11
conda activate mario
conda install -c conda-forge libstdcxx-ng
pip install -e .
```

You can then run the game by running:
```bash
python main.py
```

## Controls
You can control blocks using the arrow or WASD keys. Press 'c' to hold a block and space to make a black drop. After the game ends you can fill in your name and press enter to save your score in the highscores.

