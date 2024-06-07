import pygame
from pygame.locals import QUIT
import os
from simulation import makePlot, pointGenerator, isInCenter

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetrahedron Simulation")

IMAGE_DIR = 'simulation_images'

def main():
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    index = 0
    inside_count = 0
    total_iterations = 0  
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        points = pointGenerator()
        inside = isInCenter(points)
        if inside:
            inside_count += 1
        total_iterations += 1
        probability = inside_count / total_iterations  # Calculate probability

        makePlot(points, index, inside, probability)

        image_path = os.path.join(IMAGE_DIR, f'tetrahedron_{index}.png')
        if os.path.exists(image_path):
            image = pygame.image.load(image_path)
            screen.fill((255, 255, 255))
            screen.blit(image, (0, 0))

            font = pygame.font.Font(None, 36)
            text = font.render(f"Image: {index} Probability: {probability:.2f}", True, (0, 0, 0))
            screen.blit(text, (10, 10))

            pygame.display.flip()

            index += 1

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
