# Frist I would import then initialize all the pygame methods would use in the project. 
import random
import pygame
 
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Then I would set up the screen as well chose a caption for the game. 
screen_width = 500 
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height)) # makes the screen
pygame.display.set_caption("Flappy cat")  


# file stuff

# Then I would make the variables for the sounds in my game as well as make the background music loop. 
background_music = "468212__sergequadrado__soft-background-loop.wav" 
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1) # Whem set to -1, it means that the music will loop indefinitely. 
meow_sound = pygame.mixer.Sound("436541__mafon2__cat-meow.wav")

 
# The sets up all the images I will use in my project. 
image2 = pygame.image.load("pixil-frame-0 (1).png") # Top pipe
image1 = pygame.image.load("pixil-frame-0.png") # Bottom pipe
image3 = pygame.image.load("notfly.png")
image4 = pygame.image.load("fly.png")

# When I loaded in my images originally, I realized that I drew them a little bigger then I needed.
# So I decide to just scale both frames instead of redrawing. 
player_idle = pygame.transform.scale(image3, (image3.get_width() // 3, image3.get_height() // 3))
player_fly = pygame.transform.scale(image4, (image4.get_width() // 3, image4.get_height() // 3))

image_width, image_height = image1.get_size()  # Setint image1's sizes for other lines.

# This fuction plays whenever a new pipe is made.
def spawn_pipe():
    random_image = random.choice([image1, image2]) # This value can be either the top or bottom pipe  
    start_x = screen_width # So the pipe comes from the end of the screen
    start_y = 0 if random_image == image2 else screen_height - image_height # This piece of code makes it so the top pipes have a y of is 0.
    # The bottom ones spawn at screen_height subtrated by the height of the pipes so the pipe ends up touching the bottom of the screen.
    return random_image, start_x, start_y 

# First pipe
current_image, start_x, start_y = spawn_pipe() # makes a new pipe with a random image and starting position.

pipe_speed = 3 
points = 0
score = 0
fall_speed = -5 # how long it will take for the player character to change direction from moving upwards to moving downwards. 
jump_strength = 10  
gravity = 0.5 # it increases the downward velocity of the player character [] frame.

game_started = False
player = player_idle  

# Define player hitbox
Player_x = 0
Player_y = 220
player_hitbox = pygame.Rect(Player_x, Player_y, player.get_width(), player.get_height())

# Define pipe hitbox
pipe_hitbox = pygame.Rect(start_x, start_y, image_width, image_height)
  
# Pink color for clouds
PINK = (255, 192, 203)

# Clouds variables
cloud_radius = 30
cloud_spacing = 150
clouds = []

# Function to create clouds
def create_clouds():
    # How many cloud can fit of the x with one extra off screen to make it look smoother.
    num_clouds = screen_width // cloud_spacing + 1
    for i in range(num_clouds):
        x = i * cloud_spacing
        y = random.randint(cloud_radius, screen_height - cloud_radius)
        clouds.append((x, y))

create_clouds()

# Add text font
text_font = pygame.font.SysFont('freesansbold', 30)

# Display "Press right to play" text
start_text = text_font.render('Press right to play and space to jump', True, (255, 255, 255))
text_rect = start_text.get_rect(center=(screen_width//2, screen_height//2))
screen.blit(start_text, text_rect)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_RIGHT:
                game_started = True
                start_text = None  # Clear the start text when right arrow key is pressed
            elif event.key == pygame.K_SPACE:
                player = player_fly
                meow_sound.play()  # Play meow sound
                fall_speed = -jump_strength  # Apply jump strength to start moving upwards
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player = player_idle  # Change back to idle image when space key is released

    screen.fill((135, 206, 250))  # Set sky blue color

    # Display "Press right to play" text if the game hasn't started
    if not game_started and start_text:
        screen.blit(start_text, text_rect)

    my_font = pygame.font.SysFont('freesansbold', 30)
    Pipes = my_font.render('Pipes:' + str(points), True, (0, 0, 0))
    Score_text = my_font.render('Score:' + str(score), True, (0, 0, 0)) 
    screen.blit(Pipes, (0,0))
    screen.blit(Score_text, (428,0))
   
    if points == 5:
        points = 0
        score += 1
        pipe_speed = random.choice([3, 4, 5, 6, 7])

    # Draw clouds
    for cloud in clouds:
        pygame.draw.circle(screen, PINK, (cloud[0], cloud[1]), cloud_radius)

    # Update cloud positions for scrolling effect
    for i in range(len(clouds)):
        clouds[i] = (clouds[i][0] - pipe_speed, clouds[i][1])
        if clouds[i][0] < -cloud_radius:
            clouds[i] = (screen_width + cloud_radius, clouds[i][1])

    # Draw the scaled player image
    screen.blit(player, (Player_x, Player_y)) 

    Add = max(1, ((points -0.025) // 5) + 0.025)  
    
    # Update player hitbox position
    player_hitbox = pygame.Rect(Player_x, Player_y, player.get_width(), player.get_height())

    # Move the pipe if the game has started
    if game_started:
        start_x -= pipe_speed
        Player_y += fall_speed  # Apply current vertical speed
        fall_speed += gravity 
        # Draw the image at the updated position
        screen.blit(current_image, (start_x, start_y))

        # Update pipe hitbox position
        pipe_hitbox = pygame.Rect(start_x, start_y, image_width, image_height)

        # Check if the current pipe goes off the screen
        if start_x <= -image_width:
            # Spawn a new pipe
            current_image, start_x, start_y = spawn_pipe()
            points += 1
            pipe_speed = pipe_speed + Add

        # Check for collision between player and pipe hitboxes
        if player_hitbox.colliderect(pipe_hitbox):
            # Player hits the pipe, play death sound and end the game
            running = False

        # Check if player touches the top or bottom
        if Player_y <= -90 or Player_y >= screen_height:
            # Player touches the top or bottom, play death sound and end the game
            running = False

    # Update the display
    pygame.display.flip()

    # Delay to control frame rate
    pygame.time.delay(10)

pygame.quit()
  # Apply gravity
 