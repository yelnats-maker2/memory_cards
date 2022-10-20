import sys
import mempuzzle
from mpuzzle_const import *
import drawing
import pygame

#main objects
newgame = mempuzzle.Mpuzzle_state()
render = drawing.Mpuzzle_render(newgame)
render.initScreen()

#texts
myfont = pygame.font.Font(None, 32)
mysmallfont = pygame.font.Font(None, 14)
mytext = myfont.render("you win!", True, BLACK)
helptext = mysmallfont.render("Click on 2 boxes to try to match them. Click again to clear your selection. Remember to say encouraging words for Karate Cat.", True, WHITE)
losetext = myfont.render("you lose! leave this game!!", True, RED)
starttext = myfont.render("press a key to begin!", True, GREEN)

#cat fighter spritesheet from
#https://opengameart.org/content/cat-fighter-sprite-sheet
#by dogchicken
anispeed = drawing.Mpuzzle_render.FPS // 15 #set speed for all animations

#animation for playing
fightercat = drawing.Animation(anispeed)
fightercat_pos_x, fightercat_pos_y = 500, 25
fightercat.load_ssheet("cat_ani_fighter.png", 64, 64, 3, 9)

#animation for the win screen
fightercat2 = drawing.Animation(anispeed)
fightercat2.load_ssheet("cat_ani_fighter.png", 64, 64, 4, 8)
fightercat2.setpos(200, 200)

#animation for the lose screen, fuck it we all have 8GB ram
fightercat3 = drawing.Animation(anispeed)
fightercat3.load_ssheet("cat_ani_fighter.png", 64, 64, 8, 12)
fightercat3.setpos(200, 200)

#animation for opening screen
fightercat4 = drawing.Animation(anispeed)
fightercat4.load_ssheet("cat_ani_fighter.png", 64, 64, 5, 6)
fightercat4.setpos(200, 200)

mousex, mousey = 0, 0
while newgame.state == newgame.MODE_START:

    render.tick()
    render.displaySurf.fill(NAVYBLUE)
    render.displaySurf.blit(starttext, (100, 10))
    fightercat4.adv()
    fightercat4.draw_ssheet(render.displaySurf)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            newgame.begin()
            render.displaySurf.blit(losetext, (200, 10))
            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    

while newgame.state == newgame.MODE_PLAYING:

    render.tick()
    render.drawBoard()
    fightercat.setpos(fightercat_pos_x, fightercat_pos_y)
    fightercat.adv()
    fightercat.draw_ssheet(render.displaySurf)
    
    mouseclicked = False
    #handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouseclicked = True
        if event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos

    rect = render.getBoxAtPixel(mousex, mousey)
    if rect != None:
        render.drawHighlightBox(rect[0], rect[1])
        if mouseclicked == True:
            render.gamestate.selectBox(rect[0], rect[1])
            #make the cat move across the screen
            fightercat_pos_x = (fightercat_pos_x + 50) % drawing.Mpuzzle_render.WINDOWWIDTH

    #blit texts
    triesnum = myfont.render(("%d/%d tries left" % (render.gamestate.tries, render.gamestate.maxtries)), True, RED)
    render.displaySurf.blit(triesnum, (450, 240))
    render.displaySurf.blit(helptext, (5, 400))

    pygame.display.update()

while newgame.state == newgame.MODE_WON:
    render.tick()
    render.drawWinScreen()
    fightercat3.adv()
    fightercat3.draw_ssheet(render.displaySurf)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()    
    
while newgame.state == newgame.MODE_LOST:
    render.tick()
    render.drawLoseScreen()
    fightercat2.adv()
    fightercat2.draw_ssheet(render.displaySurf)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()



