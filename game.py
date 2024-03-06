import pygame
import sys
import random
from math import *
 
pygame.init()
 
width = 1750
height = 890
 
# Load the background image
background_image = pygame.image.load("assets\\images\\bg.jpg")
background_image = pygame.transform.scale(background_image, (width, height))
 
# Load the ghost image outside the class
ghost_image = pygame.image.load("assets\\images\\ghost.png")


display = pygame.display.set_mode((width, height))
pygame.display.set_caption("CopyAssignment - ghost Shooter Game")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
 
margin = 100
lowerBound = 100
 
score = 0
 
white = (230, 230, 230)
lightBlue = (4, 27, 96)
red = (231, 76, 60)
lightGreen = (25, 111, 61)
darkGray = (40, 55, 71)
darkBlue = (64, 178, 239)
green = (35, 155, 86)
yellow = (244, 208, 63)
blue = (46, 134, 193)
purple = (155, 89, 182)
orange = (243, 156, 18)
 
font = pygame.font.SysFont("Arial", 25)


# Load the background music
pygame.mixer.music.load("assets\\audio\\Asian-Graveyard-Remastered(chosic.com).mp3")
pygame.mixer.music.play(-1)
 
# Load the sound effect for bursting ghosts
burst_sound = pygame.mixer.Sound("assets\\audio\\scary-scream-193752.mp3")
 
# Fonts
instruction_font = pygame.font.Font(None, 30)
heading_font = pygame.font.Font(None, 50)

def instructions():
    instruction_text = [
        "Instructions:",
        "1. Use your mouse to aim and click to shoot ghosts.",
        "2. Burst as many ghosts as you can before they reach the top.",
        "3. Avoid hitting the lower platform or missing ghosts.",
        "4. Press 'Q' to quit the game.",
        "5. Press 'R' to restart the game.",
        "6. Have fun!",
        "",
        "Click anywhere to start the game."
    ]
   
    y_offset = 50
    for line in instruction_text:
        text = instruction_font.render(line, True, white)
        text_rect = text.get_rect(center=(width/2, y_offset))
        display.blit(text, text_rect)
        y_offset += 40
 
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def show_prompt():
    text = font.render("Do you want to continue? (Y/N)", True, (255, 255, 255))
    display.blit(text, (50, 50))
    pygame.display.flip()
 
class ghost:
    def __init__(self, speed, ghost_image):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed = -speed
        self.proPool= [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.ghost_image = ghost_image
       
    def move(self):
        direct = random.choice(self.proPool)
 
        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10
 
        self.y += self.speed*sin(radians(self.angle))
        self.x += self.speed*cos(radians(self.angle))
 
        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height/5:
                self.x -= self.speed*cos(radians(self.angle))
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()
           
    def show(self):
        ghost_rect = self.ghost_image.get_rect(center=(self.x + self.a, self.y + self.b))
        display.blit(self.ghost_image, ghost_rect)
           
    def burst(self):
        global score
        pos = pygame.mouse.get_pos()
 
        if isonghost(self.x, self.y, self.a, self.b, pos):
            score += 1
            # Play burst sound
            burst_sound.play()
            self.reset()
               
    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed -= 0.002
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
       

 
# Create ghosts with the same ghost image
ghosts = []
noghost = 10
for i in range(noghost):
    obj = ghost(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]), ghost_image)
    ghosts.append(obj)
 
