import pygame
import random
import Lists


def create_path(length, randomized=True, preset=None):
    """ Creates a sequence of Numbers correlating to directions that the Player can follow,
     without going back on themselves."""
    if randomized:
        path = [random.choice((4, 2))]
        L = (0, (1, 2, 4), (1, 2, 3), (2, 3, 4), (1, 3, 4))
        for i in range(length):
            x = random.choice(L[path[i]])
            path.append(x)
    else:
        path = preset
    return path


def door_movement(player, door_number, room_position, door_entrances):
    """ Sets the Player and Room (Surface) positions upon stage transition. """
    if door_number == 1:
        player.x = door_entrances[3][0]
        player.y = door_entrances[3][1]
        room_position[0] = player.x - door_entrances[3][0]
        room_position[1] = player.y - door_entrances[3][1]
    elif door_number == 2:
        player.x = door_entrances[4][0]
        player.y = door_entrances[4][1]
        room_position[0] = player.x - door_entrances[4][0]
        room_position[1] = player.y - door_entrances[4][1]
    elif door_number == 3:
        player.x = door_entrances[1][0]
        player.y = door_entrances[1][1]
        room_position[0] = player.x - door_entrances[1][0]
        room_position[1] = player.y - door_entrances[1][1]
    elif door_number == 4:
        player.x = door_entrances[2][0]
        player.y = door_entrances[2][1]
        room_position[0] = player.x - door_entrances[2][0]
        room_position[1] = player.y - door_entrances[2][1]
    return room_position


def r(x, y, w, h):
    """ Makes a Rectangle"""
    return pygame.Rect(x, y, w, h)


def map_to_rect(col_map):
    list_a = []
    list_b = []
    y = 0
    for row in col_map:
        x = 0
        for tile in row:
            if tile == '1':
                a = r(x * 20, y * 20, 20, 20)
                list_a.append(a)
            if tile == '2':
                b = r(x * 20, y * 20, 20, 20)
                list_b.append(b)
            x += 1
        y += 1
    return list_a, list_b


def create_room(layer, model):
    """ Creates a Platform List and a Door List that the Player can interact with. """
    plat_list = []
    door_list = {}
    door_entrances = {}
    damage_list = []
    if layer == 0:
        plat_list = [r(0, 0, 20, 600), r(20, 0, 780, 20), r(780, 20, 20, 580), r(20, 580, 760, 20)]
        door_list = {0: r(375, 375, 10, 10)}
        door_entrances = {1: [375, 375], 2: [375, 375], 3: [375, 375], 4: [375, 375]}
    elif 0 < layer < 2:

        # MODEL 1 -------------------------------------------------------------------------------------------------
        if model == 1:
            # Platforms
            platforms = map_to_rect(Lists.r1)
            for p in platforms[0]:
                plat_list.append(p)
            for s in platforms[1]:
                damage_list.append(s)

            # Doors
            door_list = {1: r(480, 0, 160, 40), 2: r(1560, 480, 60, 120), 3: r(1000, 1160, 160, 80),
                         4: r(0, 680, 40, 160)}
            door_entrances = {1: [500, 100], 2: [1500, 500], 3: [1000, 990], 4: [80, 780]}

        # MODEL 2 -------------------------------------------------------------------------------------------------
        elif model == 2:
            platforms = map_to_rect(Lists.r2)
            for p in platforms[0]:
                plat_list.append(p)
            for s in platforms[1]:
                damage_list.append(s)

            # Doors
            door_list = {1: r(440, 0, 160, 40), 2: r(1560, 760, 60, 160), 3: r(440, 1160, 160, 40),
                         4: r(0, 280, 40, 160)}
            door_entrances = {1: [530, 90], 2: [1500, 840], 3: [420, 1040], 4: [60, 360]}

        # MODEL 3 -------------------------------------------------------------------------------------------------
        elif model == 3:
            # Platforms
            platforms = map_to_rect(Lists.r3)
            for p in platforms[0]:
                plat_list.append(p)
            for s in platforms[1]:
                damage_list.append(s)

            # Doors
            door_list = {1: r(280, 0, 160, 40), 2: r(1560, 720, 60, 160), 3: r(1240, 1160, 160, 40),
                         4: r(0, 160, 40, 160)}
            door_entrances = {1: [380, 90], 2: [1500, 760], 3: [1220, 1020], 4: [60, 200]}

        # MODEL 4 -------------------------------------------------------------------------------------------------
        elif model == 4:
            # Platforms
            platforms = map_to_rect(Lists.r4)
            for p in platforms[0]:
                plat_list.append(p)
            for s in platforms[1]:
                damage_list.append(s)

            # Doors
            door_list = {1: r(720, 0, 160, 40), 2: r(1560, 520, 40, 160), 3: r(720, 1160, 160, 40),
                         4: r(0, 520, 40, 160)}
            door_entrances = {1: [760, 80], 2: [1500, 600], 3: [700, 990], 4: [60, 600]}

        # MODEL 5 -------------------------------------------------------------------------------------------------
        elif model == 5:
            # Platforms
            platforms = map_to_rect(Lists.r5)
            for p in platforms[0]:
                plat_list.append(p)
            for s in platforms[1]:
                damage_list.append(s)

            # Doors
            door_list = {1: r(1000, 0, 160, 60), 2: r(1560, 120, 40, 160), 3: r(1320, 1160, 160, 40),
                         4: r(0, 880, 40, 160)}
            door_entrances = {1: [1020, 90], 2: [1500, 220], 3: [1340, 835], 4: [80, 960]}

        # MODEL 0 -------------------------------------------------------------------------------------------------
        elif model == 0:
            # Platforms
            platforms = map_to_rect(Lists.r0)
            for p in platforms[0]:
                plat_list.append(p)
            for s in platforms[1]:
                damage_list.append(s)

            # Doors
            door_list = {4: r(0, 280, 60, 160), 2: r(740, 280, 60, 160)}
            door_entrances = {1: [300, 300], 2: [300, 300], 3: [300, 300], 4: [300, 300]}

    # End Room
    elif layer == 2:
        platforms = map_to_rect(Lists.r_end)
        for p in platforms[0]:
            plat_list.append(p)
        door_entrances = {1: [300, 300], 2: [300, 300], 3: [300, 300], 4: [300, 300]}

    return plat_list, door_list, door_entrances, damage_list
