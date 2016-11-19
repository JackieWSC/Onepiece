class Row:
    def __init__(self, jpd, hkd, bold):
        self.jpd = jpd
        self.hkd = hkd
        self.bold = bold

    def __str__(self):
        return "Row({0}, {1}, {2})".format(self.jpd, self.hkd, self.bold)


class Group:
    def __init__(self, name, begin, end, interval, highlight, rate):
        self.name = name
        self.begin = begin
        self.end = end
        self.interval = interval
        self.highlight = highlight
        self.rate = rate
        self.rowList = []
        self.CreateRowList()

    def CreateRowList(self):
        for i in range(self.begin, self.end + self.interval, self.interval):
            bold = False
            if ( i % self.highlight == 0 ):
                bold = True

            self.rowList.append( Row( i, round(i * self.rate,1), bold ) )

    def PrintRowList(self):
        for i in self.rowList:
            print i

    def GetRowList(self):
        return self.rowList

    def __str__(self):
        return "Group({0}, {1}, {2})".format(self.name, self.begin, self.interval)


class jpy2hkd:
    def __init__(self):
        self.jpy2hkdrate = 0.0075
        self.groupName = []
        self.groupMap = {}

    def AddGroup(self, name, group):
        self.groupName.append(name)
        self.groupMap[name] = group

    def GetGroup(self):
        return self.groupName

    def GetGroupMap(self, groupName):
        return self.groupMap[groupName]


# Testing
# g1 = Group("100", 100, 1000, 50, 50, 0.075)
# g2 = Group("1000", 1000, 10000, 100, 1000, 0.075)
# g3 = Group("10000", 10000, 30000, 1000, 1000, 0.075)

# main = jpy2hkd()
# main.AddGroup("100",g1)
# main.AddGroup("1000",g2)
# main.AddGroup("10000",g3)

# print g1
# g1.PrintRowList()
# print main.GetGroup()
# print main.GetGroupMap("100").PrintRowList()
# print main.GetGroupMap("1000").PrintRowList()

