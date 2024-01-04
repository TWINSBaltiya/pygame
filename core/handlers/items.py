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

    def needStep(self, cords):
        return cords[0] != self.rect.x + hW or cords[1] != self.rect.y + hH

    def nextStep(self, cords, pixels):
        sx, sy = 0, 0
        if cords[0] > self.rect.x + hW and pixels[self.rect.x + hW + 1, self.rect.y + hH] == 0:
            sx = 1
        elif cords[0] < self.rect.x + hW and pixels[self.rect.x + hW - 1, self.rect.y + hH] == 0:
            sx = -1
        if cords[1] > self.rect.y + hH and pixels[self.rect.x + hW, self.rect.y + hH + 1] == 0:
            sy = 1
        elif cords[1] < self.rect.y + hH and pixels[self.rect.x + hW, self.rect.y + hH - 1] == 0:
            sy = -1
        self.rect.x += sx
        self.rect.y += sy
        return sx, sy

    # идем вниз или вверх до тех пор,
    # пока левый или правый пиксель (в зависимости от dx) не будет черный в ч\б фоне.
    # 0 - соответствует черному цвету.
    # ПРОВЕРИТЬ! судя по всему условие верно только один раз, иначе на второй раз dx, dy не определены!
    def overcomeStep(self, pixels, dx, dy):
        if pixels[self.pivotX() + dx, self.pivotY()] != 0:
            self.rect.y += dy
            return False
        else:
            return True

    # координаты точки отсчета героя
    def pivotX(self):
        return self.rect.x + hW
    def pivotY(self):
        return self.rect.y + hH



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
