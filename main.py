import pygame
from pgu import gui
import sys

pygame.init()
screen_x, screen_y = 800, 400
FPS = 60


class Player:
    def __init__(self, color, x, y, width, height, speed):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw_play(self, screen):
        x = self.x
        y = self.y
        pygame.draw.rect(screen, "gray", (x, y, self.width, self.height))

    def pl_right(self):
        if self.x <= screen_x - self.width:
            self.x += self.speed

    def pl_left(self):
        if self.x >= 0:
            self.x -= self.speed


class Ball:
    def __init__(self, color, x, y, radius, speedx, speedy):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.speedx = speedx
        self.speedy = speedy
        self.ballrect = None

    def ballmove(self, p):
        self.y += self.speedy
        self.x += self.speedx
        if self.y <= self.radius:
            self.speedy = -self.speedy
        if self.y > p.y - self.radius and p.x + p.width > self.x > p.x - self.radius:
            self.speedy = -self.speedy
        if self.x >= screen_x - self.radius or self.x <= self.radius:
            self.speedx = -self.speedx

    def draw(self, screen):
        self.ballrect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        pygame.draw.circle(screen, "yellow", self.ballrect.center, self.radius)


class Brick:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw_brick(self, screen):
        bricks = []
        for row in range(1, 10):
            for col in range(1, 10):
                x = col * (self.width + 5)
                y = row * (self.height + 5)
                if (x <= screen_x and x >= 0 and y <= screen_y):
                    brick = pygame.Rect(x, y, self.width, self.height)
                    bricks.append(brick)

        for brick in bricks:
            pygame.draw.rect(screen, (184, 134, 11), brick)
        return bricks


def check_colision(brick, ball):
    if pygame.Rect.colliderect(brick, ball.ballrect):
        return True
    return False

def create_popup(screen, clock, bricks):

    if len(bricks) == 0:
        label = gui.Label("YOU WIN!")
    else:
        label = gui.Label("YOU LOSE :( ")

    btn_restart = gui.Button("Restart Game")
    btn_quit = gui.Button("Quit Game")

    def close_popup(event=None):
        pygame.quit()
        sys.exit()

    def restart_game():
        player1 = Player("gray", 350, 370, 100, 20, 10)
        brickFactory = Brick("white", 5, 2, 70, 20)
        bricks = brickFactory.draw_brick(screen)
        ball = Ball(("Red"), 400, 355, 10, 3, 3)
        game_loop(screen, clock, player1, bricks, ball)
        pygame.display.update()

    btn_restart.connect(gui.CLICK, restart_game)
    btn_quit.connect(gui.CLICK, close_popup)
    main_table = gui.Table(width=300, height=200)
    main_table.tr()
    main_table.td(label, colspan=2)
    main_table.tr()
    main_table.td(btn_restart, colspan=1)
    main_table.td(btn_quit, colspan=1)
    dialog = gui.Dialog(gui.Label("Game Over"), main_table)
    dialog.open()
    app = gui.Desktop()
    app.init(widget=dialog, screen=screen, area=screen.get_rect())
    app.run()


def game_loop(screen, clock, player1, bricks, ball):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player1.pl_right()
        if keys[pygame.K_LEFT]:
            player1.pl_left()

        if ball.y >= screen_y or len(bricks) == 0:
            create_popup(screen, clock, bricks)
            return

        ball.ballmove(player1)
        player_move(player1, ball)
        screen.fill((0, 0, 0))
        ball.draw(screen)

        for brick in bricks:
            is_colision = check_colision(brick, ball)
            if is_colision:
                bricks.remove(brick)

                ball.speedy -= 2 * ball.speedy

        for brick in bricks:
            pygame.draw.rect(screen, "red", brick)

        player1.draw_play(screen)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    screen = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Break Bricks')
    clock = pygame.time.Clock()

    player1 = Player("gray", 350, 370, 100, 20, 10)
    brickFactory = Brick("white", 5, 2, 70, 20)
    bricks = brickFactory.draw_brick(screen)

    ball = Ball(("Red"), 400, 355, 10, 3, 3)
    game_loop(screen, clock, player1, bricks, ball)

    pygame.display.update()


if __name__ == '__main__':
    main()
