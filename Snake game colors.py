""" Version 1.0.1 """

# Importing modules
import sys, random, time, pygame

# Check errors
# Pygame.init returns suc. process and errors in tuple
check_errors = pygame.init()
if check_errors[1] > 0:
    print('Error(s) found..Exiting')
    sys.exit(-1)
else:
    print('initialization successful..')

# Sets the display surface
score = 0
play_surface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('Snake Game')

# Colors
teal = (0, 128, 128)
purple = (128, 0, 128)
green = (0, 128, 0)
olive = (128, 128, 0)
white = (255, 255, 255) # Background
red = (255, 0, 0) # Food
blue = (0, 0, 255) # Text
black = (0, 0, 0) # Score

# List of colors
color_list = [teal, purple, green, olive, red, blue, black]

# Get HIGH SCORE

def get_high_score():
    HI = open('Snake_high_score.txt', 'r')
    high_score = int(HI.read())
    if score > high_score:
        HI = open('Snake_high_score.txt', 'w')
        HI.write(str(score))
        HI.close()
        return score
    else:
        HI.close()
        return high_score


# Score board
def show_score(choice):
    Sfont = pygame.font.SysFont('comicsansms', 16)
    Ssurface = Sfont.render('Score: ' + str(score), True, black)
    Srect = Ssurface.get_rect()
    if choice == 1:
        Srect.midtop = (40, 10)
    else:
        Srect.midtop = (360, 150)
    play_surface.blit(Ssurface, Srect)

# FPS controller
FPS_controller = pygame.time.Clock()

# Snake position
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
scolor = color_list[random.randrange(0, 7)]
changeto = direction

# Food position
fcolor = color_list[random.randrange(0, 7)]
fpos = [random.randrange(1, 72)*10, random.randrange(1, 46)*10]
fspawn = True


# Game Over function
def game_over():
    GOfont = pygame.font.SysFont('comicsansms', 72)
    HIfont = pygame.font.SysFont('monaco', 32)
    HIsurface = HIfont.render('High Score: ' + str(get_high_score()), True, black)
    HIrect = HIsurface.get_rect()
    HIrect.midtop = (360, 120)
    play_surface.blit(HIsurface, HIrect)
    GOsurface = GOfont.render('Game Over!', True, blue)
    GOrect = GOsurface.get_rect()
    GOrect.midtop = (360, 15)
    play_surface.blit(GOsurface, GOrect)
    show_score(0)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()


# Main logic
def main():
    global changeto, direction, scolor, fspawn, score, fcolor, fspawn, fpos
    i = 10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    changeto = 'DOWN'
                if event.key == pygame.K_UP or event.key == ord('w'):
                    changeto = 'UP'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    changeto = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    changeto = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Direction validation
        if changeto == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'
        if changeto == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'
        if changeto == 'UP' and not direction == 'DOWN':
            direction = 'UP'
        if changeto == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'

        # Update the snake position [x,y]
        if direction == 'RIGHT':
            snake_pos[0] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10

        # Snake body mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == fpos[0] and snake_pos[1] == fpos[1]:
            scolor = fcolor
            fspawn = False
            score += 5
            i += (1/2)
        else:
            snake_body.pop()
        if fspawn == False:
            fcolor = color_list[random.randrange(0, 7)]
            while fcolor == scolor:
                fcolor = color_list[random.randrange(0, 7)]
            fpos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
        fspawn = True

        play_surface.fill(white)

        for pos in snake_body:
            pygame.draw.rect(play_surface, scolor, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(play_surface, fcolor, pygame.Rect(fpos[0], fpos[1], 10, 10))

        # Check if game is over
        if snake_pos[0] > 710 or snake_pos[0] < 0:
            game_over()
        elif snake_pos[1] > 450 or snake_pos[1] < 0:
            game_over()
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        show_score(1)
        pygame.display.flip()
        FPS_controller.tick(i)

if __name__ == '__main__':
    main()
