# Chess AI

This is a python program that uses the mini-max algorithm to predict the next best move. The AI also uses an opening book to predict the best opening moves. Once the AI reaches a novel position, it evaluates the position using square tables, piece values and hanging pieces. Then using the mini-max algorithm the AI finds the best move. 

## Usage
Make sure the chess package is installed
```bash
pip install chess
```
Then to run...
```bash
python runner.py
```
## How to play
By default, the code is set up to run the Player vs Computer function.

The input for your move needs to be a UCI notation
###### Example inputs
- e2e4
- e7e5
- e1g1 (white short castling)
- e7e8q (for promotion)

### Example:
```
pick (white or black): white
eval: 0
```
```
your move: d2d4
eval: 40

AI's move g8f6
eval: -10
```