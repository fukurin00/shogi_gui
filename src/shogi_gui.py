import random
import os
import pygame
import numpy as np
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_WIDHT = 700
BOARD_HEIGHT = 700
black = (0,0,0)
white = (255,255,255)
chacol = (187,156,105)

 
man_dict = {0:'nothing',1:'fuhyou', 2:'kyosya', 3:'keima', 4:'ginsyou', 5:'kinsyou', 6:'gakugyou', 7:'hisya', 8:'ousyou'}
left,top = (SCREEN_WIDTH-BOARD_WIDHT)/2, (SCREEN_HEIGHT-BOARD_HEIGHT)/2 
board_size = int(BOARD_HEIGHT/9)


class App:
    '''
    pygameのループ
    '''
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = SCREEN_WIDTH,SCREEN_HEIGHT
 
    def on_init(self):
        pygame.init()
        pygame.display.set_caption("shogi-gui")
        self._display_surf = pygame.display.set_mode(self.size)
        self._running = True
        self.background = Background(chacol,BOARD_WIDHT,BOARD_HEIGHT)
        self._display_surf.fill(white)
        self._display_surf.blit(self.background.image, (left,top))
        
        
        self.game = Game()

        for i in range(1,10,1):
            for j in range(1,7,1):
                if j<=3:
                    man = self.game.board.squares[i][j].man
                else:
                    man = self.game.board.squares[i][j+3].man
                if man.chara != 0:
                    self._display_surf.blit(man.image, (left+(man.x-1)*board_size+1,top+(man.y-1)*board_size+1))
        
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

class Man:
    '''
    各コマ
    '''
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.chara = self.set_chara()
        self.player = self.set_player()
        if self.chara != 0:
            self.image = pygame.image.load(os.path.join("../image",man_dict[self.chara]+".png"))
            self.image = pygame.transform.smoothscale(self.image, (board_size,board_size))
            if self.player==1:
                self.image = pygame.transform.rotate(self.image,180)
        else:
            self.image = None

    def set_chara(self)->int:
        if self.y==3 or self.y==7:
            chara = 1
        elif self.y==1 or self.y==9:
            chara = 8
        else:
            chara = 0
        
        return chara
        
    def set_player(self)->int:
        player = 0
        if 1<=self.y and self.y<=3:
            player = 1
        if self.y>=7:
            player = 0
        return player
            
        
class Square:
    ''' 
    各マス
    '''
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.man = Man(x,y)
        

class Board:
    '''
    盤
    '''
    def __init__(self)->None:
        squares = []
        for i in range(10):
            for j in range(10):
                squares.append(Square(i,j))
        
        self.squares = np.array(squares)
        self.squares.shape=10,10

class Game:
    '''
    ゲームを進める
    '''
    def __init__(self):
        self.board = Board()


        


class Background(pygame.sprite.Sprite):
    '''
    背景
    '''
    def __init__(self,color=chacol, w=1000, h=1000):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
        for i in range(10):
            pygame.draw.line(self.image, (0,0,0), [i*w/9, 0], [i*w/9, h], 5)
            pygame.draw.line(self.image, (0,0,0), [0, i*h/9], [w, i*h/9], 5)
        


if __name__ == '__main__':
    app = App()
    app.on_execute()