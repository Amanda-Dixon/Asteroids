import pygame
from circleshape import CircleShape
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    print(f"Starting Asteroids! with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    player = Player(x, y)
    asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        for to_draw in drawable:
            to_draw.draw(screen)

        for to_update in updatable:
            to_update.update(dt)

        for asteroid in asteroids:
            if CircleShape.collides_with(player, asteroid):
                log_event("player_hit")
                print("Game Over!")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if CircleShape.collides_with(shot, asteroid):
                    log_event("asteroid_split")
                    shot.kill()
                    Asteroid.split(asteroid)

        pygame.display.flip()

        log_state()

        # limit framerate to 60 FPS
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
