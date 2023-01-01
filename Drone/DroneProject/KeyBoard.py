import pygame

class KeyBoard:

    def init(self):
        pygame.init()
        win = pygame.display.set_mode((720, 480))

    def getKey(self, Key):
        result = False
        for e in pygame.event.get():
            pass
        KeyInput = pygame.key.get_pressed()
        myKey = getattr(pygame, 'K_{}'.format(Key))

        if KeyInput[myKey]:
            result = True
        pygame.display.update()

        return result
