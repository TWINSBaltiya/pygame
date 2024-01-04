import pygame

# начальные корды для персонажа
hX = 460
hY = 490

# относительные смещения от левого верхнего угла прямоугольника героя
hW = 75
hH = 165

# размеры спрайта героя
dS = 175


# класс перса
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cords = ()
        # его начальные корды
        self.x = hX
        self.y = hY
        # маркер повернут или нет Hero
        self.f = False

    def __call__(self, screen, *args):
        # перерисовываем на новые корды (в args передеём х и у)
        self.x += args[0]
        self.y += args[1]

        self.cords = (self.x, self.y)

    def is_rotate(self):
        return self.f

    def rotate(self):
        if self.f:
            self.f = False
        else:
            self.f = True

    def get_cords(self):
        return self.cords

# не используется
class item:
    def __init__(self):
        self.cords = ()
        # его начальные корды
        self.x = 410
        self.y = 540

    def __call__(self, screen, *args):
        # перерисовываем на новые корды (в args передеём х и у)
        self.x += args[0]
        self.y += args[1]
        pygame.draw.rect(screen, 'red', (self.x, self.y, 100, 150), 8)
        self.cords = (self.x, self.y)

    def get_cords(self):
        return self.cords
