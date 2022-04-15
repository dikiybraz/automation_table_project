import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import gdspy
from PIL import Image

def get_coords(image_path):

    # Считывание изображения в формате BGR (формат по умолчанию в cv2)
    image = cv2.imread(image_path)

    # Перевод в другой цветовой формат HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Первая компонента hue (оттенок) - красный цвет находится в промежутке 340-360 и 0-20 (так как у нас на картинке нет других ярко выраженных цветов, мы можем взять весь диапазон hue)
    # Вторая компонента saturation (насыщенность)
    # Третья компонета value (яркость)
    lower_red = np.array([0,100,100])
    upper_red = np.array([360,255,255])

    # Получили маскуу, то есть выбрали только те пиксели, которые нужны для дальнейшего анализа
    mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Наложили маску (это логическое И между маской и картинкой)
    output = cv2.bitwise_and(image, image, mask=mask)

    # Берется только красный канал
    # На выходе будет матрица из True и False, которая затем переводится в 0 и 1 методом astype
    red_thresh = (output[..., 2] > 200).astype(np.uint8) 

    # Находим все возможные контуры на бинарной маске
    contours, hierarchy = cv2.findContours(red_thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    # На выходе будет нужна только переменная contours, которая будет хранить список контуров
    
    coords = [] # Массив, в котором будут храниться координаты прямоугольников для каждого устройства
    for contour in contours: # Пробег по всем контурам, чтобы найти только нужные
        if len(contour) > 35 and len(contour) < 65: # Длина контура (соответствует дифракционным решеткам)
            x, y, w, h = cv2.boundingRect(contour) # Считываем по 4 координаты каждого контура, удовлетворяющего условию
            device_coords = [x, y, w, h]
            coords.append(device_coords) # Добавляем координаты в список

    return coords, red_thresh

def draw_bounding_boxes(image_path, coords):
    image = cv2.imread(image_path)
    
    # Переворачиваем ось y
    ax = plt.axis()
    plt.axis((ax[0],ax[1],ax[3],ax[2])) 
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Перевод изображения из BGR в RGB
    for coord in coords: # Пробег по координатам контуров для отрисовки прямоугольников
        x, y, w, h = coord
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2) # Отрисовка прямоугольников

    plt.figure(figsize=(34, 18)) # Размер выводимой картинки    
    plt.imshow(image)
        
    coordinates = [(x[0] + x[2] / 2, x[1] + x[3] / 2) for x in coords] # Координаты центров боксов
    for coord in coordinates:
        plt.scatter(coord[0], coord[1]) # Построение точек coordinates в прямоугольниках
        
    # Переворачиваем ось y
    ax = plt.axis()
    plt.axis((ax[0],ax[1],ax[3],ax[2])) 
        
def save_image_from_gds(file_path):

    gdsii = gdspy.GdsLibrary(infile=file_path) # Считывание gds файла
    main_cell = gdsii.top_level()[0]

    polygons = main_cell.get_polygons()
    res = np.vstack(polygons)

    plt.figure(figsize=(34, 18))
    plt.scatter(res[:, 0], res[:, 1], color='red')
    plt.axis('off')
    
    # Переворачиваем ось y
    ax = plt.axis()
    plt.axis((ax[0],ax[1],ax[3],ax[2])) 

    plt.savefig('out.png', bbox_inches = 'tight', pad_inches = 0)
    
    # Меняем размер изображения в соответствии с GDS файлом
def resize_image(input_image_path, output_image_path, size):
    
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    
    #resized_image.show()
    resized_image.save(output_image_path)
 
    # Обрезаем лишние участки изображения из GDS файла
def image_crop(input_image_path, output_image_path, left, top, right, bottom):

    original_image = Image.open(input_image_path)
    cropped_image = original_image.crop((left, top, right, bottom))
    
    cropped_image.save(output_image_path)


GDS_FILENAME = 'chip.gds'
save_image_from_gds(GDS_FILENAME)
input_image_path = 'out.png'

resize_image(input_image_path='out.png',
             output_image_path='resized.png',
             size=(1960, 650))

image_crop(input_image_path='resized.png',
           output_image_path='cropped.png',
           left = 80, top = 0, right = 1880, bottom = 650)

coords, red = get_coords('cropped.png')
draw_bounding_boxes('cropped.png', coords)


coordinates = [(x[0] + x[2] / 2, x[1] + x[3] / 2) for x in coords] # Координаты центров боксов

with open('data.json', 'w') as f: # Сохранение coordinates в файл data.json
    json.dump(coordinates, f)
    
with open('data.json') as fh: # Считывание координат из файла
    a = json.load(fh)

with open('file.txt', 'w') as fw: # Записываем координаты центров боксов в файл
    json.dump(a, fw)