import sprites


class Helicopter(object):
    health = 3
    animation_number = 0
    animation_list = sprites.helicopter_list
    counter = 0
    current = sprites.helicopter_list[animation_number]
    crash_counter = 0
    damaged_counter = 0
    damaged = False
    wreck_start = False
    wrecked = False
    x = 0
    y = 0
    moving_up = False
    moving_left = False
    moving_down = False
    moving_right = False
    next_0 = True
    next_1 = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def wreck(self):
        self.wreck_start = True
        self.crash_counter += 1
        if 5 <= self.crash_counter < 10:
            self.current = sprites.helicopter_crash_1
        if 10 <= self.crash_counter < 15:
            self.current = sprites.helicopter_crash_2
        if 15 <= self.crash_counter < 20:
            self.current = sprites.helicopter_crash_3
        if self.crash_counter >= 20:
            self.current = sprites.helicopter_crash_4
            self.crash_counter = 0
            self.wreck_start = False
            self.wrecked = True

    def blink_red(self):
        self.animation_list = sprites.damage_helicopter_list
        self.damaged_counter += 1
        if self.damaged_counter >= 15:
            self.animation_list = sprites.helicopter_list
            self.damaged = False
            self.damaged_counter = 0