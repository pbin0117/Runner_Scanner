import gspread
from scanner import Scanner
from pdf2image import convert_from_path
import numpy as np

class Database(object):
    def __init__(self, document):
        self.key = "service_key.json"
        
        self.sa = gspread.service_account(filename=self.key)
        self.document = self.sa.open(document)

        self.worksheets = {}


    def addSheet(self, sheet):
        self.worksheets[sheet] = Sheet(sheet, self.document)

    
class Sheet(object):
    def __init__(self, sheetName, document):
        self.sheetName = sheetName

        try:
            self.worksheet = document.worksheet(sheetName)
        except:
            self.worksheet = document.add_worksheet(title=sheetName, rows=100, cols=20) 

    def getCell(self, cellNum):
        return self.worksheet.acell(cellNum).value
    
    def getCells(self, cellRange):
        return self.worksheet.get(cellRange).value
    
    def updateCell(self, cellRange, value):
        return self.worksheet.update(cellRange, value)
    
    def pasteSheet400(self, data): # probably will have to put these in subclasses for more specialized methods
        
        numRunners = len(data)
        numRecords = len(data[0])

        #type of workout
        self.worksheet.merge_cells("A1:D2", merge_type='MERGE_ALL')
        self.updateCell("A1:A1", "Type: 400m repeats")

        #date of workout
        self.worksheet.merge_cells("E1:H2", merge_type='MERGE_ALL')
        self.updateCell("E1:E1", "Date: 9/10/2023")

        # (name / records)
        self.updateCell("A3:A3", "Names")
        
        for i in range(numRecords-1):
            cell = chr(66 + i)+"3"
            self.updateCell(f"{cell}:{cell}", str(i+1))


        

        rangeRow = 3 + numRunners # 3 being the start of the data input
        rangeColumn = chr(64 + numRecords) # using the ascii table to find the range for columns

        cellRange = "A4:" + rangeColumn + str(rangeRow)

        self.updateCell(cellRange, data)

    def readSheet400(self):
        pass


if __name__ == "__main__":
    for i in range(8):
            cell = chr(66 + i)+"3"
            print(f"{cell}:{cell}")
            
    # src = "Test_Simple.pdf"
    # src = np.array(convert_from_path(src)[0])

    # scanner = Scanner(src)
    # data = scanner.extract_records()

    # database = Database("Test")
    # database.addSheet("Sheet1")

    # testData = [['', '5.46', '4.3', '3.2', '4.3', '24', '3.1', '4.5', '3.1'], 
    #             ['Sammy', '1.2', '3.6', '2.1', '6.4', '10.4', '111.1', '2.3', '4'], 
    #             ['Harold', '4.1', '2,3', '10.2', '99.1', '7.2', '41', '23', ''],]

    # database.worksheets["Sheet1"].pasteSheet400(data)

    






# print("Rows: ", wks.row_count)
# print("Cols: ", wks.col_count)

# print(wks.acell('A9').value)
# print(wks.get('A7:E9'))
# # print(wks.get_all_records())

# wks.update('A1', 'Heeyy')
# wks.update('B1:C2', [['1', '2'], ['3', '4']])