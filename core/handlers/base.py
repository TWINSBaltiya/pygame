import os
import sys
import pygame


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