# pygame - https://habr.com/ru/articles/588605/
# работа со спрайтами - https://habr.com/ru/articles/588765/
# шпаргалка - https://waksoft.susu.ru/2019/04/24/pygame-shpargalka-dlja-ispolzovanija/
import pygame

# Импорт спомогательных функций
from core.handlers.base import screen_init, heros_init, game_init, step_handling, event_handling, step_fix


def main():

    # Конфигурация игрового движка
    pygame.init()

    # Конфигурация экрана
    screen, pixels, all_sprites = screen_init(pygame)

    # Получение всех героев в кортедже
    hero = heros_init(pygame)

    # Задание значений игровых переменных
    isGame, isStep, isImpasse, clock, cords, dx, dy = game_init(screen, all_sprites, hero)

    # Основной игровыой цикл
    while isGame:
        isGame, cords = event_handling(pygame.event.get(), cords)

        isStep, isImpasse, dx, dy = step_handling(pixels, cords, hero, isStep, isImpasse, dx, dy)

        step_fix(pygame, screen, all_sprites, hero, cords, clock)

    pygame.quit()


if __name__ == '__main__':
    main()
