# Taylor Sayson
# 13 May 2024
# Block B

import pygame as pg

# --CONSTANTS--
# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
EMERALD = (21, 219, 147)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 177)
GRAY = (128, 128, 128)
ORANGE = (245, 93, 5)
GREEN = (0, 163, 69)
WIDTH = 1280
HEIGHT = 720
SCREEN_SIZE = (WIDTH, HEIGHT)


# Import and scale images
RIMIMAGE = pg.image.load("./Images/frontnet.png")
RIM = pg.transform.scale(RIMIMAGE, (RIMIMAGE.get_width() // 3, RIMIMAGE.get_height() // 3))
BACKRIM = pg.image.load("./Images/backnet.png")
BACK = pg.transform.scale(BACKRIM, (BACKRIM.get_width() // 3, BACKRIM.get_height() // 3))
BACKGROUND = pg.image.load("./Images/gymbackground.png")
# CREATE RIM CLASS
class Rim(pg.sprite.Sprite):
    def __init__(self, x, rim:pg.sprite.Group = None):
        super().__init__()

        self.image = RIM
        self.rect = self.image.get_rect()
        self.rim_sprites = rim
        
        # Rim location
        self.rect.centerx = x
        self.rect.y = 210
        self.ground = 680

class Back(pg.sprite.Sprite):
    def __init__(self,x, back:pg.sprite.Group = None):
        super(). __init__()
        self.image = BACK
        self.rect= self.image.get_rect()
        self.all_sprites = back
        self.rect.centerx= x
        self.rect.y = 210

# CREATE BALL CLASS
class Ball(pg.sprite.Sprite):
    def __init__(self, players:pg.sprite.Group = None, rims:pg.sprite.Group = None):
        super().__init__()
        
        # Draw ball
        self.image = pg.Surface((50,50))
        self.image.set_colorkey(BLACK)
        pg.draw.circle(self.image, ORANGE, (25,25), 25)

        # Ball initial position and velocity
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, 450)
        self.vel_x = 0
        self.vel_y = -20

        # Define
        self.player_sprites = players
        self.rim_sprites = rims
        self.hold = None
        self.basket= None
        self.dribble = False
        self.vertical_direction = 1
        self.scorea = 0
        self.scoreb = 0
        self.count = False
        self.net = False
        self.net2 = False
        self.shotx = 10
        self.shoty = -16
        
        # If player has ball, jumps and does not release ball, ball will auto release just prior to player lands on ground
        # However, if player catches the ball while already in air, disable auto release. Define when shot is loaded or not
        self.shotloaded = False
        
        # When player lets go of ball to shoot, they contact the ball immediately and grab the ball again
        # Say when player is colliding with the ball after picking it up, or if they are colliding with ball because they just shot it
        self.reshot = False
        

    def update(self):  
        # Collisions between ball and player, and ball and rim
        collided = pg.sprite.spritecollide(self, self.player_sprites, False)
        scored = pg.sprite.spritecollide(self, self.rim_sprites, False )

        # If ball and player collide and reshot is False, self.hold is the first player collision
        if collided and self.reshot == False:
            self.hold = collided[0]  

        # When is the ball contacted with the rim
        if scored:
            self.basket = scored[0]
        elif not scored:
            self.basket = None
        
        # Location above rim
        if self.rect.centerx<=140 and self.rect.centery<= 210 or self.rect.centerx>= 1130 and self.rect.centery<=210:
            self.count = True
            self.net = True
            self.net2 = True
        if self.rect.left> 140 and self.rect.right<1130:
            self.count = False
        if self.rect.top>300:
            self.net2= False

        if self.net2 == False:
            self.net =False
        
        
        if self.basket:
            # If the ball is being held by a player and also hits the rim, make player drop ball
            if self.hold:
                self.hold = None
                self.reshot = True
                self.vel_y = 0.8
                self.shooting = 0    

            #if ball rim is the right rim
            if self.basket.rect.centerx ==1205:
                if self.vel_y >0 and self.basket.rect.top +15>self.rect.bottom:
                    if self.rect.right > 1265 or (self.rect.left<self.basket.rect.left):
                        # self.rect.bottom = self.rect.top # if clipping happens, comment this out
                        self.vel_y *= -1       
                        self.vel_x -= .1        
                #If ball hits top rim on edges, bounce off
                if self.vel_x > 0 and self.rect.right > self.basket.rect.left and self.rect.centerx < self.basket.rect.left and self.rect.top <self.basket.rect.top + 16 and self.rect.bottom > self.basket.rect.top + 16:
                    self.rect.right = self.basket.rect.left
                    self.vel_x *= -1
                    
                # If ball hits bottom, rim bounce 
                if self.vel_y < 0 and self.basket.rect.top <self.rect.top < self.basket.rect.top + 20:
                    self.rect.top = self.basket.rect.top +20
                    self.vel_y *= -1
                
                # If ball goes in slow down
                elif self.vel_y > 0 and self.rect.top> self.basket.rect.top and self.net == True:
                    self.rect.centerx= self.basket.rect.centerx
                    self.vel_x=0
                    self.vel_y = max(self.vel_y /1.2, 1.3)
                    if self.count == True:
                        self.scorea += 1
                        self.count = False
                
            #if ball rim is the left rim  
            elif self.basket.rect.centerx ==75:
                if self.vel_y> 0 and self.basket.rect.top + 15 >self.rect.bottom:
                    if self.rect.left < 15 or (self.rect.right> self.basket.rect.right):
                        self.rect.bottom = self.basket.rect.top
                        self.vel_y *= -1
                        self.vel_x += .1
                #If ball hits top rim on edges, bounce off
                if self.vel_x < 0 and self.rect.left < self.basket.rect.right and self.rect.centerx > self.basket.rect.right and self.rect.top <self.basket.rect.top + 16 and self.rect.bottom > self.basket.rect.top + 16:
                    self.rect.left = self.basket.rect.right
                    self.vel_x *= -1
                # If ball hits bottom, rim bounce
                if self.vel_y < 0 and self.basket.rect.top <self.rect.top < self.basket.rect.top + 20:
                    self.rect.top = self.basket.rect.top +20
                    self.vel_y *= -1
                 # If ball goes in slow down   
                elif self.vel_y > 0 and self.rect.top> self.basket.rect.top and self.net == True:
                    self.rect.centerx= self.basket.rect.centerx
                    self.vel_x=0
                    self.vel_y = max(self.vel_y /1.2, 1.3)
                    if self.count == True:
                        self.scoreb += 1
                        self.count = False            

        # Player has to touch the ground with the ball for shot to be loaded
        # Once ball is no longer being held, shot is unloaded
        if self.hold and self.hold.rect.bottom == 680:
            self.shotloaded = True
        if not self.hold:
            self.shotloaded = False

        # Once ball is no longer contacted by player, set reshot to False
        if not collided:
            self.reshot = False         

        # If ball and player collide
        if self.hold:
            self.hold.shooting = 1
            pressed = pg.key.get_pressed()
            # Make ball follow player if on ground
            if self.hold.rect.bottom == 680:
        
                # follow on right side of player if player is moving right, left side if player moving left
                if self.hold.vel_x>0:
                    self.rect.left = self.hold.rect.right -15
                elif self.hold.vel_x < 0:
                    self.rect.right = self.hold.rect.left +15
                # If player is not moving, face ball towards the hoop they are shooting on
                elif self.hold.vel_x ==0:
                    if self.hold.initial == 500:
                        self.rect.left = self.hold.rect.right -15
                    if self.hold.initial == 780:
                        self.rect.right = self.hold.rect.left +15
                    
                # Make player dribble ball if on ground
                if self.rect.y <= 590:
                    self.vertical_direction = 1
                elif self.rect.y >= 630:
                    self.vertical_direction = -1
                self.rect.y += 4 * self.vertical_direction
               

            pressed = pg.key.get_pressed()
            # If player is about to land with the ball and shot is loaded, release ball to prevent travellling rule
            if self.hold.rect.bottom > 650 and self.hold.vel_y > 0 and self.shotloaded:
                if self.hold.initial == 500:
                    self.hold.shooting=0
                    self.hold = None
                    self.vel_x = self.shotx
                    self.vel_y = self.shoty
                elif self.hold.initial == 780:
                    self.hold.shooting=0
                    self.hold = None
                    self.vel_x = -self.shotx
                    self.vel_y = self.shoty
            

            # Set reshot to True if they shoot 
            elif self.hold.rect.bottom == 680 and not pressed[self.hold.input["up"]] and self.shotloaded:
                self.reshot = True

            
            # Any instance player is in air, position ball in shooting position
            elif (self.hold.rect.bottom < 680 and pressed[self.hold.input["up"]]) or (self.hold.rect.bottom < 680 and not self.shotloaded) :
                    self.rect.bottom = self.hold.rect.top + 23
                    if self.hold.initial == 500:
                        self.rect.left = self.hold.rect.right -35
                    if self.hold.initial == 780:
                        self.rect.right = self.hold.rect.left +35
      
            # If they are in air with shot loaded, and up input is no longer pressed, shoot ball
            else:
                    if self.shotloaded:
                        if self.hold.initial == 500:
                            self.hold.shooting=0
                            self.hold = None
                            self.vel_x = self.shotx
                            self.vel_y = self.shoty
                            
                        elif self.hold.initial == 780:
                            self.hold.shooting=0
                            self.hold = None
                            self.vel_x = -self.shotx
                            self.vel_y = self.shoty
                            
        # Set ball physics when not being affected by other sprites
        else:
            # Keep in the borders
            if self.rect.bottom > 680:
                self.rect.bottom = 680
                self.vel_y *= -1
            if self.rect.left < 0:
                self.rect.left = 0
                self.vel_x *= -1
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                self.vel_x *= -1

            # Gravity
            if self.vel_y >=0:
                self.vel_y = self.vel_y + .5
            if self.vel_y <0:
                self.vel_y = self.vel_y + .65
                
            # Stop ball from having lots of very small bounces
            if -0.5<self.vel_y<0.5 and self.rect.bottom >= 680:
                self.vel_y *=0

            # Horizontal friction/deceleration
            if self.vel_x >1:
                self.vel_x = max(self.vel_x - .017, 0)
            elif self.vel_x <1:
                self.vel_x = min(self.vel_x + .017, 0)
            elif self.vel_x > 0:
                self.vel_x = max(self.vel_x - .005, 0)
            elif self.vel_x < 0:
                self.vel_x = min(self.vel_x + .005, 0)
            
            
            # Ball follows velocity
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y


class Player(pg.sprite.Sprite):
    def __init__(self, color, input, x, y):
        super().__init__()

        # Draw a player
        self.image = pg.Surface((90, 90))
        self.image.set_colorkey(BLACK)
        pg.draw.circle(self.image, color, (45, 45), 45)

        # Player initial position and velocity
        self.rect = self.image.get_rect()
        self.initial = x
        self.rect.centerx = x
        self.rect.centery = y
        self.vel_x = 0
        self.vel_y = 0
        # Refer on up, down, left, right inputs
        self.input = input
        self.shooting = 0

    def update(self):
        # Move player
        
        # Define key presses
        pressed = pg.key.get_pressed()
        
        # If player is on ground, accelerate, top velocity of 8/-8
        if pressed[self.input["left"]] and self.vel_y==0:
            self.vel_x = max(self.vel_x - .8, -8)
        elif pressed[self.input["right"]]and self.vel_y==0:
            self.vel_x = min(self.vel_x + .8, 8)
        # If player is in the air, top velocity of 3/-3
        elif pressed[self.input["left"]]:
            self.vel_x = max(self.vel_x - 3, -3)
        elif pressed[self.input["right"]]:
            self.vel_x = min(self.vel_x + 3, 3)
        #Deceleration
        else:
            if self.vel_x >0:
                self.vel_x = max(self.vel_x - 1, 0)
            elif self.vel_x <0:
                self.vel_x = min(self.vel_x + 1, 0)

        # Vertical movement
        # If up input pressed and player is going up set y velocity to make player jump, limit max height when player can input jump        
        if pressed[self.input["up"]] and self.vel_y<=0 and self.rect.bottom > 570 and self.shooting ==1:
            self.vel_y = -16
        elif pressed[self.input["up"]] and self.vel_y<=0 and self.rect.bottom > 480 and self.shooting ==0:
            self.vel_y = -16

        # Gravity
        else:
            self.vel_y = self.vel_y + .7
            
        # Player follows velocity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Keep player within screen bounds
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel_x = 0
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.bottom > 680:
            self.rect.bottom = 680
            self.vel_y = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0

# Create wait function until space bar pressed to begin game
def wait():
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    waiting = False
        
def start():
    """Environment Setup and Game Loop"""
    pg.init()

    # --Game State Variables--
    screen = pg.display.set_mode(SCREEN_SIZE)
    done = False
    clock = pg.time.Clock()
    font = pg.font.SysFont("Futura", 30)
    font2 = pg.font.SysFont("Futura", 60)
    font3 = pg.font.SysFont("Futura", 22)
    font4 = pg.font.SysFont("Futura", 17)
    # Game Title
    pg.display.set_caption("1v1 Hoops")
    #Game instructions
    title = font2.render("WELCOME TO 1v1 Hoops", True, WHITE)
    p1controls = font4.render("PLAYER 1 CONTROLS - MOVE LEFT: 'A', MOVE RIGHT: 'D', JUMP/BLOCK/INITIATE SHOT: 'W', SHOOT: release 'W'", True, WHITE)
    p2controls = font4.render("PLAYER 2 CONTROLS - MOVE LEFT: 'left' key, MOVE RIGHT: 'right' key, JUMP/BLOCK/INITIATE SHOT: 'up' key, SHOOT: release 'up' key", True, WHITE)
    startcommand = font3.render("Press SPACEBAR to begin!", True, WHITE)
    screen.blit(title, (50, 100))
    screen.blit(p1controls, (50, 300))
    screen.blit(p2controls, (50, 340))
    screen.blit(startcommand, (50, 475))
    pg.display.flip()

    # Wait for key press to start the game
    wait()

    # All sprites go in this sprite Group
    all_sprites = pg.sprite.Group()
    player_sprites = pg.sprite.Group()
    rim_sprites = pg.sprite.Group()
    
    # Create Player sprite objects
    player = Player(BLUE, {'left': pg.K_LEFT, 'right': pg.K_RIGHT, 'up': pg.K_UP, 'down': pg.K_DOWN}, 780, 720)
    player2 = Player(GREEN, {'left': pg.K_a, 'right': pg.K_d, 'up': pg.K_w, 'down': pg.K_s}, 500, 720)
    player_sprites.add(player)
    player_sprites.add(player2)

    # Create Rim objects
    rim1 = Rim(75, rim_sprites)
    rim2 = Rim(1205, rim_sprites)
    rim_sprites.add(rim1)
    rim_sprites.add(rim2)

    # Create Ball objects
    ball = Ball(player_sprites, rim_sprites)
    back1 = Back(75, all_sprites)
    back2 = Back(1205, all_sprites)

    # Add sprites, order them layered
    all_sprites.add(player)
    all_sprites.add(player2)
    all_sprites.add(back1)
    all_sprites.add(back2)
    all_sprites.add(ball)
    all_sprites.add(rim1)
    all_sprites.add(rim2)    

    # --Main Loop--
    while not done:
        # --- Event Listener
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        all_sprites.update()

        # --- Draw items
        screen.blit(BACKGROUND, (0,0))
        all_sprites.draw(screen)

        #score bug
        scorea = font.render(f"PLAYER 1: {ball.scorea}", True, GREEN)
        scoreb = font.render(f"PLAYER 2: {ball.scoreb}", True, BLUE)
        wincon = font3.render("First to 11 wins", True, WHITE)
        screen.blit(scorea, ((WIDTH// 2 -235), 30))
        screen.blit(scoreb, ((WIDTH//2 +45), 30))
        screen.blit(wincon, (WIDTH//2-80, 5))

        #win screen words
        winscreen1 = font2.render("PLAYER 1 WINS!", True, GREEN)
        winscreen2 = font2.render("PLAYER 2 WINS!", True, BLUE)


        #win condition 11 points
        if ball.scorea >=11:
            screen.blit(winscreen1, (WIDTH//2 -250, HEIGHT//2-150))
            ball.count = False

        if ball.scoreb >=11:
            screen.blit(winscreen2, (WIDTH//2- 250, HEIGHT//2-150))
            ball.count = False

        # Update the screen with anything new
        pg.display.flip()

        # --- Tick the Clock
        clock.tick(60)  # 60 fps

    pg.quit()

def main():

    start()

if __name__ == "__main__":
    main()