def isonghost(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    else:
        return False
   
def pointer():
    pos = pygame.mouse.get_pos()
    r = 25
    l = 20
    color = lightGreen
    for i in range(noghost):
        if isonghost(ghosts[i].x, ghosts[i].y, ghosts[i].a, ghosts[i].b, pos):
            color = red
    pygame.draw.ellipse(display, color, (pos[0] - r/2, pos[1] - r/2, r, r), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] - l/2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(display, color, (pos[0] + l/2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + l/2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(display, color, (pos[0] - l/2, pos[1]), (pos[0] - l, pos[1]), 4)
 

def lowerPlatform():
    pygame.draw.rect(display, darkGray, (0, height - lowerBound, width, lowerBound))
   

def showScore(lvl, start_time):
    scoreText = font.render(f"Ghosts Bursted : " + str(score), True, white)
    display.blit(scoreText, (150, height - lowerBound + 50))

    scoreText1 = font.render(f"Current Level : {lvl}", True, white)
    display.blit(scoreText1, (450, height - lowerBound + 50))

    lvl_no = int(lvl[len(lvl)-1])

    if lvl_no==1:
        scoreText2 = font.render(f"Tips: Hit {int(lvl[len(lvl)-1]) * 15 * 1} ghosts", True, white)
        display.blit(scoreText2, (750, height - lowerBound + 50))
    elif lvl_no==2:
        scoreText2 = font.render(f"Tips: Hit {int(lvl[len(lvl)-1]) * 15 * 1} ghosts", True, white)
        display.blit(scoreText2, (750, height - lowerBound + 50))
    else:
        scoreText2 = font.render(f"Tips: Hit {int(lvl[len(lvl)-1]) * 15 * 4} ghosts", True, white)
        display.blit(scoreText2, (750, height - lowerBound + 50))

    elapsed_seconds = count_seconds(start_time)
        
    seconds_text = font.render("Elapsed Seconds: " + str(elapsed_seconds), True, white)

    # print(elapsed_seconds)

    display.blit(seconds_text, (990, height - lowerBound + 50))

    pygame.display.update()
    clock.tick(60)


    
   
def close():
    pygame.quit()
    sys.exit()

def display_prompt():
    display.fill((255, 255, 255))  # Fill the screen with white



    prompt_text = font.render("You won , keep it up ghost hunter !!", True, (0, 0, 0))
    display.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, height // 2 - prompt_text.get_height() // 2))
    pygame.display.update()


    prompt2_text = font.render("Go to next level ? (yes/no)", True, (0, 0, 0))
    display.blit(prompt2_text, (width // 2 - prompt2_text.get_width() // 2, height // 2 + 20 - prompt2_text.get_height() // 2))
    pygame.display.update()


def display_confirmation():
    display.fill((255, 255, 255))  # Fill the screen with white


    prompt_text = font.render("You Loose , better luck next time !!", True, (0, 0, 0))
    display.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, height // 2 - prompt_text.get_height() // 2))
    pygame.display.update()


    prompt2_text = font.render("Do you wish to continue ? (yes/no)", True, (0, 0, 0))
    display.blit(prompt2_text, (width // 2 - prompt2_text.get_width() // 2, height // 2 + 20 - prompt2_text.get_height() // 2))
    pygame.display.update()



def show_confirmation():
    waiting_for_input = True

    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting_for_input = False
                    return True
                elif event.key == pygame.K_n:
                    waiting_for_input = False
                    return False

        display_confirmation()
        pygame.time.delay(50)  # Adjust delay as needed
        clock.tick(60)

def get_yes_no_input():
    waiting_for_input = True

    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting_for_input = False
                    return True
                elif event.key == pygame.K_n:
                    waiting_for_input = False
                    return False

        display_prompt()
        pygame.time.delay(50)  # Adjust delay as needed
        clock.tick(60)

def count_seconds(start_time):
    current_time = pygame.time.get_ticks()
    elapsed_seconds = (current_time - start_time) // 1000
    return elapsed_seconds

def game(lvl):

    global score
    loop = True
    
    start_time = pygame.time.get_ticks()
    

    while loop:


        elapsed_seconds = count_seconds(start_time)
        
        seconds_text = font.render("Elapsed Seconds: " + str(elapsed_seconds), True, (0, 0, 0))

        print(elapsed_seconds)

        # display.blit(seconds_text, (width // 2 - seconds_text.get_width() // 2, height // 2 - seconds_text.get_height() // 2))

        # pygame.display.update()
        # clock.tick(60)

        if score > 15 and lvl==1 and elapsed_seconds < 60:
            
            score = 0

            lvl = lvl + 1

            start_time = pygame.time.get_ticks()

            response = get_yes_no_input()

            if response:
                print("User chose: Yes")
            else:
                print("User chose: No")
                sys.exit()

        elif score < 15 and lvl==1 and elapsed_seconds > 60:
            
            response = show_confirmation()

            if response:
                print("User chose: Yes")
                game()
            else:
                print("User chose: No")
                sys.exit()

        elif score > 30 and lvl == 2 and elapsed_seconds < 60:
            
            score = 0

            lvl = lvl + 1

            start_time = pygame.time.get_ticks()

            response = get_yes_no_input()

            if response:
                print("User chose: Yes")
            else:
                print("User chose: No")
                sys.exit()

        elif score < 30 and lvl==2 and elapsed_seconds > 60:
            
            response = show_confirmation()

            if response:
                print("User chose: Yes")
                game()
            else:
                print("User chose: No")
                sys.exit()
        elif score > 60 and lvl == 3 and elapsed_seconds < 60:
            
            score = 0

            lvl = lvl + 1

            start_time = pygame.time.get_ticks()

            response = get_yes_no_input()

            if response:
                print("User chose: Yes")
            else:
                print("User chose: No")
                sys.exit()

        elif score < 60 and lvl==3 and elapsed_seconds > 60:
            
            response = show_confirmation()

            if response:
                print("User chose: Yes")
                game()
            else:
                print("User chose: No")
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    score = 0
                    game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        print("Wish to continue 'Yes'")
                        continue  # Exit the loop or perform other actions for 'Yes'
                    elif event.key == pygame.K_n:
                        print("Quit 'No'")
                        loop = False  # Exit the loop or perform other actions for 'No'

 
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(noghost):
                    ghosts[i].burst()
 
        # Draw the background image
        display.blit(background_image, (0, 0))
       
        for i in range(noghost):
            ghosts[i].show()
 
        pointer()
       
        for i in range(noghost):
            ghosts[i].move()
 
       
        lowerPlatform()
        showScore(f'Level {lvl}', start_time)
        pygame.display.update()
        clock.tick(60)
       
# game()


if __name__=="__main__":

    instructions()
    game(1)

    

    