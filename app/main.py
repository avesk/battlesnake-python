import bottle
import os
import random


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#FFFFFF',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    coords = data['coords']

    # dir = check_collisions(coords)
    directions = ['up', 'down', 'left', 'right']
    dir = directions[2]
    
    return {
        'move': random.choice(directions),
        'taunt': 'battlesnake-python!'
    }

# def check_collisions(coords):
#     head = coords[0]
#     x = head[0]
#     y = head[1]
#     horiz = {'left' : x-1, 'right' : x+1}
#     vert = {'up' : y+1, 'down' : y-1}

#     for coord in coords:
#         if coord != [ horiz['left'], y ]
#             return 'left'
#         if coord != [ horiz['right'], y ]
#             return 'right'
#         if coord != [ x, vert['up'] ]
#             return 'up'
#         if coord != [ x, vert['down'] ]
#             return 'down'

#         else return 'down'



# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
