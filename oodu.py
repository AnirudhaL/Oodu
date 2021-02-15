import pygame

pygame.init()

jump_music = pygame.mixer.Sound('Slam_Mid_02.wav')
pygame.mixer.music.load("TheSummit.wav")
vol = pygame.mixer.music.get_volume()

win = pygame.display.set_mode((800, 550))

pygame.display.set_caption("Oodu Sina")


run1 = [pygame.image.load('Layer 3.png'), pygame.image.load('Layer 4.png'), pygame.image.load('Layer 5.png'),
        pygame.image.load('Layer 6.png'), pygame.image.load('Layer 7.png'), pygame.image.load('Layer 8.png'),
        pygame.image.load('Layer 9.png'), pygame.image.load('Layer 10.png'), pygame.image.load('Layer 11.png'),
        pygame.image.load('Layer 12.png'), pygame.image.load('Layer 13.png'), pygame.image.load('Layer 14.png'),
        pygame.image.load('Layer 15.png')]
run2 = []
run = []
for i in run1:
    run2.append(pygame.transform.flip(i, True, False))
for i in run2:
    run.append(pygame.transform.smoothscale(i, (175, 100)))
bg = pygame.image.load("bg.png")
ka = pygame.image.load("katte.png")
base = pygame.image.load("base.png")

icon_img = pygame.image.load("icon_image.png")
pygame.display.set_icon(icon_img)

clock = pygame.time.Clock()
re_score = 0
ac = (0, 255, 255)
ic = (150, 255, 255)
pause = False
sco = 0
VEL = 15
fontz = "cambria"


