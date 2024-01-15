import gspread
from scanner import Scanner
from pdf2image import convert_from_path
import numpy as np
import re

class Database(object):
    def __init__(self, document):
        self.key = "service_key.json"
        
        self.sa = gspread.service_account(filename=self.key)
        self.document = self.sa.open(document)
        
        self.runners = Runners(self.document)
        self.worksheets = {}

        for worksheet in self.document.worksheets():
            if len(worksheet.title) >= 15:
                continue
            print(worksheet.title)

            if (worksheet.title == "Runners"):
                continue
            
            self.addSheet(worksheet.title, worksheet.get("A4:I23"))

    def addSheet(self, sheet, data):
        if (len(data) < 2):
            return None

        count = 0
        for things in data[2]:
            if things != '':
                count += 1

        # case 1: time trial
        if (count <= 2):
            self.worksheets[sheet] = SheetTimeTrial(sheet, self.document)
            self.worksheets[sheet].readSheet()
        # case 2: repeats
        else:
            self.worksheets[sheet] = SheetRepeats(sheet, self.document)
            

class Runners(object):
    def __init__(self, document):
        self.worksheet = document.worksheet("Runners")

        self.runners = []
        self.names = []

        self.loadRunnerFromDatabase()

    def getCell(self, cellNum):
        return self.worksheet.acell(cellNum).value
    
    def getCells(self, cellRange):
        return self.worksheet.get(cellRange)
    
    def updateCell(self, cellRange, value):
        return self.worksheet.update(cellRange, value)
    
    def loadRunnerFromDatabase(self):
        self.data = self.getCells("A1:H200")
        i = 0
        while (i < len(self.data)):
            
            records = []
            for j in range(1, len(self.data[i])):
                record = Record(self.data[0 + i][j], self.data[1 + i][j], self.data[2 + i][j], self.data[3 + i][j])
                records.append(record)

            name = self.data[i][0]
            runner = (name, records)
            self.names.append(name)
            self.runners.append(runner)
            i += 4

    def saveRunner(self, name, record):
        if (name == ''):
            return None
        if name in self.names:
            index = self.names.index(name)

            records = self.runners[index]
            newCol = len(records[1]) + 1

            rangeColumn = chr(65 + newCol) # using the ascii table to find the range for columns
            
            cellRange = rangeColumn + str(index*4 + 1) + ":" + rangeColumn + str(index * 4 + 4)

            self.updateCell(cellRange, [[record[0]], [record[1]], [record[2]], [record[3]]])
            
            print(records)
            records[1].append(Record(record[0], record[1], record[2], record[3]))

            self.runners[index] = records
        else:
            index = len(self.names)
            
            nameCellRange = "A" + str(index * 4 + 1) + ":" + "A" + str(index * 4 + 1)
            self.updateCell(nameCellRange, name)

            recordCellRange = "B" + str(index * 4 + 1) + ":" + "B" + str(index * 4 + 4)
            self.updateCell(recordCellRange, [[record[0]], [record[1]], [record[2]], [record[3]]])

            record = [Record(record[0], record[1], record[2], record[3])]
            self.runners.append((name, record))
            self.names.append(name)
    def writeRunnerToScreen(self, name):
        index = self.names.index(name)
        runner = self.runners[index]

        


class Record(object):
    def __init__(self, date, type, onekTime, recordedTime):
        self.date = date
        self.type = type
        self.onekTime = onekTime
        self.recordedTime = recordedTime

    def getDate(self):
        return self.date
    
    def getType(self):
        return self.type

    def getOneKTime(self):
        return self.onekTime
    
    def getRecordedTime(self):
        return self.recordedTime


class Sheet(object):
    def __init__(self):
        self.sheetName = ""
        self.worksheet = None
        self.numOfNames = 0
        self.numOfRecords = 1

        self.data = [[]]

    def __init__(self, sheetName, document):
        self.sheetName = sheetName

        try:
            self.worksheet = document.worksheet(sheetName)
        except:
            self.worksheet = document.add_worksheet(title=sheetName, rows=100, cols=20) 

        self.numOfNames = 0
        self.numOfRecords = 1

        self.data = [[]]

    def getCell(self, cellNum):
        return self.worksheet.acell(cellNum).value
    
    def getCells(self, cellRange):
        return self.worksheet.get(cellRange)
    
    def updateCell(self, cellRange, value):
        return self.worksheet.update(cellRange, value)
    
    def sortByName(self): # selection sort
        n = self.numOfNames - 1 # set n to the length of the array
        while (n > 0):
            maxIndex = 0

            for i in range(n):
                if self.data[i][0][0] > self.data[maxIndex][0][0]: # comparing the names 
                    maxIndex = i

            # swap elements of index n and index maxIndex
            temp = self.data[maxIndex]
            self.data[maxIndex] = self.data[n]
            self.data[n] = temp

            n -= 1

    def sortByAvgTime(self): # selection sort
        n = self.numOfNames - 1
        while (n > 0):
            maxIndex = 0

            for i in range(n):
                if self.data[i][1] > self.data[maxIndex][1]: # comparing the avgtime 
                    maxIndex = i

            # swap elements of index n and index maxIndex
            temp = self.data[maxIndex]
            self.data[maxIndex] = self.data[n]
            self.data[n] = temp

            n -= 1

    def pasteSheet(self, data, typee, date):
        return None

