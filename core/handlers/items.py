import pygame

from core.data.constants import hX, hY, hW, hH

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

    def needRotate(self, cords):
        if self.pivotX() < cords[0] and self.is_rotate():
            self.image = pygame.transform.flip(self.image, True, False)
            self.rotate()
        if self.pivotX() > cords[0] and not self.is_rotate():
            self.image = pygame.transform.flip(self.image, True, False)
            self.rotate()

    def needStep(self, cords):
        return cords[0] != self.pivotX() or cords[1] != self.pivotY()

    def setDiff(self, cords, pixels):
        sx, sy = 0, 0

        if cords[0] > self.pivotX() and pixels[self.pivotX() + 1, self.pivotY()] == 0:
            sx = 1
        elif cords[0] < self.pivotX() and pixels[self.pivotX() - 1, self.pivotY()] == 0:
            sx = -1
        if cords[1] > self.pivotY() and pixels[self.pivotX(), self.pivotY() + 1] == 0:
            sy = 1
        elif cords[1] < self.pivotY() and pixels[self.pivotX(), self.pivotY() - 1] == 0:
            sy = -1

        return sx, sy

    def setRect(self, sx, sy):
        self.rect.x += sx
        self.rect.y += sy

    def nextStep(self, cords, pixels):
        sx, sy = self.setDiff(cords, pixels)
        self.setRect(sx, sy)
        return (sx, sy) == (0, 0)

    # идем вниз или вверх до тех пор,
    # пока левый или правый пиксель (в зависимости от dx) не будет черный в ч\б фоне (0 - черный).
    # ПРОВЕРИТЬ! судя по всему этот код только для сглаженной функции!
    # НЕ РАБОТАЕТ при обходе вверх!
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
