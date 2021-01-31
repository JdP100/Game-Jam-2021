import pygame
import random
import Entities
import Utility

pygame.init()


def draw_text(string, x, y):
    temp_text = font.render(string, False, white, black)
    height = temp_text.get_height()
    window.blit(temp_text, (x, y))
    return height


# MONOLITHIC VARIABLES
Running = True
Paused = False
Debug = False
Sound = True
clock = pygame.time.Clock()
pygame.display.set_caption('Main.py')

# Window Variables
window_width = 3200
window_height = 2400
window = pygame.display.set_mode((window_width // 4, window_height // 4), 0, 32)

# Player Variables
player = Entities.Player(375, 375)
image = pygame.image.load('Images/player_s.png')

# Camera Variables
camera = Entities.Camera(10, 10, 780, 580)

# Button Variables
button_list = {'Play_Button': Entities.Buttons(100, 100, 300, 100), 'Quit_Button': Entities.Buttons(100, 250, 150, 70),
               'Thx_Button': Entities.Buttons(100, 100, 300, 100)}

# Object Variables
arrow_image = pygame.image.load('Images/directional_arrows_s.png')
arrow_width = arrow_image.get_width() // 2
arrow_height = arrow_image.get_height() // 2

item_image = pygame.image.load('Images/items.png')
item_width = item_image.get_width() // 2
item_height = item_image.get_height()

items_dict = {'note_1': Entities.Items(460, 445), 'note_2': Entities.Items(460, 455), 'note_3': Entities.Items(460, 445)}

# Room Variables
room_count_total = 0
cur_level = 0
room_model = 0
room = Utility.create_room(cur_level, room_model)
platform_list = room[0]
door_dict = room[1]
door_pos = room[2]
spike_list = room[3]
path = Utility.create_path(0, False, [2, 2])
cur_step = 0

Room_width = 1600
Room_height = 1200
Room_position = [0, 0]
Room = pygame.Surface((Room_width, Room_height))

# Color Variables
black = (0, 0, 0)
white = (245, 245, 245)
red = (255, 50, 50)
green = (50, 255, 50)
beige = (200, 180, 100)
brown = (150, 120, 0)

# Font Variables
font = pygame.font.SysFont("Courier New", 16)

# GAME LOOP
while Running:
    # UPDATE #
    delta_time = clock.tick(1000) / 1000
    event = pygame.event.poll()
    keys = pygame.key.get_pressed()

    if Paused:
        delta_time = 0

    # Update the Player
    player.update(event, keys, delta_time, room)
    camera.update()
    camera.global_position(player.x, player.y)

    # Update the Room
    for s in spike_list:
        if s.colliderect(player.hitbox):
            room_count_total += 1
            room_model = 0
            room = Utility.create_room(cur_level, 0)
            Room_position = Utility.door_movement(player, 1, Room_position, door_pos)
            cur_step = 0
            path = Utility.create_path(5)
            # Time Constraints
            platform_list = room[0]
            door_dict = room[1]
            door_pos = room[2]
            spike_list = room[3]

    if cur_level != 0:
        for d in door_dict:
            door_num = d
            if door_dict[d] in door_dict.values():
                door_rect = door_dict[d]
                if door_rect.colliderect(player.hitbox):
                    room_count_total += 1
                    player.y_speed = 0
                    if cur_step + 1 < len(path):
                        if door_num != path[cur_step]:
                            cur_step = 0
                            path = Utility.create_path(5)
                            room = Utility.create_room(cur_level, 0)
                            room_model = 0
                        elif door_num == path[cur_step]:
                            cur_step += 1
                            room_model = random.randint(1, 5)
                            room = Utility.create_room(cur_level, room_model)
                    elif cur_step + 1 >= len(path) and cur_level < 5:
                        cur_level += 1
                        room_model = 0
                        cur_step = 0
                        path = Utility.create_path(5)
                        room = Utility.create_room(cur_level, 0)

                    # Reset Player Position
                    platform_list = room[0]
                    door_dict = room[1]
                    door_pos = room[2]
                    spike_list = room[3]
                    Room_position = Utility.door_movement(player, door_num, Room_position, door_pos)
                    break

    if player.y > 4000:
        room_model = 0
        room = Utility.create_room(cur_level, 0)
        Room_position = Utility.door_movement(player, 1, Room_position, door_pos)
        cur_step = 0
        path = Utility.create_path(5)
        # Time Constraints
        platform_list = room[0]
        door_dict = room[1]
        door_pos = room[2]
        spike_list = room[3]

    # Items
    items_dict['note_1'].update(player)
    items_dict['note_2'].update(player)
    items_dict['note_3'].update(player)

    # INPUT #
    # Buttons
    mouse_button = pygame.mouse.get_pressed(3)
    left_click = mouse_button[0]
    mouse_position = pygame.mouse.get_pos()
    if 'Play_Button' in button_list:
        if button_list['Play_Button'].update(mouse_position, left_click):
            cur_level = 1
            player.x = 375
            player.y = 375
            path = Utility.create_path(5)
            Room_position = [0, 100]
        if cur_level != 0:
            del button_list['Play_Button']
    if 'Quit_Button' in button_list:
        if button_list['Quit_Button'].update(mouse_position, left_click):
            Running = False
    if 'Thx_Button' in button_list and cur_level == 5:
        if button_list['Thx_Button'].update(mouse_position, left_click):
            Running = False

    if event.type == pygame.QUIT:
        Running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            Running = False
        elif event.key == pygame.K_o:
            Debug ^= True
        elif event.key == pygame.K_p:
            Paused ^= True

    # Camera
    cam_offset_x = camera.x + (camera.width // 2) - camera.Global_x
    cam_offset_y = camera.y + (camera.height // 2) - camera.Global_y

    # DRAW #
    window.fill(black)
    Room.fill(black)
    window.set_clip(camera.rect)

    # Room Specific
    if room_model == 0 and 0 < cur_level < 5:
        for a in range(len(path)):
            if path[a] == 1:
                Room.blit(arrow_image, (100 + arrow_width * a, 100),
                          [arrow_width, arrow_height, arrow_width, arrow_height])
            elif path[a] == 2:
                Room.blit(arrow_image, (100 + arrow_width * a, 100),
                          [0, 0, arrow_width, arrow_height])
            elif path[a] == 3:
                Room.blit(arrow_image, (100 + arrow_width * a, 100),
                          [0, arrow_height, arrow_width, arrow_height])
            elif path[a] == 4:
                Room.blit(arrow_image, (100 + arrow_width * a, 100),
                          [arrow_width, 0, arrow_width, arrow_height])

    # Items
    if room_count_total == 1:
        items_dict['note_1'].interact = True
        Room.blit(item_image, (items_dict['note_1'].x, items_dict['note_1'].y), (0, 0, item_width, item_height))
    else:
        items_dict['note_1'].interact = False

    if room_count_total > 10 and room_model == 0 and not items_dict['note_2'].read:
        items_dict['note_2'].interact = True
        Room.blit(item_image, (items_dict['note_2'].x, items_dict['note_2'].y), (0, 0, item_width, item_height))
        for d in door_dict:
            door_rect = door_dict[d]
            if door_rect.colliderect(player.hitbox):
                items_dict['note_2'].read = True
    else:
        items_dict['note_2'].interact = False

    if cur_level == 4:
        items_dict['note_3'].interact = True
        Room.blit(item_image, (items_dict['note_1'].x, items_dict['note_1'].y), (0, 0, item_width, item_height))
    else:
        items_dict['note_3'].interact = False

    # Draw the Player
    player.draw(Room, image)

    # Draw the Platforms
    for p in platform_list:
        pygame.draw.rect(Room, white, p, 0)
    if cur_level != 0:
        for d in door_dict:
            pygame.draw.rect(Room, beige, door_dict[d], 0)
            pygame.draw.rect(Room, brown, door_dict[d], 3)
    for s in spike_list:
        pygame.draw.rect(Room, red, s, 0)

    if Debug:
        for p in platform_list:
            pygame.draw.rect(Room, red, p, 2)
        for d in door_dict:
            pygame.draw.rect(Room, green, door_dict[d], 2)

    window.blit(Room, (Room_position[0] + cam_offset_x, Room_position[1] + cam_offset_y), (0, 0, window_width,
                                                                                           window_height))
    if items_dict['note_1'].draw_text:
        text_height = 16
        draw_text('"The moment I entered this place I knew it was a mistake...', 10, 10)
        draw_text("the door vanished behind me as if it never existed in the ", 10, text_height + 10)
        draw_text("first place…I have no choice now but to go deeper into this", 10, 2 * text_height + 10)
        draw_text("mansion in hopes of finding an exit… Im leaving these notes", 10, 3 * text_height + 10)
        draw_text('in case anyone to suffer the same fate as me…"', 10, 4 * text_height + 10)

        draw_text("Well she was definitely here… let’s hope I can find her.", 10, 6 * text_height + 10)

    if items_dict['note_2'].draw_text:
        text_height = 16
        draw_text('"This mansion is definitely not of this world… time here seems', 10, 10)
        draw_text("off I’ve only been walking for about 10 minutes and my watch is", 10, 2 * text_height + 10)
        draw_text("telling me it’s been over two hours… I’m going to write the time", 10, 3 * text_height + 10)
        draw_text('on these notes to keep track of how long I’ve been in here."', 10, 4 * text_height + 10)
        draw_text("(9:44 PM 8/28)", 10, 5 * text_height + 10)

        draw_text("8/28? That was almost two months ago… Has she been in here that long?", 10, 7 * text_height)
    '“  ” '
    if items_dict['note_3'].draw_text:
        text_height = 16
        draw_text('"It seems I’ve found the way out of this mansion and if you’re reading this', 10, 10)
        draw_text("then you have too. I hope my notes helped you escape. Unfortunately this", 10, 2 * text_height + 10)
        draw_text('mansion didn’t have what I was looking for so I’m off to the next lead I have."', 10, 3 * text_height + 10)
        draw_text('(12:50 PM 9/4)', 10, 4 * text_height + 10)

        draw_text("Well its great to know she got out but… where has she gone now?", 10, 5 * text_height + 10)


    # Debug
    if Debug:
        text_height = draw_text("Room Type = {0}, {1}".format(cur_level, room_model), 10, 16)
        draw_text("Path = {0}, Step = {1}".format(path, cur_step), 10, 2 * text_height)
        draw_text("Room (X,Y) = {0}, {1}".format(int(Room_position[0]), int(Room_position[1])), 10, 3 * text_height)
        draw_text("Player (X,Y) = {0}, {1}".format(int(player.x), int(player.y)), 10, 4 * text_height)
    if cur_level == 0:
        button_list['Play_Button'].draw(window, pygame.font.SysFont("Courier New", 64), '  PLAY')
        button_list['Quit_Button'].draw(window, pygame.font.SysFont("Courier New", 32), '  QUIT')
    elif cur_level == 5:
        button_list['Thx_Button'].draw(window, pygame.font.SysFont("Courier New", 64), '  THX')

    pygame.display.flip()

pygame.quit()
