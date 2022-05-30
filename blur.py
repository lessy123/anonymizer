# importing cv2 
import cv2 
  
def blur_image(path = r"/home/alex/anonymizer/RAM/1.jpeg"):
    image = cv2.imread(path)     
    ksize = (10, 10)    
    image = cv2.blur(image, ksize)     
    cv2.imwrite(path, image)
    if __name__ == "__main__":    
        print("Изображение обработано")
    #window_name = 'Image'   
    #cv2.imshow(window_name, image) 
    # cv2.waitKey(0)
    #print("Файл сохранен")

if __name__ == "__main__":    
    blur_image()