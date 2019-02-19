import bottle
import os
import random
from astar import AStar


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

    return {
        'color': '#7300E6',
        'taunt': '{} ({}x{})'.format(game_id, 1, 1),
        'head_url': head_url
    }

@bottle.post('/move')
def move():
    data = bottle.request.json
    board = data.get('board')
    board_height = board.get('height')
    board_width = board.get('width')

    # print(board)
    GRID = buildGrid(board, board_height, board_width)
    # print(GRID)
    # TODO: Do things with data
    # get the snake
    VINCE = data['you']
    xhead = VINCE['body'][0]['x']
    yhead = VINCE['body'][0]['y']
    head_tuple = (xhead, yhead)

    # first food bit
    first_food_bit = (board['food'][0]['x'], board['food'][0]['y'])
    AS = AStar()
    path_to_food = AS.find_path(GRID, head_tuple, first_food_bit)
    print(path_to_food)
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    direction = get_dir(head_tuple, path_to_food[1])
    print(direction)
    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }

def buildGrid(board, ht, w):
    grid = [[0 for i in range(w)] for j in range(ht)] # initialize a grid of 1s
    for snake in board.get('snakes'):
        for snake_parts in snake.get('body'):
            sx = snake_parts['x']
            sy = snake_parts['y']
            grid[sx][sy] = -1

    return grid
    # for foodbits in board.food:
    #     grid[foodbits.x][foodbits.y] = 

def get_dir(start, end):
    direction = (start[0] - end[0], start[1] - end[1])
    print(direction)
    if(direction == (0, -1)):
        return 'down'
    elif(direction == (0, 1)):
        return 'up'
    elif(direction == (-1, 0)):
        return 'right'
    elif(direction == (1, 0)):
        return 'left'
# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
