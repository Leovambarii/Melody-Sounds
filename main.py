import pygame, sys

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

WIDTH = 500
HEIGHT = 350
BOUNDARY_WIDTH = 10
BOUNDARY_HEIGHT = 285
RECTANGLE_WIDTH = 50
RECTANGLE_HEIGHT = 30
COLORS = {
    "RECT_1": (179, 0, 0),
    "RECT_2": (204, 0, 0),
    "RECT_3": (230, 0, 0),
    "RECT_4": (255, 0, 0),
    "RECT_5": (255, 26, 26),
    "RECT_6": (255, 51, 51),
    "RECT_7": (255, 77, 77),
    "RECT_8": (255, 102, 102),
    "PINK": (255, 230, 230),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
}
COLOR_RECT_NAMES = ["RECT_1", "RECT_2", "RECT_3", "RECT_4", "RECT_5", "RECT_6", "RECT_7", "RECT_8"]

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
    screen.fill(COLORS["PINK"])

    boundary_left = Boundary(COLORS["BLACK"], BOUNDARY_WIDTH, BOUNDARY_HEIGHT)
    boundary_left.rect.top = 23
    boundary_left.rect.left = 40

    boundary_right = Boundary(COLORS["BLACK"], BOUNDARY_WIDTH, BOUNDARY_HEIGHT)
    boundary_right.rect.top = 23
    boundary_right.rect.right = WIDTH - 40

    boundaries = pygame.sprite.Group()
    boundaries.add(boundary_left)
    boundaries.add(boundary_right)


    rectangles = pygame.sprite.Group()
    rect_height = 28
    for i in range(8):
        rec = Rectangle(COLORS[COLOR_RECT_NAMES[i]], 50, 30, [1+i, 0])
        rec.rect.left = boundary_left.rect.right + 1
        rec.rect.top = rect_height
        rect_height += 35
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

        pygame.display.update()
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

        screen.fill(COLORS["PINK"])
        boundaries.draw(screen)
        rectangles.draw(screen)
        line_height = 25
        for i in range(9):
            pygame.draw.line(screen, (0, 0, 0), (50, line_height), (WIDTH-50, line_height), 5)
            line_height += 35
        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()