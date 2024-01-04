# pygame - https://habr.com/ru/articles/588605/
# работа со спрайтами - https://habr.com/ru/articles/588765/
# шпаргалка - https://waksoft.susu.ru/2019/04/24/pygame-shpargalka-dlja-ispolzovanija/
import pygame

from core.handlers.base import corners, load_image
from core.handlers.items import Hero, hX, hY, hW, hH, dS


def main():
    pygame.init()

    # 150 тактов за 0,15 c
    nT = 150

    # получаем размер экрана
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h

    # растягиваем окно во весь экран
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Game')

    all_sprites = pygame.sprite.Group()

    # получаем и растягиваем картинку на весь экран
    image1 = load_image("backround.jpg")
    bg_image = pygame.transform.scale(image1, (screen_w, screen_h))
    bg = pygame.sprite.Sprite(all_sprites)
    bg.image = bg_image
    bg.rect = bg.image.get_rect()
    bg.rect.x, bg.rect.y = 0, 0

    # растянутый задний фон в ч/б (границы ходьбы)
    image2 = load_image("wb_backround.jpg")
    wb_bg_image = pygame.transform.scale(image2, (screen_w, screen_h))
    pixels = pygame.PixelArray(wb_bg_image)

    clock = pygame.time.Clock()
    hero = Hero()
    hero_image = load_image("hero.jpg")
    hero.image = hero_image
    hero.rect = hero.image.get_rect()
    # засовываем картинку героя в квадрат dSxdS (175х175)
    hero.image = pygame.transform.scale(hero_image, (dS, dS))
    # начальные координаты левого верхнего угла прямоугольной области для персонажа.
    hero.rect.x, hero.rect.y = hX, hY
    all_sprites.add(hero)

    all_sprites.draw(screen)
    # fd = False - маркер того, что требуется обход препятствия (текущая пиксела не валидная)
    fd = True
    # новые требуемые координаты героя совпадают с собственными координатами героя
    cords = (hX, hY)
    running = True
    while running:
        for event in pygame.event.get():
            # выход из программы при нажатии на крестик
            if event.type == pygame.QUIT:
                running = False

            # выход из программы по клавише Esc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # проверка получения новых координат для героя
            if event.type == pygame.MOUSEBUTTONDOWN:
                # новые требуемые координаты героя
                cords = event.pos

                # проверка необходимости перевернуть героя
                if hero.rect.x + hW < cords[0] and hero.is_rotate():
                    hero.image = pygame.transform.flip(hero.image, True, False)
                    hero.rotate()
                if hero.rect.x + hW > cords[0] and not hero.is_rotate():
                    hero.image = pygame.transform.flip(hero.image, True, False)
                    hero.rotate()

        # смотрим, является ли пиксель по цвету в ч\б фоне черным (равен 0), иначе ничего не делаем.
        if pixels[cords] == 0:
            # меняем корды героя, если хоть одна отличается от кордов клика
            if (cords[0] != hero.rect.x + hW or cords[1] != hero.rect.y + hH):
                x, y = 0, 0

                # узнаем в каком направлении идти по x и y при fd = True (пиксела валидная, препятствие не обходим)
                if fd:
                    # TODO: сделать функцию очередного смещения, возвращающую int, int (для установки x, y)
                    if cords[0] > hero.rect.x + hW and pixels[hero.rect.x + hW + 1, hero.rect.y + hH] == 0:
                       x = 1
                    elif cords[0] < hero.rect.x + hW and pixels[hero.rect.x + hW - 1, hero.rect.y + hH] == 0:
                       x = -1
                    if cords[1] > hero.rect.y + hH and pixels[hero.rect.x + hW, hero.rect.y + hH + 1] == 0:
                       y = 1
                    elif cords[1] < hero.rect.y + hH and pixels[hero.rect.x + hW, hero.rect.y + hH - 1] == 0:
                       y = -1
                    hero.rect.x += x
                    hero.rect.y += y
                    print(cords, (hero.rect.x + hW, hero.rect.y + hH))

                # ВАЖНО! если после тика корды не поменялись, а мы всё равно прошли через верхнее условие,
                # то наш перс стоит в тупике, ниже код обхода этого тупика
                # TODO: сделать функцию обхода, возвращающую bool (для установки fd)
                if x == 0 and y == 0:
                    print(cords, (hero.rect.x + hW, hero.rect.y + hH))
                    # в corners проверяем различные ситуации, когда ободить надо по разному
                    if fd:
                        dx, dy = corners((hero.rect.x + hW, hero.rect.y + hH), cords)
                    # идем вниз или вверх до тех пор,
                    # пока левый или правый пиксель (в зависимости от dx) не будет черный в ч\б фоне.
                    # 0 - соответствует черному цвету.
                    if pixels[hero.rect.x + hW + dx, hero.rect.y + hH] != 0:
                        hero.rect.y += dy
                        fd = False
                    else:
                        fd = True

        all_sprites.draw(screen)

        clock.tick(nT)

        # Отображение новых изменений (перерисовка)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
