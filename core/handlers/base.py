# сложно, главное что работает
def corners(pos1, pos2):
    if pos2[0] - pos1[0] <= 0 and pos2[1] - pos1[1] <= 0:
        return -1, -2
    elif pos2[0] - pos1[0] <= 0 <= pos2[1] - pos1[1]:
        return -1, 2
    elif pos2[0] - pos1[0] >= 0 >= pos2[1] - pos1[1]:
        return 1, -2
    elif pos2[0] - pos1[0] >= 0 and pos2[1] - pos1[1] >= 0:
        return 1, 2