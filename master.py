# pygame - https://habr.com/ru/articles/588605/
# работа со спрайтами - https://habr.com/ru/articles/588765/
# шпаргалка - https://waksoft.susu.ru/2019/04/24/pygame-shpargalka-dlja-ispolzovanija/
import pygame

# Импорт спомогательных функций
from core.handlers.base import corners, screen_init, heros_init, game_init, event_handling, game_update


def main():

    # Конфигурация игрового движка
    pygame.init()

    # Конфигурация экрана
    screen, pixels, all_sprites = screen_init(pygame)

    # Получение всех героев в кортедже
    hero = heros_init(pygame)

    # Задание значений игровых переменных
    running, isStep, clock, cords = game_init(screen, all_sprites, hero)

    # Основной игровыой цикл
    while running:
        running, cords = event_handling(pygame.event.get(), cords)

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

        game_update(pygame, screen, all_sprites, hero, cords, clock)

    pygame.quit()


if __name__ == '__main__':
    main()
