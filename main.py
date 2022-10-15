import sys
import mempuzzle
from mpuzzle_const import *
import drawing
import pygame


newgame = mempuzzle.Mpuzzle_state()
render = drawing.Mpuzzle_render(newgame)
render.initScreen()
myfont = pygame.font.Font(None, 32)
mysmallfont = pygame.font.Font(None, 14)
mytext = myfont.render("you win!", True, BLACK)
helptext = mysmallfont.render("Click on 2 boxes to try to match them. Click again to clear your selection. Remember to say encouraging words for Karate Cat.", True, WHITE)
losetext = myfont.render("you lose! leave this game!!", True, RED)
mousex, mousey = 0, 0
anispeed = drawing.Mpuzzle_render.FPS // 15
fightercat = drawing.Animation(anispeed)
fightercat_pos_x, fightercat_pos_y = 500, 25
fightercat.load_ssheet("cat_ani_fighter.png", 64, 64, 3, 9)

while True:

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
    if render.gamestate.hasWon():
        render.displaySurf.blit(mytext, (300, 10))

    #display the lose screen
    if render.gamestate.hasLost():
        fightercat2 = drawing.Animation(anispeed)
        fightercat2.load_ssheet("cat_ani_fighter.png", 64, 64, 4, 8)
        fightercat2.setpos(200, 200)

        while True:
            render.tick()
            render.drawLoseScreen()
            fightercat2.adv()
            fightercat2.draw_ssheet(render.displaySurf)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    #display the win screen
    if render.gamestate.hasWon():
        fightercat3 = drawing.Animation(anispeed)
        fightercat3.load_ssheet("cat_ani_fighter.png", 64, 64, 8, 12)
        fightercat3.setpos(200, 200)

        while True:
            render.tick()
            render.drawWinScreen()
            fightercat3.adv()
            fightercat3.draw_ssheet(render.displaySurf)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()    
    pygame.display.update()



