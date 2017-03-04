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
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'EL CHUPA'
    }

'''def dangerzone(nextdirr):
    bodyParts = data['snakes'][0]['coords']
    for parts in bodyParts:
        if nextdirr == parts:
            return False
    return True
def computenextdirr(dirr,xhead,yhead):
    if dirr == 'up':
        return (xhead,yhead+1)
    if dirr == 'down':
        return (xhead,yhead-1)
    if dirr == 'left':
        return (xhead-1,yhead)
    if dirr == 'right':
        return (xhead+1,yhead) 
'''
        
@bottle.post('/move')
def move():
    data = bottle.request.json
    board_height = data['height']
    board_width = data['width']
    

    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']
    dirr = directions[1]
    
    
    #grab head coordinates
    coords1 = data['snakes']
    coords2 = coords1[0]
    coords = coords2['coords']
    head = coords[0]
    xhead = head[0]
    yhead = head[1]
    

    close_food = find_close_food(data,xhead,yhead)
    dirr = find_food(close_food,xhead,yhead)
    return {
        'move': dirr,
        'taunt': 'battlesnake-python!'
    }
def find_close_food(data,xhead,yhead):
    food = data['food']
    closeFoodDist = 1000
    closeFoodx = 0
    closeFoody = 0
    for food in food:
        foodx = food[0]
        foody = food[1]
        dist = abs(xhead-foodx) + abs(yhead-foody)
        if dist < closeFoodDist:
            closeFoodDist = dist
            closeFoodx = food[0]
            closeFoody = food[1]
    return close_food(closeFoodx,closeFoody)
def find_food(close_food,xhead,yhead):
    closeFoodx = close_food[0]
    closefoody = close_food[1]
    movx = closeFoodx-xhead
    movy = closeFoody-yhead
    if movx !=0:
        if movx>0:
            return directions[3]
        elif movx<0:
            return directions[2]
    elif movy !=0:
        if movy>0:
            return directions[1]
        elif movy<0:
            return directions[0]

def dontHitWalls():
    if yhead == board_height-1:
        dirr = directions[2]  
   
    if xhead == 0:
        dirr = directions[0]
        
    if yhead == 0:
        dirr = directions[3]
    
    if xhead == board_width-1 and yhead != board_height-1:
        dirr = directions[1]


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))