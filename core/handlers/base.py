import os
import sys
import pygame

# Импорт объектов-героев
from core.handlers.items import Hero
# Получение констант из конфигурации
from core.data.constants import hX, hY, dS, nT


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

def __screen_setup__(name, mode):
    # получаем размер экрана
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h
    # растягиваем окно во весь экран
    screen = pygame.display.set_mode((screen_w, screen_h), mode)

    # устанавливаем название окна
    pygame.display.set_caption(name)

    return screen

def screen_init():
    # настройка экрана
    screen = __screen_setup__('Game', pygame.FULLSCREEN)

    # растянутый игровой фон помещаем в группу спрайтов для отрисовки
    image1 = load_image("backround.jpg")
    bg_image = pygame.transform.scale(image1, screen.get_size())
    # получение группы спрайтов для отрисовки
    all_sprites = pygame.sprite.Group()
    bg = pygame.sprite.Sprite(all_sprites)
    bg.image = bg_image
    bg.rect = bg.image.get_rect()
    bg.rect.x, bg.rect.y = 0, 0

    # растянутый задний фон в ч/б (границы ходьбы) преобразуем в PixelArray
    image2 = load_image("wb_backround.jpg")
    wb_bg_image = pygame.transform.scale(image2, screen.get_size())
    # получение массива пикселей
    pixels = pygame.PixelArray(wb_bg_image)

    return screen, pixels, all_sprites

def __entity_fabric__(entity, sprite, size, coordinates):
    entity_image = load_image(sprite)
    entity.image = entity_image
    entity.rect = entity.image.get_rect()
    # засовываем картинку героя в квадрат dSxdS (175х175), где size - кортедж
    entity.image = pygame.transform.scale(entity_image, size)
    # начальные координаты левого верхнего угла прямоугольной области для персонажа, где coordinates - кортедж
    entity.rect.x, entity.rect.y = coordinates
    return entity

def entities_init():
    # Здесь инициализируются требуемые сущности

    # Сущность Hero
    hero = __entity_fabric__(Hero(), "hero.jpg", (dS, dS), (hX, hY))

    # Сущность

    # Возвратить в кортеже все инициализируемые сущности
    return hero

def game_init(screen, all_sprites, hero):
    all_sprites.add(hero)
    all_sprites.draw(screen)

    clock = pygame.time.Clock()

    # isStep = False - маркер приостаноки, т. е. требуется обход препятствия (текущая пиксела не валидная)
    isStep = True
    # isImpasse = True - маркер начала обхода препятствия (текущая пиксела не валидная)
    isImpasse = False
    # новые требуемые координаты героя совпадают с собственными координатами героя
    cords = (hX, hY)
    isGame = True
    dx, dy = 0, 0
    return isGame, isStep, isImpasse, clock, cords, dx, dy

def step_handling(pixels, cords, hero, isStep, isImpasse, dx, dy):
    # смотрим, является ли пиксель по цвету в ч\б фоне черным (равен 0), иначе ничего не делаем, и
    # меняем корды героя, если хоть одна отличается от кордов клика
    if pixels[cords] == 0 and hero.needStep(cords):
        # узнаем в каком направлении идти по x и y при fd = True (пиксела валидная, препятствие не обходим)
        # пытаемся сделать шаг
        if isStep:
            # isImpasse = True - значит обнаружено препятствие
            isImpasse = hero.nextStep(cords, pixels)

        # ВАЖНО! если после тика корды не поменялись, а мы всё равно прошли через верхнее условие,
        # то наш перс стоит в тупике, ниже код обхода этого тупика
        if isImpasse:
            # продолжение шага при обнаружении препятствия для решения, как поступать;
            # в corners проверяем различные ситуации, когда обходить надо по разному
            if isStep:
                dx, dy = corners((hero.pivotX(), hero.pivotY()), cords)

            # isStep = False - приостановка шага для обработки обхода
            isStep = hero.overcomeStep(pixels, dx, dy)
    return isStep, isImpasse, dx, dy

def step_fix(screen, all_sprites, hero, cords, clock):
    # проверка необходимости перевернуть героя
    hero.needRotate(cords)

    all_sprites.draw(screen)

    clock.tick(nT)

    # Отображение новых изменений (перерисовка)
    pygame.display.flip()

def game():
    # Конфигурация экрана
    screen, pixels, all_sprites = screen_init()

    # Получить все сущности в кортеже
    hero = entities_init()

    # Задание значений игровых переменных
    isGame, isStep, isImpasse, clock, cords, dx, dy = game_init(screen, all_sprites, hero)

    # Основной игровыой цикл
    while isGame:
        isGame, cords = event_handling(pygame.event.get(), cords)

        isStep, isImpasse, dx, dy = step_handling(pixels, cords, hero, isStep, isImpasse, dx, dy)

        step_fix(screen, all_sprites, hero, cords, clock)