import pygame
import socket
import json

# ======================
# CONFIG
# ======================
TARGET = ("0.0.0.0", 9999)
SEND_HZ = 30
STEP = 0.05

# ======================
# NETWORK
# ======================
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ======================
# PYGAME INIT
# ======================
pygame.init()
screen = pygame.display.set_mode((420, 240))
pygame.display.set_caption("Machine Controller")

font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# ======================
# JOYSTICK
# ======================
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# ======================
# STATE
# ======================
linear = 0.0
angular = 0.0
running = True

# ======================
# LOOP
# ======================
while running:
    clock.tick(SEND_HZ)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                linear = angular = 0.0

            elif joystick is None:
                if event.key == pygame.K_w:
                    linear += STEP
                elif event.key == pygame.K_s:
                    linear -= STEP
                elif event.key == pygame.K_a:
                    angular += STEP
                elif event.key == pygame.K_d:
                    angular -= STEP

    # -------- INPUT --------
    if joystick:
        linear = -joystick.get_axis(1)
        angular = joystick.get_axis(0)

    # -------- CLAMP --------
    linear = max(-1.0, min(1.0, linear))
    angular = max(-1.0, min(1.0, angular))

    # -------- SEND --------
    msg = {"linear": linear, "angular": angular}
    sock.sendto(json.dumps(msg).encode(), TARGET)

    # -------- DRAW --------
    screen.fill((20, 20, 20))

    def draw_text(text, y):
        img = font.render(text, True, (200, 200, 200))
        screen.blit(img, (20, y))

    draw_text("Machine Controller", 10)
    draw_text(f"Linear  : {linear:+.2f}", 50)
    draw_text(f"Angular : {angular:+.2f}", 80)
    draw_text(f"Input   : {'Joystick' if joystick else 'Keyboard'}", 120)
    draw_text("WASD / Stick to move", 160)
    draw_text("SPACE stop | ESC quit", 185)

    pygame.display.flip()

pygame.quit()
