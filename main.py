import pygame, sys
import numpy as np

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

WIDTH = 700
HEIGHT = 500
BOUNDARY_WIDTH = 10
BOUNDARY_HEIGHT = HEIGHT * 0.8
RECTANGLE_WIDTH = 50
RECTANGLE_HEIGHT = 30
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0)
}


class Boundary(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(COLORS["WHITE"])
        self.image.set_colorkey(COLORS["WHITE"])
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()


class Rectangle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(COLORS["BLACK"])
        self.image.set_colorkey(COLORS["BLACK"])
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.velocity = [speed[0], speed[1]]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = -self.velocity[1]


def main():
    pygame.display.set_caption("SATISFYING SOUNDS")
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill(COLORS["WHITE"])

    boundary_left = Boundary(COLORS["BLACK"], BOUNDARY_WIDTH, BOUNDARY_HEIGHT)
    boundary_left.rect.top = HEIGHT * 0.1
    boundary_left.rect.left = WIDTH * 0.1

    boundary_right = Boundary(COLORS["BLACK"], BOUNDARY_WIDTH, BOUNDARY_HEIGHT)
    boundary_right.rect.top = HEIGHT * 0.1
    boundary_right.rect.right = WIDTH - WIDTH * 0.1

    boundaries = pygame.sprite.Group()
    boundaries.add(boundary_left)
    boundaries.add(boundary_right)


    rectangles = pygame.sprite.Group()
    for i in range(8):
        rec = Rectangle(COLORS["RED"], 50, 30, [2*(i+1), 0])
        rec.rect.left = boundary_left.rect.right + 1
        rec.rect.top = 50 * (i+1)
        rectangles.add(rec)

    pitch_sounds = []
    pitch_sounds.append(pygame.mixer.Sound("pitch_0_minus100.mp3"))
    pitch_sounds.append(pygame.mixer.Sound("pitch_1_minus75.mp3"))
    pitch_sounds.append(pygame.mixer.Sound("pitch_2_minus50.mp3"))
    pitch_sounds.append(pygame.mixer.Sound("pitch_3_minus25.mp3"))
    pitch_sounds.append(pygame.mixer.Sound("pitch_4_original.mp3"))
    pitch_sounds.append(pygame.mixer.Sound("pitch_5_plus25.mp3"))
    pitch_sounds.append(pygame.mixer.Sound("pitch_6_plus50.mp3"))
    pitch_sounds.append(pygame.mixer.Sound("pitch_7_plus75.mp3"))
    pitch_sounds.append(pygame.mixer.Sound("pitch_8_plus100.mp3"))
    # pitch_sounds.reverse()

    clock = pygame.time.Clock()
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            loop = False

        boundaries.update()
        rectangles.update()

        for i, rec in enumerate(rectangles):
            if rec.rect.left <= boundary_left.rect.right:
                rec.rect.left = boundary_left.rect.right + 1
                pitch_sounds[i].play()
                rec.bounce()
            elif rec.rect.right >= boundary_right.rect.left:
                rec.rect.right = boundary_right.rect.left - 1
                pitch_sounds[i].play()
                rec.bounce()

        screen.fill(COLORS["WHITE"])
        boundaries.draw(screen)
        rectangles.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()