class Runner:

    def __init__(self, x, y):
        self.jumpCount = 10
        self.isJump = False
        self.x = x
        self.y = y
        self.r_count = 60
        self.standing = True
        self.speed = 1
        self.imgs = run[0]
        self.run = run

    def draw(self):
        if self.r_count + 1 >= 13:
            self.r_count = 0
        if self.standing:
            win.blit(self.run[self.r_count//self.speed], (self.x, self.y))
            self.r_count += 1
        if self.r_count >= 13:
            self.r_count = 0

    def get_mask(self):
        return pygame.mask.from_surface(self.imgs)


class Pipe:

    global VEL
    global sco

    ze = 0
    p = 0

    if p >= 50:
        VEL = 20
    if p >= 100:
        VEL = 30

    def __init__(self, width, height, x):
        self.x = x
        self.width = width
        self.height = height
        self.height = 50
        self.bottom = 0
        self.katte = ka
        self.passed = False
        self.set_height()
        self.katte_mask = None

    def set_height(self):
        self.height = 50
        self.bottom = 480 - self.height

    def move(self):
        self.x -= VEL
        if self.x <= 0:
            self.x = 800
            self.p += 5

    def sc(self):
        global re_score
        if re_score == 1:
            self.p = 0
            re_score = 0
        return self.p

    def draw(self):
        self.katte = pygame.transform.scale(self.katte, (30, 50))
        win.blit(self.katte, (self.x, self.bottom))

    def collide(self, man):
        man_mask = man.get_mask()
        pipe_mask = pygame.mask.from_surface(self.katte)
        offset = (self.x - man.x, self.bottom - round(man.y))
        b_point = man_mask.overlap(pipe_mask, offset)
        if b_point:
            pygame.mixer.Sound.play(jump_music)
            return True
        return False


class Base:
    global VEL, sco
    
    if sco >= 50:
        VEL = 20
    if sco >= 100:
        VEL = 30
    
    WIDTH = base.get_width()
    IMG = base

    def __init__(self, y):

        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        self.x3 = self.WIDTH + self.WIDTH
        self.x4 = self.x3 + self.WIDTH
        self.x5 = 800

    def move(self):
        self.x1 -= VEL
        self.x2 -= VEL
        self.x3 -= VEL
        self.x4 -= VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x4 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

        if self.x3 + self.WIDTH < 0:
            self.x3 = self.x2 + self.WIDTH

        if self.x4 + self.WIDTH < 0:
            self.x4 = self.x3 + self.WIDTH

        if sco % 50 == 0 and sco > 0 and not pipe.collide(cat):
            font = pygame.font.SysFont(fontz, 30)
            text = font.render('INEN AYTALLA', 1, (0, 0, 0))
            win.blit(text, (320, 510))

        if sco % 100 == 0 and sco > 0 and not pipe.collide(cat):
            large_text = pygame.font.SysFont(fontz, 40, True)
            text_surf, text_rect = test_object("BENKI GURU NEENU", large_text)
            text_rect = (260, (win.get_height() // 3))
            win.blit(text_surf, text_rect)

    def draw(self):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        win.blit(self.IMG, (self.x3, self.y))
        win.blit(self.IMG, (self.x4, self.y))


def test_object(text, fonts):
    text = str(text)
    text_surface = fonts.render(text, False, (0, 0, 0))
    return text_surface, text_surface.get_rect


def button(mes, x, y, w, h, active, inactive, text_x, action=None, font_size=26):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if w + x > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(win, active, (x, y, w, h), 5)
    else:
        pygame.draw.rect(win, inactive, (x, y, w, h))

    large_text = pygame.font.SysFont(fontz, font_size)
    text_surf, text_rect = test_object(mes, large_text)
    text_rect = (text_x, 328)
    win.blit(text_surf, text_rect)

    if w + x > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1 and action is not None:
            action()


def un_paused():
    global pause
    pause = False


def paused():

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        large_text = pygame.font.SysFont(fontz, 100, True)
        text_surf, text_rect = test_object("PAUSED", large_text)
        text_rect = (230, (win.get_height() // 3))
        win.blit(text_surf, text_rect)

        large_text = pygame.font.SysFont(fontz, 28)
        text_surf, text_rect = test_object("YAKE? EN AYTU?", large_text)
        text_rect = (320, 510)
        win.blit(text_surf, text_rect)

        button("Continue!", 140, 320, 150, 50, ac, ic, 156, un_paused)
        button("SAAKA?", 556, 320, 100, 50, ac, ic, 565, quit_game, 23)

        pygame.display.update()


def game_intro(p, q, w):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(bg, (0, 0))
        BASE.draw()
        large_text = pygame.font.SysFont(fontz, 80, True)
        text_surf, text_rect = test_object("OODU SINA", large_text)
        text_rect = (200, (win.get_height() // 3))
        win.blit(text_surf, text_rect)

        large_text = pygame.font.SysFont(fontz, 22)
        text_surf, text_rect = test_object("ANIRUDHA LAKSHMAN", large_text)
        text_rect = (558, 520)
        win.blit(text_surf, text_rect)

        large_text = pygame.font.SysFont(fontz, 24)
        text_surf, text_rect = test_object("INEN AYTALLA", large_text)
        text_rect = (5, 520)
        win.blit(text_surf, text_rect)

        large_text = pygame.font.SysFont(fontz, 24)
        text_surf, text_rect = test_object("HSVJ", large_text)
        text_rect = (360, 520)
        win.blit(text_surf, text_rect)

        button(p, 149, 320, w, 50, ac, ic, 160, play)
        button(q, 556, 320, w, 50, ac, ic, 565, quit_game, 23)

        pygame.display.update()


def re_play():
    global re_score, sco

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        large_text = pygame.font.SysFont(fontz, 100, True)
        text_surf, text_rect = test_object("HOGE!", large_text)
        text_rect = ((win.get_width() / 3), (win.get_height() // 4))
        win.blit(text_surf, text_rect)

        large_text = pygame.font.SysFont(fontz, 28)
        text_surf, text_rect = test_object("HUSHARU MACCHA", large_text)
        text_rect = (305, 510)
        win.blit(text_surf, text_rect)

        font = pygame.font.SysFont(fontz, 50, False, True)
        text = font.render('Score: ' + str(sco), 1, (0, 0, 0))
        win.blit(text, (330, 240))

        re_score = 1
        pipe.x = 800

        button("Play again?", 140, 320, 170, 50, ac, ic, 160, play)
        button("SAAKA?", 556, 320, 100, 50, ac, ic, 565, quit_game, 23)

        pygame.display.update()


def re_draw_game_window():
    global sco
    win.blit(bg, (0, 0))
    sco = pipe.sc()
    font = pygame.font.SysFont(fontz, 30)
    text = font.render('Score: ' + str(sco), 1, (0, 0, 0))
    win.blit(text, (2, 5))
    cat.draw()
    pipe.draw()
    pipe.move()
    BASE.draw()
    BASE.move()
    pygame.display.update()


def quit_game():
    pygame.quit()
    quit()


def play():
    global pause
    
    pygame.mixer.music.set_volume(vol/2)
    pygame.mixer.music.play(-1)

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_p]:
            pause = True
            paused()

        if not cat.isJump:
            if keys[pygame.K_SPACE]:
                cat.isJump = True

        else:
            if cat.jumpCount >= -10:
                neg = 1
                if cat.jumpCount < 0:
                    neg = -1
                cat.y -= (cat.jumpCount ** 2) * 0.5 * neg
                cat.jumpCount -= 1
            else:
                cat.isJump = False
                cat.jumpCount = 10
        if pipe.collide(cat):
            pygame.mixer.music.stop()
            re_play()
        re_draw_game_window()


BASE = Base(465)
pipe = Pipe(0, 0, 800)
cat = Runner(100, 370)

game_intro("OODU!", "SAAKA?", 100)
