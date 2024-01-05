import os
import sys
import pygame

# Импорт объектов-героев
from core.handlers.items import Hero
# Получение констант из конфигурации
from core.data.constants import hX, hY, dS


def load_image(name):
    fullname = os.path.join('core/data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

# сложно, главное что работает
def corners(pos1, pos2):
    if pos2[0] - pos1[0] <= 0 > pos2[1] - pos1[1]:
        return -1, 1
    elif pos2[0] - pos1[0] <= 0 < pos2[1] - pos1[1]:
        return -1, 1
    elif pos2[0] - pos1[0] >= 0 > pos2[1] - pos1[1]:
        return 1, 1
    elif pos2[0] - pos1[0] >= 0 < pos2[1] - pos1[1]:
        return 1, 1
    elif pos2[0] - pos1[0] < 0 == pos2[1] - pos1[1]:
        return -1, 1
    elif pos2[0] - pos1[0] > 0 == pos2[1] - pos1[1]:
        return 1, 1
    else:
        return 0, 0

def event_handling(events, cords):
    for event in events:
            # выход из программы при нажатии на крестик
            if event.type == pygame.QUIT:
                return False, cords

            # выход из программы по клавише Esc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False, cords

            # проверка получения новых координат для героя
            if event.type == pygame.MOUSEBUTTONDOWN:
                # новые требуемые координаты героя
                return True, event.pos
    return True, cords

def screen_init(pygame):
    # получаем размер экрана
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h
    # растягиваем окно во весь экран
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)

    # устанавливаем название окна
    pygame.display.set_caption('Game')

    # получаем и растягиваем картинку на весь экран
    image1 = load_image("backround.jpg")
    bg_image = pygame.transform.scale(image1, (screen_w, screen_h))
    all_sprites = pygame.sprite.Group()
    bg = pygame.sprite.Sprite(all_sprites)
    bg.image = bg_image
    bg.rect = bg.image.get_rect()
    bg.rect.x, bg.rect.y = 0, 0

    # растянутый задний фон в ч/б (границы ходьбы) преобразуем в PixelArray
    image2 = load_image("wb_backround.jpg")
    wb_bg_image = pygame.transform.scale(image2, (screen_w, screen_h))
    pixels = pygame.PixelArray(wb_bg_image)
    return screen, pixels, all_sprites

def heros_init(pygame):
    # Здесь добавляются разные герои

    # Первый герой Hero
    hero = Hero()
    hero_image = load_image("hero.jpg")
    hero.image = hero_image
    hero.rect = hero.image.get_rect()
    # засовываем картинку героя в квадрат dSxdS (175х175)
    hero.image = pygame.transform.scale(hero_image, (dS, dS))
    # начальные координаты левого верхнего угла прямоугольной области для персонажа
    hero.rect.x, hero.rect.y = hX, hY

    # Второй герой

    # Возврать в кортедже всех героев
    return hero

def game_init(screen, all_sprites, hero):
    all_sprites.add(hero)
    all_sprites.draw(screen)

    clock = pygame.time.Clock()

    # isStep = False - маркер приостаноки, т. е. требуется обход препятствия (текущая пиксела не валидная)
    isStep = True
    # новые требуемые координаты героя совпадают с собственными координатами героя
    cords = (hX, hY)
    running = True
    return running, isStep, clock, cords