class SheetTimeTrial(Sheet):
    def __init__(self, sheetName, document):
        super().__init__(sheetName, document)
        self.data = [[]]

    def pasteSheet(self, data, type, date, database):
        numRunners = len(data)
        numRecords = len(data[0])

        #type of workout
        self.worksheet.merge_cells("A1:D2", merge_type='MERGE_ALL')
        self.updateCell("A1:A1", "5k Time Trial")

        #date of workout
        self.worksheet.merge_cells("E1:H2", merge_type='MERGE_ALL')
        self.updateCell("E1:E1", date)

        # (name / records)
        self.updateCell("A3:A3", "Names")
        
        rangeRow = 3 + numRunners # 3 being the start of the data input
        rangeColumn = chr(64 + numRecords)

        cellRange = "A4:" + rangeColumn + str(rangeRow)
        print(cellRange)
        print(len(data))
        print(len(data[0]))

        self.updateCell(cellRange, data)

        self.updateCell("I1:I1", "Number of Runners: " + str(numRunners))

        self.rawData = data
        self.calculateAvgTime()

        # update the runners database
        for runner in self.data:
            print(runner)
            record = [date[5:], type[5:], runner[1], runner[0][1]]
            print(record)
            database.runners.saveRunner(runner[0][0], record)

    def readSheet(self):
        self.rawData = self.getCells(f"A4:I30") # automatically cuts off at a None record 

        self.numOfNames = len(self.rawData)
        self.numOfRecords = len(self.rawData[0])-1

        self.calculateAvgTime()

    def calculateAvgTime(self):
        self.data = []
        for person in self.rawData:
            try:
                record = person[1].split(":")
                time = int(record[0]) * 60 + int(record[1])
                avg = time / 5

                minute = round(avg // 60)
                second = round(avg % 60)

                avg = f"{minute}:{second}"

                self.data.append((person, avg))
            except:
                print("invalid record")
        

class SheetRepeats(Sheet):
    def __init__(self, sheetName, document):
        super().__init__(sheetName,document)
        self.data = [[]]

    def pasteSheet(self, data, typee, date, database): 
        
        numRunners = len(data)
        numRecords = len(data[0])

        #type of workout
        self.worksheet.merge_cells("A1:D2", merge_type='MERGE_ALL')
        self.updateCell("A1:A1", typee)

        #date of workout
        self.worksheet.merge_cells("E1:H2", merge_type='MERGE_ALL')
        self.updateCell("E1:E1", date)

        # (name / records)
        self.updateCell("A3:A3", "Names")
        
        for i in range(numRecords-1):
            cell = chr(66 + i)+"3"
            self.updateCell(f"{cell}:{cell}", str(i+1))

        rangeRow = 3 + numRunners # 3 being the start of the data input
        rangeColumn = chr(64 + numRecords) # using the ascii table to find the range for columns

        cellRange = "A4:" + rangeColumn + str(rangeRow)

        self.updateCell(cellRange, data)

        self.updateCell("I1:I1", "Number of Runners: " + str(numRunners))
        self.updateCell("I2:I2", "Number of Records: " + str(numRecords-1))

        self.rawData = data

        self.calculateAvgTime()

        for i, runner in enumerate(self.data):
            print(runner)
            record = [date[5:], typee[5:], self.otheravg[i], runner[1]]
            print(record)
            database.runners.saveRunner(runner[0][0], record)

        self.readSheet()

    def readSheet(self):
        self.rawData = self.getCells(f"A4:I30") # automatically cuts off at a None record 

        self.numOfNames = len(self.rawData)
        self.numOfRecords = len(self.rawData[0])-1

        type = self.getCells("A1:D2")
        self.distance = int(re.sub('\D', '', type[0][0]))
        if self.distance == 0:
            self.distance = 1

        self.calculateAvgTime()


    def calculateAvgTime(self):
        self.data = []
        self.otheravg = []
        for person in self.rawData:
            records = person[1:]
            sum = 0
            count = 0
            for time in records:
                # convert time to float
                try:
                    sum += float(time)
                    count += 1
                except:
                    print("Invalid record") # there are cases where a random character goes in the thing

            self.avg = round(sum / count, 2)
            otheravg = round(sum / count * (1000/400), 2)
            self.otheravg.append(otheravg)
            

            self.data.append((person, self.avg))

    
if __name__ == "__main__":
    database = Database("Test")
    database.addSheet("One")

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