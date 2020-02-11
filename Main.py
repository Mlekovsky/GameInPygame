import pygame
#Basic initialization
pygame.init()

screenWidth = 500
screenHeight = 480

win = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Pygame game!")

#Loading textures
walkRight = [pygame.image.load('Resources/R1.png'), pygame.image.load('Resources/R2.png'), pygame.image.load('Resources/R3.png'), pygame.image.load('Resources/R4.png'), pygame.image.load('Resources/R5.png'), pygame.image.load('Resources/R6.png'), pygame.image.load('Resources/R7.png'), pygame.image.load('Resources/R8.png'), pygame.image.load('Resources/R9.png')]
walkLeft = [pygame.image.load('Resources/L1.png'), pygame.image.load('Resources/L2.png'), pygame.image.load('Resources/L3.png'), pygame.image.load('Resources/L4.png'), pygame.image.load('Resources/L5.png'), pygame.image.load('Resources/L6.png'), pygame.image.load('Resources/L7.png'), pygame.image.load('Resources/L8.png'), pygame.image.load('Resources/L9.png')]
bg = pygame.image.load('Resources/bg.jpg')
char = pygame.image.load('Resources/standing.png')

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):       
            if self.left:
                win.blit(walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1    
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


#Basic variables to optimalize later
clock = pygame.time.Clock()

def redrawGameWindow():
    win.blit(bg, (0,0))      
    mainPlayer.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()  

#Initialize objects
mainPlayer = player(300, 410, 64, 64)
bullets = []
run = True

while run:
    clock.tick(27)
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.remove(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if(mainPlayer.left):
            facing = -1
        else:   
            facing = 1 

        if len(bullets) < 5:
            bullets.append(projectile(round(mainPlayer.x + mainPlayer.width //2), round(mainPlayer.y + mainPlayer.height //2), 6, (0,0,0), facing))

    if keys[pygame.K_LEFT] and mainPlayer.x > mainPlayer.vel:
        mainPlayer.x -= mainPlayer.vel
        mainPlayer.left = True
        mainPlayer.right = False
        mainPlayer.standing = False
    elif keys[pygame.K_RIGHT] and mainPlayer.x < screenWidth - mainPlayer.width - mainPlayer.vel:    
        mainPlayer.x += mainPlayer.vel
        mainPlayer.right = True
        mainPlayer.left = False
        mainPlayer.standing = False
    else:
        mainPlayer.standing = True
        mainPlayer.walkCount = 0

    if not(mainPlayer.isJump):    
        if keys[pygame.K_UP]:
            mainPlayer.isJump = True
            mainPlayer.walkCount = 0
    else:
        if mainPlayer.jumpCount >= -10:
            neg = 1
            if mainPlayer.jumpCount < 0:
                neg = -1
            mainPlayer.y -= (mainPlayer.jumpCount ** 2) * 0.5 * neg
            mainPlayer.jumpCount -= 1
        else:
            mainPlayer.isJump = False
            mainPlayer.jumpCount = 10          

    redrawGameWindow()

pygame.quit()            
