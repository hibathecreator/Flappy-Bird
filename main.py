import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((576, 800))
pygame.display.set_caption('Flappy Bird')

clock = pygame.time.Clock()

bg_surface = pygame.image.load('background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (576, 800))

floor_surface = pygame.image.load('base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (576, 124))
floor_x_pos = 0

bird_downflap = pygame.transform.scale(pygame.image.load('bluebird-downflap.png').convert_alpha(), (55, 35))
bird_midflap = pygame.transform.scale(pygame.image.load('bluebird-midflap.png').convert_alpha(), (55, 35))
bird_upflap = pygame.transform.scale(pygame.image.load('bluebird-upflap.png').convert_alpha(), (55, 35))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load('bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale(bird_surface, (55, 35))
# bird_rect = bird_surface.get_rect(center=(100, 400))

pipe_surface = pygame.image.load('pipe-green.png')
pipe_surface = pygame.transform.scale(pipe_surface, (52, 350))

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [350, 450, 600]

game_over_surface = pygame.transform.scale(pygame.image.load('message.png').convert_alpha(), (400, 500))
game_over_rect = game_over_surface.get_rect(center=(288, 400))

flap_sound = pygame.mixer.Sound('sfx_wing.wav')
death_sound = pygame.mixer.Sound('sfx_hit.wav')
score_sound = pygame.mixer.Sound('sfx_point.wav')
score_sound_countdown = 100
# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 800 - 124))
    screen.blit(floor_surface, (floor_x_pos + 576, 800 - 124))


def create_pipe():
    random_pipe_hei = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_hei))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_hei - 250))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 676:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 676:
        can_score = True
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(480, 50))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        score_surface = game_font.render('Score: ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(480, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(430, 100))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx <105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0 and can_score == False:
                can_score = True
    return


game_font = pygame.font.Font('04B_19.TTF', 40)
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                score = 0
                pipe_list.clear()
                bird_rect.center = (100, 400)
                bird_movement = 0
                game_active = True

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #score
        pipe_score_check()
        score_display('main_game')
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')
        screen.blit(game_over_surface, game_over_rect)
    # floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
