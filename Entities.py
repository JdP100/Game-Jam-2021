import pygame


class Buttons:
    """ Buttons the Player can click with their mouse. """

    def __init__(self, x, y, width, height, pause=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Pause = pause
        self.color = (200, 200, 200)
        self.border = (100, 100, 100)

    def update(self, mouse_pos, click):
        self.color = (200, 200, 200)
        self.border = (100, 100, 100)
        if self.x <= mouse_pos[0] <= self.x + self.width:
            if self.y <= mouse_pos[1] <= self.y + self.height:
                self.color = (250, 250, 200)
                self.border = (100, 150, 150)
                if click:
                    return True

    def draw(self, surface, font=None, string=None):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(surface, self.border, (self.x, self.y, self.width, self.height), 4)
        if font is not None and string is not None:
            temp_text = font.render(string, False, self.border)
            surface.blit(temp_text, (self.x, self.y))


class Camera:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.Global_x = 0
        self.Global_y = 0
        self.entity = None

    def global_position(self, x, y):
        self.Global_x = x
        self.Global_y = y

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Player:
    """ The Player object. """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.new_x = x
        self.new_y = y
        self.height = 55
        self.width = 40
        self.x_speed = 200
        self.y_speed = 0
        self.x_acceleration = None
        self.y_acceleration = 400
        self.y_collision = False
        self.x_collision = False
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.on_ground = True
        self.double_jump = False
        self.flip_image = False

    def update(self, event, keys, dt, room):
        # Hitbox Update
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.new_x = self.x
        self.new_y = self.y

        # Player Input
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.new_x += self.x_speed * dt
            self.flip_image = False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.new_x -= self.x_speed * dt
            self.flip_image = True
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or keys[pygame.K_UP]):
            if self.on_ground:
                # JUMP MECHANIC NEEDS ADJUSTING FOR DIFFERING FRAMERATE #
                self.y_speed = -350
                self.double_jump = False
            elif self.double_jump:
                self.y_speed = -350
                self.double_jump = False

        # Y - Level Update
        self.y_speed += self.y_acceleration * dt
        self.new_y += self.y_speed * dt

        # Collision Update
        platform_list = room[0]
        self.x_collision = False
        self.y_collision = False
        self.on_ground = False

        # X - Collision
        self.hitbox = pygame.Rect(self.new_x, self.y, self.width, self.height)
        for p in platform_list:
            if p.colliderect(self.hitbox):
                self.x_collision = True
                break
        if not self.x_collision:
            self.x = self.new_x

        # Y - Collision
        self.hitbox = pygame.Rect(self.x, self.new_y, self.width, self.height)
        for p in platform_list:
            if p.colliderect(self.hitbox):
                self.on_ground = True
                self.y_collision = True
                self.y_speed = 0
                if p[1] >= self.new_y:
                    self.on_ground = True
                    self.double_jump = False
                if p[1] > self.y + self.height:
                    self.y = p[1] - self.height
                break
        if not self.y_collision:
            self.y = self.new_y

    def draw(self, surface, image):
        image = pygame.transform.flip(image, self.flip_image, False)

        surface.blit(image, (self.x, self.y - 5))


class Items:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 40, 60)
        self.read = False
        self.interact = False
        self.draw_text = False
        self.message = ''

    def update(self, player):
        if self.interact and self.rect.colliderect(player.hitbox):
            self.draw_text = True
        else:
            self.draw_text = False
