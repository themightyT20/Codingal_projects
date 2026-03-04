import pygame
pygame.init()

# Window parameters - CHANGED TO 640x480
screen_width, screen_height = 640, 480
display_surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('My first game screen')  # Fixed caption

# Load and scale images
background_image = pygame.transform.scale(pygame.image.load('grey_background.png').convert(), (screen_width, screen_height))
penguin_image = pygame.transform.scale(pygame.image.load('game_screen.png').convert_alpha(), (300, 300))
penguin_rect = penguin_image.get_rect(center=(screen_width // 2, screen_height // 2 - 30))

# Colors
BLUE = (0, 100, 255)  # You can change this color

# Create a rectangle at the center
rect_width, rect_height = 200, 150
rectangle = pygame.Rect(0, 0, rect_width, rect_height)
rectangle.center = (screen_width // 2, screen_height // 2)

# Font for text
font = pygame.font.Font(None, 48)
text = font.render('Welcome to My Game!', True, (255, 255, 255))  # White text
text_rect = text.get_rect(center=(screen_width // 2, 50))

def game_loop():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw background image
        display_surface.blit(background_image, (0, 0))
        
        # Draw the penguin image
        display_surface.blit(penguin_image, penguin_rect)
        
        # Draw rectangle
        pygame.draw.rect(display_surface, BLUE, rectangle)
        
        # Draw text
        display_surface.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

if __name__ == '__main__':
    game_loop()
