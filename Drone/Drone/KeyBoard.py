import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))

def getKey(Key):
    result = False
    for e in pygame.event.get():
        pass
    KeyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(Key))

    if KeyInput[myKey]:
        result = True
    pygame.display.update()

    return result

if __name__ == '__main__':
    init()