import pygame 
import random  
import math

# Inicializace hry
pygame.init()

# Obrazovka NASTAVENI
screen_width = 1366
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Harry Potter a Ohnivý pohár")
pygame.mouse.set_visible(False)

# Nastaveni hry
player_start_lives = 10
player_start_speed = 5
egg_start_speed = 5
egg_speed_acceleration = 0.1
egg_behind_border = 100
score = 0
x, y = screen_width//2, screen_height//2
x_axis, y_axis = 0.0, 0.0

player_current_lives = player_start_lives
player_current_speed = player_start_speed
egg_current_speed = egg_start_speed

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
game_name_rect.center = (screen_width//2, 30)

game_over_text = harry_font_big.render("Hra skoncila", True, dark_yellow)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (screen_width//2, screen_height//2)

continue_text = harry_font_middle.render("Chces hrat znovu? Stiskni libovolnou klavesu", True, dark_yellow)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (screen_width//2, screen_height//2 + 40)

continue_text1 = harry_font_middle.render("Chces hrat znovu? Stiskni libovolnou klavesu", True, dark_yellow)
continue_text_rect1 = continue_text1.get_rect()
continue_text_rect1.center = (screen_width//2, screen_height//2 + 50)

win_text = harry_font_big.render("Vyhral si!!!", True, dark_yellow)
win_text_rect = win_text.get_rect()
win_text_rect.center = (screen_width//2, screen_height//2 + 15)

# Zvuky a muzika v pozadi
pygame.mixer.music.load("sound/harrypotter.sound.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0)

loose_life_sound = pygame.mixer.Sound("sound/vedlesound.mp3")
loose_life_sound.set_volume(0.5)

take_egg_sound = pygame.mixer.Sound("sound/item-pick-up.mp3")
take_egg_sound.set_volume(0.5)

haha_sound = pygame.mixer.Sound("sound/evil-laugh.mp3")
haha_sound.set_volume(1.0)

# Obrazky
background_image = pygame.image.load('img/background.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_image.set_alpha(0)

harry_image = pygame.image.load("img/hp.png")
harry_image_rect = harry_image.get_rect()
harry_image_rect.center = (screen_width//2, screen_height//2)

egg_image = pygame.image.load("img/Egg.png")
egg_image_rect = egg_image.get_rect()
egg_image_rect.x = screen_width + egg_behind_border
egg_image_rect.y = random.randint(60, screen_height-48)

pohar_image = pygame.image.load("img/cup.png")
pohar_image_rect = pohar_image.get_rect()
pohar_image_rect.center = (screen_width//2, screen_height//2 - 60)

# inicializace joystiku
pygame.joystick.init()

# kontrola ze je pripojen
if pygame.joystick.get_count() == 0:
    print("Zadny joystick nenalezen.")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

#####################
### Hlavni cyklus ###
#####################

lets_continue = True

while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
    
    # promenne pro zmenu pohybu
    dx, dy = 0, 0
    
    # pohyb joystiku
    if pygame.joystick.get_count() != 0:
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)
    
        if (y_axis < -0.1) and harry_image_rect.top > 60:
            dy -= (player_current_speed/5) * (abs(y_axis)*10)
        elif (y_axis > 0.1) and harry_image_rect.bottom < screen_height:
            dy += (player_current_speed/5) * (abs(y_axis)*10)
        if (x_axis < -0.1) and harry_image_rect.left > 0:
            dx -= (player_current_speed/5) * (abs(x_axis)*10)
        elif (x_axis > 0.1) and harry_image_rect.right < screen_width:
            dx += (player_current_speed/5) * (abs(x_axis)*10)

    # Pohyb klavesami
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP]) and harry_image_rect.top > 60:
        dy -= player_current_speed / 5 * 10   
    elif (keys[pygame.K_DOWN]) and harry_image_rect.bottom < screen_height:
        dy += player_current_speed / 5 * 10
    if (keys[pygame.K_LEFT]) and harry_image_rect.left > 0:
        dx -= player_current_speed/5*10
    elif (keys[pygame.K_RIGHT]) and harry_image_rect.right < screen_width:
        dx += player_current_speed/5*10
    
    # Klavesa pro konec hry
    if (keys[pygame.K_ESCAPE] or keys[pygame.K_q]):
        lets_continue = False

    # otaceni Harryho
    angle = math.degrees(math.atan2(-dy, dx))  # atan2(y, x) vrací úhel v radiánech
    rotated_image = pygame.transform.rotate(harry_image, angle)
    
    # zrcadlove otoceni obrazku, kdyz leti doleva
    if (-180 <= angle < -90) or (180 >= angle > 90):
        rotated_image = pygame.transform.flip(rotated_image, False, True)
    
    # Aktualizace pozice Harryho
    x += dx
    y += dy
    harry_image_rect = rotated_image.get_rect(center=(x, y))
     
    #pohyb vejce
    if egg_image_rect.x < 0:
        player_current_lives -= 1 
        egg_image_rect.x = screen_width + egg_behind_border
        egg_image_rect.y = random.randint(60, screen_height-48)
        loose_life_sound.play()
    else:
        egg_image_rect.x -= egg_current_speed
        
    # kontrola kolize
    if harry_image_rect.colliderect(egg_image_rect):
        score += 1
        egg_current_speed += egg_speed_acceleration
        player_current_speed += egg_speed_acceleration
        egg_image_rect.x = screen_width + egg_behind_border
        egg_image_rect.y = random.randint(60, screen_height-48)
        take_egg_sound.play()
        background_image.set_alpha(score)
        
        if score % 50 == 0:
            haha_sound.play()
        
    #znovu vykresleni obrazovky
    screen.fill(black)
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screen_width, 60))
    
    # Tvary
    pygame.draw.line(screen, dark_yellow, (0, 60), (screen_width, 60), 2)
    
    # texty zivoty
    lives_text = harry_font_middle.render(f"Lives: {player_current_lives}", True,  dark_yellow )
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.right = screen_width - 20 
    lives_text_rect.top = 15
    
    score_text = harry_font_middle.render(f"Score: {score}", True, dark_yellow)
    score_text_rect = score_text.get_rect()
    score_text_rect.left = 20
    score_text_rect.top = 15
    
     # Texty
    screen.blit(game_name, game_name_rect) 
    screen.blit(score_text, score_text_rect) 
    screen.blit(lives_text, lives_text_rect)  

    # Obrazky
    screen.blit(rotated_image, harry_image_rect)
    screen.blit(egg_image, egg_image_rect) 
    
    # ziskani poharu pri score 200
    if score == 200:
        background_image.set_alpha(255)
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, (screen_height//2)-30, screen_width, 100))
        screen.blit(pohar_image, pohar_image_rect) 
        screen.blit(continue_text1, continue_text_rect1)
        screen.blit(win_text, win_text_rect)
        pygame.mixer.music.stop()
        pygame.display.update()
        
        pause = True
        while pause:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN) or (event.type == pygame.JOYBUTTONDOWN):
                    score = 0
                    background_image.set_alpha(0)
                    player_current_lives = player_start_lives
                    egg_current_speed = egg_start_speed
                    harry_image_rect.y = screen_height//2
                    player_current_speed = player_start_speed 
                    pause = False
                    pygame.mixer.music.play(-1, 0.0)
                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False         
  
    # kontrola konce hry 
    if player_current_lives == 0:
        background_image.set_alpha(0)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, (screen_height//2)-30, screen_width, 100))
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()
        pygame.mixer.music.stop()
        
        pause = True
        while pause:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN) or (event.type == pygame.JOYBUTTONDOWN):
                    score = 0
                    player_current_lives = player_start_lives
                    egg_current_speed = egg_start_speed
                    harry_image_rect.y = screen_height//2
                    player_current_speed = player_start_speed 
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