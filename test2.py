import pygame
import pygame.freetype

# Window size
WINDOW_WIDTH    = 400
WINDOW_HEIGHT   = 400

DARK_BLUE  = (   3,   5,  54)
STARRY     = ( 230, 255, 80 )


### initialisation
pygame.init()
window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
pygame.display.set_caption("Star")

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
#my_font = pygame.font.SysFont('Comic Sans MS', 30)
GAME_FONT = pygame.freetype.Font("moveon.ttf", 24)

text_surface, rect = GAME_FONT.render('Meteor Rain', (255, 255, 255))

# Define a star
centre_coord = ( WINDOW_WIDTH//2, WINDOW_HEIGHT//2 )
star_point  = [ (165 + 30, 151 + 20), (200, 20 + 100), (235 - 30, 151 + 20), (371 - 100, 164 + 10), (257 - 50, 219 - 40),
                 (200, 346 - 110), (143 + 50, 219 - 40), (29 + 100, 164 + 10)   ]
star_points  = [ (195-129, 171-120), (200-129, 120-120), (205-129, 171-120), (271-129, 174-120), (205-129, 179-120),
                 (200-129, 236-120), (195-129, 179-120), (129-129, 174-120)]

window.blit(text_surface, (10,10))
GAME_FONT.render_to(window, (10, 40), "by Meihui Liu", (255, 255, 255))

### Main Loop
clock = pygame.time.Clock()
done = False
while not done:

    # Handle user-input
    for event in pygame.event.get():
        if ( event.type == pygame.QUIT ):
            done = True

    # Re-draw the window
    window.fill( DARK_BLUE )                             # background fill
    pygame.draw.polygon( window, STARRY, star_points )   # Draw the star
    #window.blit(text_surface, (10,10))
    #GAME_FONT.render_to(window, (10, 40), "by Meihui Liu", (255, 255, 255))

    pygame.display.flip()                                # Update the display

    # Clamp FPS
    clock.tick_busy_loop(60)

pygame.quit()