import pygame
import random
import sys
import threading
import keyboard
from version import version_string

class Color:
    def __init__(self, r, g, b, alpha=255):
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha

    def to_tuple(self):
        return (self.r, self.g, self.b, self.alpha)

class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.alive = True

    def draw(self, screen):
        pass

    def fade(self, delta):
        z_count = 0
        component_names = ['r', 'g', 'b']
        for comp_name in component_names:
            value = getattr(self.color, comp_name)
            if value > delta:
                value -= delta
            else:
                value = 0
                z_count += 1
            setattr(self.color, comp_name, value)

        if(z_count == len(component_names)):
            self.alive = False

# Circle class derived from shape
class Circle(Shape):
    def __init__(self, x, y, color, radius):
        self.radius = radius
        super().__init__(x, y, color)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color.to_tuple(), (self.x, self.y), self.radius)

# Rectangle class derived from shape
class Rectangle(Shape):
    def __init__(self, x, y, color, width, height):
        self.width = width
        self.height = height
        super().__init__(x, y, color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color.to_tuple(), (self.x, self.y, self.width, self.height))

def random_color():
    return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def block_system_keys():
    # List of keys to block
    keys_to_block = [
        'windows',   # Windows key
        'esc',       # Escape key
    ]

    for key_combo in keys_to_block:
        keyboard.block_key(key_combo)

    # Keep the script running to maintain the block
    keyboard.wait('ctrl+c')  # Use Ctrl+C to stop blocking if needed

if __name__ == "__main__":
    print(f"Screenbasher {version_string}")

    # Start blocking keys in a separate thread
    block_thread = threading.Thread(target=block_system_keys)
    block_thread.daemon = True
    block_thread.start()

    pygame.init()
    pygame.mouse.set_visible(False)

    # Screen setup
    info_object = pygame.display.Info()
    screen_width = info_object.current_w
    screen_height = info_object.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption('Key Basher')

    # Variables
    items = []
    pressed_keys = set()
    exit_combination = [pygame.K_LCTRL, pygame.K_c]

    running = True
    prev_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pressed_keys.add(event.key)

                # Check for exit combination
                if all(key in pressed_keys for key in exit_combination):
                    running = False
                    break

                color = random_color()

                # Randomly choose to draw a circle or rectangle
                if random.choice([True, False]):
                    # Circle
                    radius = random.randint(10, 50)
                    x = random.randint(radius, screen_width - radius)
                    y = random.randint(radius, screen_height - radius)
                    items.append(Circle(x, y, color, radius))
                else:
                    # Rectangle
                    width = random.randint(20, 100)
                    height = random.randint(20, 100)
                    x = random.randint(0, screen_width - width)
                    y = random.randint(0, screen_height - height)
                    rect = pygame.Rect(x, y, width, height)
                    items.append(Rectangle(x, y, color, width, height))

            elif event.type == pygame.KEYUP:
                if event.key in pressed_keys:
                    pressed_keys.remove(event.key)

            elif event.type == pygame.MOUSEMOTION:
                red = Color(255, 0, 0)
                items.append(Circle(event.pos[0], event.pos[1], red, 20))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    green = Color(0, 255, 0)
                    items.append(Circle(event.pos[0], event.pos[1], green, 200))
                elif event.button == 3:  # Right click
                    blue = Color(0, 0, 255)
                    items.append(Circle(event.pos[0], event.pos[1], blue, 200))
                else:
                    # Ignore 2: middle click, 4: scroll wheel up, 5: scroll wheel down
                    pass

            else:
                # Ignore other events
                pass

        screen.fill((0, 0, 0))

        # Implement a 10ms tick
        tick = False
        dt_ms = pygame.time.get_ticks() - prev_time
        if dt_ms > 10:
            tick = True
            prev_time = pygame.time.get_ticks()

        # Draw all items
        for item in items:
            item.draw(screen)

            # Fade on tick
            if tick:
                item.fade(1)

        # remove dead items
        items = [item for item in items if item.alive]

        pygame.display.flip()

    pygame.quit()
    sys.exit()
