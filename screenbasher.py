import pygame
import random
import sys
import threading
import keyboard  # New import

def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def block_system_keys():
    # List of keys to block
    keys_to_block = [
        'windows',   # Windows key
        'esc',       # Escape key
        'alt+tab',   # Alt+Tab combination
        'alt+f4',    # Alt+F4 combination
        'ctrl+esc',  # Ctrl+Escape combination
    ]

    for key_combo in keys_to_block:
        keyboard.block_key(key_combo)

    # Keep the script running to maintain the block
    keyboard.wait('ctrl+c')  # Use Ctrl+C to stop blocking if needed

# Start blocking keys in a separate thread
block_thread = threading.Thread(target=block_system_keys)
block_thread.daemon = True
block_thread.start()

pygame.init()

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
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pressed_keys.add(event.key)

            # Check for exit combination
            if all(key in pressed_keys for key in exit_combination):
                running = False
                break

            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            color = random_color()

            # Randomly choose to draw a circle or rectangle
            if random.choice([True, False]):
                radius = random.randint(10, 50)
                items.append(('circle', color, (x, y), radius))
            else:
                width = random.randint(20, 100)
                height = random.randint(20, 100)
                rect = pygame.Rect(x, y, width, height)
                items.append(('rect', color, rect))

        elif event.type == pygame.KEYUP:
            if event.key in pressed_keys:
                pressed_keys.remove(event.key)

    screen.fill((0, 0, 0))

    # Draw all items
    for item in items:
        if item[0] == 'circle':
            _, color, position, radius = item
            pygame.draw.circle(screen, color, position, radius)
        elif item[0] == 'rect':
            _, color, rect = item
            pygame.draw.rect(screen, color, rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
