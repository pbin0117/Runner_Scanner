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
        self.worksheet = document.worksheet(sheetName)

    def getCell(self, cellNum):
        return self.worksheet.acell(cellNum).value
    
    def getCells(self, cellRange):
        return self.worksheet.get(cellRange).value
    
    def updateCell(self, cellRange, value):
        return self.worksheet.update(cellRange, value)
    
    def pasteSheet400(self, data): # probably will have to put these in subclasses for more specialized methods
        numRunners = len(data)
        numRecords = len(data[0])

        rangeRow = 3 + numRunners # 3 being the start of the data input
        rangeColumn = chr(64 + numRecords) # using the ascii table to find the range for columns

        cellRange = "A4:" + rangeColumn + str(rangeRow)

        self.updateCell(cellRange, data)


if __name__ == "__main__":
    src = "Test_Simple.pdf"
    src = np.array(convert_from_path(src)[0])

    scanner = Scanner(src)
    data = scanner.extract_records()

    database = Database("Test")
    database.addSheet("Sheet1")

    testData = [['', '5.46', '4.3', '3.2', '4.3', '24', '3.1', '4.5', '3.1'], 
                ['Sammy', '1.2', '3.6', '2.1', '6.4', '10.4', '111.1', '2.3', '4'], 
                ['Harold', '4.1', '2,3', '10.2', '99.1', '7.2', '41', '23', ''],]

    database.worksheets["Sheet1"].pasteSheet400(data)

    






# print("Rows: ", wks.row_count)
# print("Cols: ", wks.col_count)

# print(wks.acell('A9').value)
# print(wks.get('A7:E9'))
# # print(wks.get_all_records())

# wks.update('A1', 'Heeyy')
# wks.update('B1:C2', [['1', '2'], ['3', '4']])