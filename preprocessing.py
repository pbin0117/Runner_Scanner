import cv2
import numpy as np
import pytesseract

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def get_binary(image):
    (thresh, blackAndWhiteImage) = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
    return blackAndWhiteImage

def invert_area(image, x, y, w, h, display=False):
    ones = np.copy(image)
    ones = 1
    
    image[ y:y+h , x:x+w ] = ones*255 - image[ y:y+h , x:x+w ] 
    
    if (display): 
        cv2.imshow("inverted", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return image
    


def draw_text(src, x, y, w, h, text):
    cFrame = np.copy(src)
    cv2.rectangle(cFrame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(cFrame, "text: " + text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,  
               2, (0, 0, 0), 5, cv2.LINE_AA)
    
    return cFrame
        
def erode(img, kernel_size = 5):
    kernel = np.ones((kernel_size,kernel_size), np.uint8) 
    img_erosion = cv2.dilate(img, kernel, iterations=2)
    return img_erosion