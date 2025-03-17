import os
import sys
import requests
import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 450
MAP_FILE = "map.png"


def get_coordinates():
    while True:
        coords1 = input('Введите координаты через пробел: ')
        try:
            lat, lon = map(float, coords1.split())
            return f"{lon},{lat}"
        except ValueError:
            print('Координаты введены неверно. Пожалуйста, введите два числа.')


def get_scale():
    while True:
        try:
            scale = int(input('Введите масштаб в %: '))
            if 1 <= scale <= 100:
                return scale
            else:
                print('Масштаб должен быть в диапазоне от 1 до 100.')
        except ValueError:
            print('Масштаб должен быть числом.')


def fetch_map_image(coords, scale):
    url = f"http://static-maps.yandex.ru/1.x/?ll={coords}&z={scale}&size={SCREEN_WIDTH},{SCREEN_HEIGHT}&l=map"
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.RequestException as e:
        print('Ошибка выполнения запроса:', e)
        sys.exit(1)

    with open(MAP_FILE, "wb") as file:
        file.write(r.content)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Карта_2')

    coords = get_coordinates()
    scale = get_scale()
    fetch_map_image(coords, scale)
    map_image = pygame.image.load(MAP_FILE)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN: #Тут отдаление и приближение
                if event.key == pygame.K_PAGEUP:
                    if scale < 17:
                        scale += 1
                        fetch_map_image(coords, scale)
                        map_image = pygame.image.load(MAP_FILE)
                elif event.key == pygame.K_PAGEDOWN:
                    if scale > 1:
                        scale -= 1
                        fetch_map_image(coords, scale)
                        map_image = pygame.image.load(MAP_FILE)

        screen.blit(map_image, (0, 0))
        pygame.display.flip()
        clock.tick(30)

    if os.path.exists(MAP_FILE):
        os.remove(MAP_FILE)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

