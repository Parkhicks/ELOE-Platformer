# intial Code from https://docs.replit.com/tutorials/python/2d-platform-game
import pygame, numpy # How to install numpy? I need to find out so I can add to the README

WIDTH = 400
HEIGHT = 300
BACKGROUND = (0, 0, 0)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("./Assets/p1_front.png", startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("./assets/p1_front.png")

        self.walk_cycle = [pygame.image.load(f"./assets/p1_walk{i:0>2}.png") for i in range(1,12)]
        self.animation_index = 0
        self.facing_left = False

        self.speed = 4
        self.jumpspeed = 20
        self.vsp = 0
        self.gravity = 1
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, boxes):
        hsp = 0
        onground = self.check_collision(0, 1, boxes)
        # check keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            hsp = self.speed
        else:
            self.image = self.stand_image

        if key[pygame.K_UP] and onground:
            self.vsp = -self.jumpspeed

        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = key

        # gravity
        if self.vsp < 10 and not onground:  # 9.8 rounded up
            self.jump_animation()
            self.vsp += self.gravity

        if onground and self.vsp > 0:
            self.vsp = 0

        # movement
        self.move(hsp, self.vsp, boxes)

    def move(self, x, y, boxes):
        dx = x
        dy = y

        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])

    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        self.rect.move_ip([-x, -y])
        return collide
    
class Enemy(Sprite):
    def __init__(self, startx, starty, width = 50, height = 50):
        super().__init__("./Assets/enemy_sprite.png", startx, starty)
        self.image = pygame.transform.scale(self.image, (width,height))
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left

    def update(self, boxes):
        self.rect.x += self.speed * self.direction
        # Reverse direction if reaching boundaries
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1
        
        collision_list = pygame.sprite.spritecollide(self, boxes, False)
        for box in collision_list:
            # Collision handling
            # For example, you can change the enemy's direction upon collision
            self.direction *= -1  # Reverse direction


class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("./assets/box.png", startx, starty)

        
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, 200)

    enemies = pygame.sprite.Group()
    enemy = Enemy(200, 100)
    enemies.add(enemy)

    boxes = pygame.sprite.Group()
    for bx in range(0, 400, 70):
        boxes.add(Box(bx, 300))

    boxes.add(Box(330, 230))
    boxes.add(Box(100, 70))

    while True:
        pygame.event.pump()
        player.update(boxes)
        enemy.update(boxes)

        # Draw loop
        screen.fill(BACKGROUND)
        player.draw(screen)
        enemies.draw(screen)
        boxes.draw(screen)
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()