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
egg_speed_acceleration = 0.5
egg_behind_border = 100
score = 0

player_lives = player_start_lives
player_current_speed = player_speed
egg_current_speed = egg_speed

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

game_over_text = harry_font_big.render("Hra skoncila", True, dark_yellow)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (Width//2, height//2)

continue_text = harry_font_middle.render("Chces hrat znovu? Stiskni libovolnou klavesu", True, dark_yellow)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (Width//2, height//2 + 40)

# Zvuky a muzika v pozadi
pygame.mixer.music.load("sound/harrypotter.sound.mp3")
pygame.mixer.music.play(-1, 0.0)
loose_life_sound = pygame.mixer.Sound("sound/vedlesound.mp3")
loose_life_sound.set_volume(1.0)
take_egg_sound = pygame.mixer.Sound("sound/item-pick-up.mp3")
take_egg_sound.set_volume(0.8)

# Obrazky
harry_image = pygame.image.load("img/PumpkinPotter.png")
harry_image_rect = harry_image.get_rect()
harry_image_rect.center = (60, height//2)

egg_image = pygame.image.load("img/Egg.png")
egg_image_rect = egg_image.get_rect()
egg_image_rect.x = Width + egg_behind_border
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
        harry_image_rect.y -= player_current_speed
        
    elif keys[pygame.K_DOWN] and harry_image_rect.bottom < height:
        harry_image_rect.y += player_current_speed
        
    #pohyb vejce
    if egg_image_rect.x < 0:
        player_lives -= 1 
        egg_image_rect.x = Width + egg_behind_border
        egg_image_rect.y = random.randint(60, height-48)
        loose_life_sound.play()
    else:
        egg_image_rect.x -= egg_current_speed
        
    # kontrola kolize
    if harry_image_rect.colliderect(egg_image_rect):
        score += 1
        egg_current_speed += egg_speed_acceleration
        player_current_speed += egg_speed_acceleration
        egg_image_rect.x = Width + egg_behind_border
        egg_image_rect.y = random.randint(60, height-48)
        take_egg_sound.play()
        
    #znovu vykresleni obrazovky
    screen.fill(black)
    
    # Tvary
    pygame.draw.line(screen, dark_yellow, (0, 60), (Width, 60), 2)
    
    # texty _zivoty
    lives_text = harry_font_middle.render(f"Live: {player_lives}", True,  dark_yellow )
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.right = Width - 20 
    lives_text_rect.top = 15
    
    score_text = harry_font_middle.render(f"Skore: {score}", True, dark_yellow)
    score_text_rect = score_text.get_rect()
    score_text_rect.left = 20
    score_text_rect.top = 15
    
     # Texty
    screen.blit(game_name, game_name_rect) 
    screen.blit(score_text, score_text_rect) 
    screen.blit(lives_text, lives_text_rect)  

    # Obrazky
    screen.blit(harry_image, harry_image_rect)
    screen.blit(egg_image, egg_image_rect)  
    
    # kontrola konce hry 
    if player_lives == 0:
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()
        pygame.mixer.music.stop()
        
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = player_start_lives
                    egg_current_speed = egg_speed
                    harry_image_rect.y = height//2
                    player_current_speed = player_speed 
                    pause = False
                    pygame.mixer.music.play(-1, 0.0)
                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False         

    # Update obrazovky     
    pygame.display.update()

    # Zpomaleni cyklus
    clock.tick(fps)

# Ukonceni hry
pygame.quit()