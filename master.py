
import pygame

# Импорт спомогательных функций
from core.handlers.base import game


def main():
    # Конфигурация игрового движка
    pygame.init()
    # Игровой цикл
    game()
    # Выход из приложения
    pygame.quit()


if __name__ == '__main__':
    main()
