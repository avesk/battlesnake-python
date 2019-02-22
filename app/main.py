import bottle
import os
import random
from astar import AStar
from OurSnake import OurSnake
from Snake import Snake
from grid import Grid

def state(Vince, Snakes, GameGrid, AS):   
    state.Vince = Vince
    state.Snakes = Snakes
    state.GameGrid = GameGrid
    state.AS =  AS

@bottle.route('/')
def static():
    return "the server is running"

@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data
    # init ourSnake class
    Vince = OurSnake(data['you'])
    # init snake classes
    Snakes = [Snake(snake) for snake in data['board']['snakes']]
    # init grid class
    GameGrid = Grid(data['board'])
    # init Astar class
    AS = AStar

    # set state
    state(Vince, Snakes, GameGrid, AS)

    return {
        'color': '#7300E6',
        'taunt': '{} ({}x{})'.format(game_id, 1, 1),
        'head_url': head_url
    }

@bottle.post('/move')
def move():
    data = bottle.request.json
    # update ourSnake class
    Vince = state.Vince
    Vince.update(data['you'])
    # update snake classes
    Snakes = state.Snakes
    for snake in Snakes:
        snake.update(data['board']['snakes'])
    # update grid class
    GameGrid = state.GameGrid
    GameGrid.update(data['board'])
    print(GameGrid.cells)

    # if health < 25: Astar Closest food
    # else Astar our tail

    direction = 'left'
    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
