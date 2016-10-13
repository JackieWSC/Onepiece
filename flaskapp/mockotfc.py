class OTFC:
    def __intit__(self):
        self.name = "mock"

    def GetNotificationFiles(self):
        files = ["xxxx.xml","yyy.xml","zzz.xml"]
        return files


    def GetRicList(self):
        ricLists = ["0005.hk","HSIV5", "HSIV6"]
        return ricLists

    
    def GetRecordByRic(iself,ric):
        record = { "1":"A", "2":"B", "3":"C", "4":"D"}
        return record
