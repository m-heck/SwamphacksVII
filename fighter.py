# Abstract class for attackers and defender
import pygame
import os
import helper
import random

# Loads images
# !! FOR NOW, GREEN = DEFENDERS and BLUE = ATTACKERS
GREEN_DRAGON_1 = pygame.image.load(os.path.join("images", "gdrag1.png"))
GREEN_DRAGON_1 = pygame.transform.scale(GREEN_DRAGON_1, (80, 80))
GREEN_DRAGON_2 = pygame.image.load(os.path.join("images", "gdrag2.png"))
GREEN_DRAGON_2 = pygame.transform.scale(GREEN_DRAGON_2, (80, 80))
BLUE_DRAGON_1 = pygame.image.load(os.path.join("images", "bdrag1.png"))
BLUE_DRAGON_1 = pygame.transform.scale(BLUE_DRAGON_1, (80, 80))
BLUE_DRAGON_2 = pygame.image.load(os.path.join("images", "bdrag2.png"))
BLUE_DRAGON_2 = pygame.transform.scale(BLUE_DRAGON_2, (80, 80))


class Fighter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = None
        self.img2 = None

    # Draws person to window
    def draw(self, window, reverse, show_range=True):
        if reverse:
            window.blit(self.img, (self.x, self.y))
        else:
            window.blit(self.img2, (self.x, self.y))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_alive(self):
        return self.alive

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def scale(self, first, second):
        self.img = pygame.transform.scale(self.img, (first, second))
        self.img2 = pygame.transform.scale(self.img2, (first, second))


class Attacker(Fighter):
    def __init__(self, x=0, y=450, hp=100, move_delay=300):
        super().__init__(x, y)
        self.max_hp = hp
        self.hp = hp
        self.move_delay = move_delay
        self.img = BLUE_DRAGON_1
        self.img2 = BLUE_DRAGON_2
        self.mask = pygame.mask.from_surface(self.img)
        self.alive = True

    def draw(self, window, reverse, show_range=True):
        if reverse:
            window.blit(self.img, (self.x, self.y))
        else:
            window.blit(self.img2, (self.x, self.y))
        self.healthbar(window)

    def get_center_x(self):
        return self.x + self.img.get_width() / 2

    def get_center_y(self):
        return self.y + self.img.get_height() / 2

    def get_img(self):
        return self.img

    # MOVEMENT METHODS
    def move_right(self, steps, window_width):
        if self.x + self.img.get_width() + 10 <= window_width:
            self.x += steps
        else:
            self.x = window_width - self.img.get_width()
        pygame.time.wait(self.move_delay)

    def move_left(self, steps):
        if self.x - steps >= 0:
            self.x -= steps
        else:
            self.x = 0
        pygame.time.wait(self.move_delay)

    def move_up(self, steps):
        if self.y - steps >= 0:
            self.y -= steps
        else:
            self.y = 0
        pygame.time.wait(self.move_delay)

    def move_down(self, steps, window_height):
        if self.y + steps + self.img.get_height() <= window_height:
            self.y += steps
        else:
            self.y = window_height
        pygame.time.wait(self.move_delay)

    def take_damage(self, dmg):
        if self.hp - dmg > 0:
            self.hp -= dmg
        else:
            self.hp = 0
            self.alive = False
            # TODO broadcast event for attacker killed

    def set_hp(self, newhp):
        self.hp = newhp

    def healthbar(self, window):
        # red rect
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width(), 10))

        # green rect
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width() * (self.hp / self.max_hp), 10))


class Defender(Fighter):
    def __init__(self, x=370, y=300, atk=5, range=200, accuracy=80):
        super().__init__(x, y)
        self.atk = atk
        self.range = range
        self.img = GREEN_DRAGON_1
        self.img2 = GREEN_DRAGON_2
        self.cooldown = 5
        self.cool_down_counter = 0
        self.mask = pygame.mask.from_surface(self.img)
        self.accuracy = accuracy

    def draw(self, window, reverse, show_range=True):
        if reverse:
            window.blit(self.img, (self.x, self.y))
        else:
            window.blit(self.img2, (self.x, self.y))
        if show_range:
            self.attack_radius(window)

    def get_center_x(self):
        return self.x + self.img.get_width() / 2

    def get_center_y(self):
        return self.y + self.img.get_height() / 2

    def get_img(self):
        return self.img

    def cool_down_caller(self):
        if self.cool_down_counter >= self.cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def attack(self, attackers):
        if self.cool_down_counter == 0:
            closest_attacker = helper.find_closest(self, attackers)
            if random.randint(0, 100) <= self.accuracy:
                if helper.find_distance(self, closest_attacker) < self.range:
                    closest_attacker.take_damage(self.atk)
                    self.cool_down_counter = 1

    def attack_radius(self, window):
        pygame.draw.circle(window, (128, 0, 0), (self.get_center_x(), self.get_center_y()), self.range, 2)
