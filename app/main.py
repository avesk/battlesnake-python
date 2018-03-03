import bottle
import os
import random


@bottle.route('/')
def static():
    return "the server is running"

@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#7300E6',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }

'''def dangerzone(nextdirr):
    bodyParts = data['snakes'][0]['coords']
    for parts in bodyParts:
        if nextdirr == parts:
            return False
    return True
'''

@bottle.post('/move')
def move():
    data = bottle.request.json
    board_height = data['height']
    board_width = data['width']


    # TODO: Do things with data

    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    print direction
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
