from PIL import Image
import cv2
from pdf2image import convert_from_path
import numpy as np

import pytesseract

from preprocessing import get_grayscale, get_binary, invert_area, draw_text


# source: https://fazlurnucom.wordpress.com/2020/06/23/text-extraction-from-a-table-image-using-pytesseract-and-opencv/
class Scanner:
    def __init__(self, src):
        self.src = src

        self.keywords = ['Type', 'Date', 'Names', 'Fist', 'Second', 'Third', 
                         'Fourth', 'Fifth', 'Sixth', 'Seventh' ,'Eighth']
        
    def is_vertical(self, line):
        return line[0]==line[2]

    def is_horizontal(self, line):
        return line[1]==line[3]
        
    def overlapping_filter(self, lines, sorting_index):
        filtered_lines = []
        
        lines = sorted(lines, key=lambda lines: lines[sorting_index])
        
        for i in range(len(lines)):
                l_curr = lines[i]
                if(i>0):
                    l_prev = lines[i-1]
                    if ( (l_curr[sorting_index] - l_prev[sorting_index]) > 5):
                        filtered_lines.append(l_curr)
                else:
                    filtered_lines.append(l_curr)
                    
        return filtered_lines
    
    def detect_lines(self, title='default', rho = 1, theta = np.pi/180, threshold = 50, minLinLength = 290, maxLineGap = 6, display = False, write = False):
        # Check if image is loaded fine
        gray = cv2.cvtColor(self.src, cv2.COLOR_BGR2GRAY)
        
        if gray is None:
            print ('Error opening image!')
            return -1
        
        dst = cv2.Canny(gray, 50, 150, None, 3)
        
        # Copy edges to the images that will display the results in BGR
        cImage = np.copy(self.src)
        
        #linesP = cv.HoughLinesP(dst, 1 , np.pi / 180, 50, None, 290, 6)
        linesP = cv2.HoughLinesP(dst, rho , theta, threshold, None, minLinLength, maxLineGap)
        
        horizontal_lines = []
        vertical_lines = []
        
        if linesP is not None:
            #for i in range(40, nb_lines):
            for i in range(0, len(linesP)):
                l = linesP[i][0]

                if (self.is_vertical(l)):
                    vertical_lines.append(l)
                    
                elif (self.is_horizontal(l)):
                    horizontal_lines.append(l)
            
            horizontal_lines = self.overlapping_filter(horizontal_lines, 1)
            vertical_lines = self.overlapping_filter(vertical_lines, 0)
                
        if (display):
            for i, line in enumerate(horizontal_lines):
                cv2.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,255,0), 3, cv2.LINE_AA)
                
                cv2.putText(cImage, str(i) + "h", (line[0] + 5, line[1]), cv2.FONT_HERSHEY_SIMPLEX,  
                        0.5, (0, 0, 0), 1, cv2.LINE_AA) 
                
            for i, line in enumerate(vertical_lines):
                cv2.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv2.LINE_AA)
                cv2.putText(cImage, str(i) + "v", (line[0], line[1] + 5), cv2.FONT_HERSHEY_SIMPLEX,  
                        0.5, (0, 0, 0), 1, cv2.LINE_AA) 
                
            cv2.imshow("Source", cImage)
            #cv.imshow("Canny", cdstP)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        if (write):
            cv2.imwrite("Images/" + title + ".png", cImage)
            
        return (horizontal_lines, vertical_lines)
    
    def get_cropped_image(self, x, y, w, h):
        cropped_image = self.src[ y:y+h , x:x+w ]
        return cropped_image
    
    def get_ROI(self, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index, offset=4):
        x1 = vertical[left_line_index][2] + offset
        y1 = horizontal[top_line_index][3] + offset
        x2 = vertical[right_line_index][2] - offset
        y2 = horizontal[bottom_line_index][3] - offset
        
        w = x2 - x1
        h = y2 - y1
        
        cropped_image = self.get_cropped_image(x1, y1, w, h)
        
        return cropped_image, (x1, y1, w, h)
    
    def extract_records(self, p_display=False):
        horizontal, vertical = self.detect_lines(display=p_display)

        records = []

        # detecting type of workout -- 1h-2h : 0v-4v
        cropped_image, (x, y, w, h) = self.get_ROI(horizontal, vertical, 0, 4, 1, 2)
        text = self.detect(cropped_image, is_number=False)

        records.append(text)

        # detecting date -- 0h-1h : 4v-8v
        cropped_image, (x, y, w, h) = self.get_ROI(horizontal, vertical, 4, 8, 1, 2)
        text = self.detect(cropped_image, is_number=False)

        records.append(text)

        num_rows = len(vertical)
        num_cols = len(horizontal)

        for i in range(4, num_cols-1):
            runner = []
            cropped_image, (x, y, w, h) = self.get_ROI(horizontal, vertical, 0,
                            1, i, i+1)
            
            # remove new line
            text = self.detect(cropped_image, is_number=False)
            text = text.strip("\n") 
            runner.append(text)

            for j in range(1, num_rows-1):
                cropped_image, (x, y, w, h) = self.get_ROI(horizontal, vertical, j,
                            j+1, i, i+1)
                # remove new line
                text = self.detect(cropped_image, is_number=False)
                text = text.strip("\n") 

                if (text == ""):
                    text = self.detect(cropped_image, is_number=True)
                    text = text.strip("\n")
                runner.append(text)

            records.append(runner)

        return records
    
    def detect(self, cropped_frame, is_number = False):
        if (is_number):
            text = pytesseract.image_to_string(cropped_frame,config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.')
        else:
            text = pytesseract.image_to_string(cropped_frame)        
            
        return text

    

if __name__ == "__main__":
    src = "Test_Simple.pdf"
    src = np.array(convert_from_path(src)[0])

    scanner = Scanner(src)
    print(scanner.extract_records(p_display=True))


