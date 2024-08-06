import pygame 
import random  

# Inicializace hry
pygame.init()

# Obrazovka NASTAVENI
Width = 1000
height = 500
screen = pygame.display.set_mode((Width, height))
pygame.display.set_caption("Harry Potter a Ohnivý pohár")

# Nastaveni hry
player_start_lives = 5
player_speed = 5
egg_speed = 5
eeg_speed_acceleration = 0.5
eeg_behind_border = 100
score = 0

player_lives = player_start_lives
eeg_current_speed = egg_speed

# FPS a hodiny
fps = 60
clock = pygame.time.Clock()

# Barvy
dark_yellow = pygame.Color("#938f0c")
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Fonty
harry_font_big = pygame.font.Font("font/HarryPotter.ttf", 50)
harry_font_middle = pygame.font.Font("font/HarryPotter.ttf", 30)

# Text
game_name = harry_font_big.render("Harry Potter and goblet of fire", True, dark_yellow)
game_name_rect = game_name.get_rect()
game_name_rect.center = (Width//2, 30)

score_text = harry_font_middle.render(f"Skore: {score}", True, dark_yellow)
score_text_rect = score_text.get_rect()
score_text_rect.left = 20
score_text_rect.top = 15

# Zvuky a muzika v pozadi

# Obrazky
harry_image = pygame.image.load("img/PumpkinPotter.png")
harry_image_rect = harry_image.get_rect()
harry_image_rect.center = (60, height//2)

egg_image = pygame.image.load("img/Egg.png")
egg_image_rect = egg_image.get_rect()
egg_image_rect.x = Width + eeg_behind_border
egg_image_rect.y = random.randint(60, height-48)


# Hlavni ciklus
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
            
    # Pohyb klavesami
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_UP] and harry_image_rect.top > 60:
        harry_image_rect.y -= player_speed
        
    elif keys[pygame.K_DOWN] and harry_image_rect.bottom < height:
        harry_image_rect.y += player_speed
        
    #pohib vejce
    if egg_image_rect.x < 0:
        player_lives -= 1 
        egg_image_rect.x = Width + eeg_behind_border
        egg_image_rect.y = random.randint(60, height-48)
    else:
        egg_image_rect.x -= egg_speed      
        
    #znovu vykresleni obrazovky
    screen.fill(black)
    
    # Tvary
    pygame.draw.line(screen, dark_yellow, (0, 60), (Width, 60), 2)
    
    # texty _zivoty
    lives_text = harry_font_middle.render(f"Live: {player_lives}", True,  dark_yellow )
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.right = Width - 20 
    lives_text_rect.top = 15


    # Obrazky
    screen.blit(harry_image, harry_image_rect)
    screen.blit(egg_image, egg_image_rect)        

    # Texty
    screen.blit(game_name, game_name_rect) 
    screen.blit(score_text, score_text_rect) 
    screen.blit(lives_text, lives_text_rect)      

    # Update obrazovky     
    pygame.display.update()

    # Zpomaleni cyklus
    clock.tick(fps)

# Ukonceni hry
pygame.quit()