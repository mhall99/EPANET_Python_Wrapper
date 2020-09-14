import sys

if 'linux' in sys.platform:
    print("linux platform")
    import epanet.toolkit as en
elif 'darwin' in sys.platform:
    print("mac")
    import epanetMac.toolkit as en
else:
    raise RuntimeError("Unsupported operating system: {}".format(sys.platform))

from test.data import example_1_path
import numpy as np
import matplotlib.pyplot as plt

"http://hackage.haskell.org/package/epanet-haskell-2.0.12.4/docs/Epanet.html#v:c_ENgetlinkindex"


class Prj:

    def __init__(self, network):
        classversion = 'v0.1'
        self.TYPELINK = ['CVPIPE', 'PIPE', 'PUMP', 'PRV', 'PSV', 'PBV', 'FCV', 'TCV',
                         'GPV']  # Constants for links: 'CVPIPE', 'PIPE', 'PUMP', 'PRV', 'PSV', 'PBV', 'FCV', 'TCV', 'GPV', 'VALVE'
        TYPEMIXMODEL = ['MIX1', 'MIX2', 'FIFO', 'LIFO']  # Constants for mixing models: 'MIX1', 'MIX2', 'FIFO', 'LIFO'
        self.TYPENODE = ['JUNCTION', 'RESERVOIR', 'TANK']  # Contants for nodes: 'JUNCTION', 'RESERVOIR', 'TANK'
        TYPEPUMP = ['CONSTANT_HORSEPOWER', 'POWER_FUNCTION',
                    'CUSTOM']  # Constants for pumps: 'CONSTANT_HORSEPOWER', 'POWER_FUNCTION', 'CUSTOM'
        TYPEQUALITY = ['NONE', 'CHEM', 'AGE', 'TRACE',
                       'MULTIS']  # Constants for quality: 'NONE', 'CHEM', 'AGE', 'TRACE', 'MULTIS'
        TYPEREPORT = ['YES', 'NO', 'FULL']  # Constants for report: 'YES', 'NO', 'FULL'
        self.TYPESOURCE = ['CONCEN', 'MASS', 'SETPOINT', 'FLOWPACED']  # Constant for sources: 'CONCEN', 'MASS', 'SETPOINT', 'FLOWPACED'
        TYPESTATS = ['NONE', 'AVERAGE', 'MINIMUM', 'MAXIMUM',
                     'RANGE']  # Constants for statistics: 'NONE', 'AVERAGE', 'MINIMUM', 'MAXIMUM', 'RANGE'
        TYPEUNITS = ['CFS', 'GPM', 'MGD', 'IMGD', 'AFD', 'LPS', 'LPM', 'MLD', 'CMH',
                     'CMD']  # Constants  for units: 'CFS', 'GPM', 'MGD', 'IMGD', 'AFD', 'LPS', 'LPM', 'MLD', 'CMH', 'CMD'
        TYPEHEADLOSS = ['HW', 'DW', 'CM']  # Constants of  headloss types: HW: Hazen - Williams, DW: Darcy - Weisbach, CM: Chezy - Manning
        TYPESTATUS = ['CLOSED', 'OPEN']  # Link status
        self.epanet_proj = en.createproject()
        print('Loading:', network)
        en.open(ph=self.epanet_proj, inpFile=network, rptFile='report.rpt', outFile='output.out')
        # Get all the countable network parameters
        self.NodeCount = en.getcount(ph=self.epanet_proj, object=en.NODECOUNT)
        self.TankReservoirCount = en.getcount(ph=self.epanet_proj, object=en.TANKCOUNT)
        self.LinkCount = en.getcount(ph=self.epanet_proj, object=en.LINKCOUNT)
        self.PatternCount = en.getcount(ph=self.epanet_proj, object=en.PATCOUNT)
        self.CurveCount = en.getcount(ph=self.epanet_proj, object=en.CURVECOUNT)
        self.CurveIndex = self.getCurveIndex()
        self.JunctionCount = self.NodeCount - self.TankReservoirCount  # en.getNodeJunctionCount

        self.NodeID = self.getNodeID()
        self.LinkID = self.getLinkID()
        # Get node type index
        self.NodeTypeIndex = self.getNodeTypeIndex()
        self.LinkTypeIndex = self.getLinkTypeIndex()

        # Get type of the parameters
        self.LinkType = self.getLnkType()
        self.NodeType = self.getNodeType()

        self.ReservoirCount = self.getReservoirCount()
        self.TankCount = self.TankReservoirCount - self.ReservoirCount

        self.PumpCount = self.getPumpCount()
        self.PipeCount = self.getPipeCount()
        self.ValveCount = self.LinkCount - self.PumpCount - self.PipeCount

        # Get node index
        self.NodeIndex = list(range(1, self.NodeCount + 1))

        self.JunctionIndex = self.NodeIndex[0:self.JunctionCount]
        self.JunctionID = self.NodeID[0:self.JunctionCount]

        temp = self.JunctionCount + self.ReservoirCount
        self.ReservoirIndex = self.NodeIndex[self.JunctionCount:temp]
        self.ReservoirID = self.NodeID[self.JunctionCount:temp]

        self.TankIndex = self.NodeIndex[temp: temp + self.ReservoirCount]
        self.TankID = self.NodeID[temp: temp + self.ReservoirCount]

        # Get link index
        self.LinkIndex = list(range(1, self.LinkCount + 1))

        self.PipeIndex = self.LinkIndex[0:self.PipeCount]
        self.PipeID = self.LinkID[0:self.PipeCount]

        temp = self.PipeCount + self.PumpCount
        self.PumpIndex = self.LinkIndex[self.PipeCount:temp]
        self.PumpID = self.LinkID[self.PipeCount:temp]

        self.ValveIndex = self.LinkIndex[temp: temp + self.ValveCount]
        self.ValveID = self.LinkID[temp: temp + self.ValveCount]

        print('Loading ends, and ready to go!')

    def getLinkTypeIndex(self):
        value = range(1, self.LinkCount + 1)
        linkTypeIndex = list()
        for i in value:
            type = en.getlinktype(ph=self.epanet_proj, index=i)
            linkTypeIndex.append(type)
        return linkTypeIndex

    def getNodeTypeIndex(self):
        value = range(1, self.NodeCount + 1)
        # print(value)
        nodeTypeIndex = list()
        for i in value:
            # print(i)
            type = en.getnodetype(ph=self.epanet_proj, index=i)
            # print(type)
            nodeTypeIndex.append(type)
        return nodeTypeIndex

    def getNodeID(self):
        value = range(1, self.NodeCount + 1)
        # print(value)
        nodeID = list()
        for i in value:
            # print(i)
            type = en.getnodeid(ph=self.epanet_proj, index=i)
            # print(type)
            nodeID.append(type)
        return nodeID

    def getNodeActualDemand(self):  # todo establish actualdemand list (DONE!)
        value = range(1, self.NodeCount + 1)
        nodeActualDemand = list()
        for i in value:
            # print(i)
            type = en.getnodevalue(ph=self.epanet_proj, index=i, property=en.DEMAND)
            # print(type)
            nodeActualDemand.append(type)
        return nodeActualDemand

    def getNodeQuality(self):  # finds chlorine concentration
        C = np.zeros(shape=self.NodeCount)
        for i in self.NodeIndex:
            # print(i)
            quality = en.getnodevalue(ph=self.epanet_proj, index=i, property=en.QUALITY)
            # print(quality)
            C[i - 1] = quality
        return C

    def getLinkID(self):
        value = range(1, self.LinkCount + 1)
        # print(value)
        linkID = list()
        for i in value:
            # print(i)
            type = en.getlinkid(ph=self.epanet_proj, index=i)
            # print(type)
            linkID.append(type)
        return linkID

    def getPumpCount(self):
        count = 0
        for i in self.LinkTypeIndex:
            if (i == 2):
                count = count + 1
        return count

    def getPipeCount(self):
        count = 0
        for i in self.LinkTypeIndex:
            if (i == 1):
                count = count + 1
        return count

    # useless
    # def getValveCount(self):
    # pass

    def getReservoirCount(self):
        count = 0
        for i in self.NodeTypeIndex:
            if (i == 1):
                count = count + 1
        return count

    def getNodeType(self):
        # print(value)
        nodeType = list()
        for i in self.NodeTypeIndex:
            # print(i)
            type = self.TYPENODE[i]
            # print(type)
            nodeType.append(type)
        return nodeType

    def getLnkType(self):
        # print(value)
        linkType = list()
        for i in self.NodeTypeIndex:
            # print(i)
            type = self.TYPELINK[i]
            # print(type)
            linkType.append(type)
        return linkType

    def getCurveIndex(self, *idTuple):
        # print('input curve:', idTuple)
        if (len(idTuple) == 0):
            value = range(1, self.CurveCount + 1)
        else:
            value = list()
            for idTemp in idTuple:
                cind = en.getcurveindex(ph=self.epanet_proj, id=idTemp)
                value.append(cind)
        return value

    def openHydraulicAnalysis(self):
        en.openH(ph=self.epanet_proj)

    def initializeHydraulicAnalysis(self):
        en.initH(ph=self.epanet_proj, initFlag=0)

    def closeHydraulicAnalysis(self):
        en.closeH(ph=self.epanet_proj)

    def nextHydraulicAnalysisStep(self):
        t = en.nextH(ph=self.epanet_proj)
        # print(t)
        return t

    def runHydraulicAnalysis(self):
        en.runH(ph=self.epanet_proj)

    def solveCompleteHydraulics(self):
        en.solveH(ph=self.epanet_proj)

    def openQualityAnalysis(self):
        en.openQ(ph=self.epanet_proj)

    def initializeQualityAnalysis(self):
        en.initQ(ph=self.epanet_proj, saveFlag=1)

    def closeQualityAnalysis(self):
        en.closeQ(ph=self.epanet_proj)

    def nextQualityAnalysisStep(self):
        t = en.nextQ(ph=self.epanet_proj)
        #print(t)
        return t

    def runQualityAnalysis(self):
        en.runQ(ph=self.epanet_proj)

    def getNodeHydaulicHead(self):
        H = np.zeros(shape=self.NodeCount)
        for i in self.NodeIndex:
            head = en.getnodevalue(ph=self.epanet_proj, index=i, property=en.HEAD)
            H[i - 1] = head
        return H

    def getLinkFlow(self):
        Q = np.zeros(shape=self.LinkCount)
        for i in self.LinkIndex:
            flow = en.getlinkvalue(ph=self.epanet_proj, index=i, property=en.FLOW)
            Q[i - 1] = flow
        return Q

    def setNodeSourceType(self, nodeID, sourceType):
        """
        Set the node with  nodeID as the quality source type value
        0. CONCEN
        1. MASS
        2. SETPOINT
        3. FLOWPACED
        """
        index = self.getNodeIndexbyID(nodeID)
        en.setnodevalue(ph=self.epanet_proj, index=index, property=en.SOURCETYPE, value=sourceType)

    def setNodeSourceQuality(self, nodeID, sourceStrength):
        """
        Set the node with  nodeID as the quality source type value
        """
        index = self.getNodeIndexbyID(nodeID)
        en.setnodevalue(ph=self.epanet_proj, index=index, property=en.SOURCEQUAL, value=sourceStrength)

    def setNodeSourceType_Quality(self, nodeID, sourceTypeString, sourceStrength):
        index = self.getNodeIndexbyID(nodeID)
        assert isinstance(sourceTypeString, str)
        sourceType = self.TYPESOURCE.index(sourceTypeString)
        en.setnodevalue(ph=self.epanet_proj, index=index, property=en.SOURCETYPE, value=sourceType)
        en.setnodevalue(ph=self.epanet_proj, index=index, property=en.SOURCEQUAL, value=sourceStrength)

    def getNodeIndexbyID(self, nodeID):
        index = en.getnodeindex(ph=self.epanet_proj, id=nodeID)
        return index

    def getNodeSourceType(self, nodeID):
        index = self.getNodeIndexbyID(nodeID)
        return en.getnodevalue(ph=self.epanet_proj, index=index, property=en.SOURCETYPE)

    def getNodeSourceQuality(self, nodeID):
        index = self.getNodeIndexbyID(nodeID)
        return en.getnodevalue(ph=self.epanet_proj, index=index, property=en.SOURCEQUAL)


if __name__ == "__main__":
    proj = Prj(example_1_path)
    print('Basic information:')
    print('_______________________________')
    print('Total node count is:', proj.NodeCount)
    print('Total node Index is:', proj.NodeIndex)
    print('Total node ID is:', proj.NodeID)
    print('Total node type index is:', proj.NodeTypeIndex)
    print('Total node type is:', proj.NodeType)
    print('_______________________________')
    print('Total junction count is:', proj.JunctionCount)
    print('Total junction ID is:', proj.JunctionID)
    print('Total Junction type index is:', proj.JunctionIndex)
    print('_______________________________')
    print('Total reservoir count is:', proj.ReservoirCount)
    print('Total reservoir ID is:', proj.ReservoirID)
    print('Total reservoir type index is:', proj.ReservoirIndex)
    print('_______________________________')
    print('Total tank count is:', proj.TankCount)
    print('Total tank ID is:', proj.TankID)
    print('Total tank type index is:', proj.TankIndex)
    print('_______________________________')
    print('Total link count is:', proj.LinkCount)
    print('Total link Index is:', proj.LinkIndex)
    print('Total link ID is:', proj.LinkID)
    print('Total link type index is:', proj.LinkTypeIndex)
    print('Total link type is:', proj.LinkType)
    print('_______________________________')
    print('Total pipe count is:', proj.PipeCount)
    print('Total pipe ID is:', proj.PipeID)
    print('Total pipe type index is:', proj.PipeIndex)
    print('_______________________________')
    print('Total pump count is:', proj.PumpCount)
    print('Total pump ID is:', proj.PumpID)
    print('Total pump type index is:', proj.PumpIndex)
    print('_______________________________')
    print('Total valve count is:', proj.ValveCount)
    print('Total valve ID is:', proj.ValveID)
    print('Total valve type index is:', proj.ValveIndex)
    print('_______________________________')

    print('Total curve count is:', proj.CurveCount)
    print('Start hydraulic simulation:')
    print('_______________________________')
    counterH = 0
    tstep = 1
    T_H = list()
    time_HOURS = 30
    D = np.zeros(shape=(proj.NodeCount, time_HOURS))
    H = np.zeros(shape=(proj.NodeCount, time_HOURS))
    Q = np.zeros(shape=(proj.LinkCount, time_HOURS))
    proj.openHydraulicAnalysis()
    proj.initializeHydraulicAnalysis()
    while True:
        # print(tstep)
        proj.runHydraulicAnalysis()
        head = proj.getNodeHydaulicHead()
        flow = proj.getLinkFlow()
        demand = proj.getNodeActualDemand()
        # print(head)
        H[:, counterH] = head
        Q[:, counterH] = flow
        D[:, counterH] = demand
        counterH = counterH + 1
        tstep = proj.nextHydraulicAnalysisStep()
        T_H.append(tstep)
        if tstep <= 0:
            break

    proj.closeHydraulicAnalysis()
    print('Hydraulic simulation ends')
    print('_______________________________')
    # print(H)
    # print(Q)

    print('Organize data and plot:')
    print('_______________________________')

    # organize data and only keep nonzero data
    H = H[:, 0:counterH]
    Q = Q[:, 0:counterH]
    D = D[:, 0:counterH]
    # print(counterH)
    # print(H[0])

    # plot head for all nodes
    fig1 = plt.figure()
    for nodei in range(0, proj.NodeCount):
        if (proj.NodeTypeIndex[nodei] == 0):
            labelstring = 'J' + proj.NodeID[nodei]
        if (proj.NodeTypeIndex[nodei] == 1):
            labelstring = 'R' + proj.NodeID[nodei]
        if (proj.NodeTypeIndex[nodei] == 2):
            labelstring = 'TK' + proj.NodeID[nodei]
        plt.step(range(0, counterH), H[nodei], label=labelstring)

    plt.title('Heads at all nodes')
    plt.xlabel('Time (hour)')
    plt.ylabel('Head (ft)')
    plt.legend()
    print('close the figure to continue...')
    # plt.show()
    fig1.savefig('head.png')

    # plot flow rates
    fig2 = plt.figure()
    for linki in range(0, proj.LinkCount):
        if (proj.LinkTypeIndex[linki] == 1):
            labelstring = 'P' + proj.LinkID[linki]
        elif (proj.LinkTypeIndex[linki] == 2):
            labelstring = 'Pu' + proj.LinkID[linki]
        else:
            labelstring = 'V' + proj.LinkID[linki]
        plt.step(range(0, counterH), Q[linki], label=labelstring)

    plt.title('Flow rates at all links')
    plt.xlabel('Time (hour)')
    plt.ylabel('Flow (GPM)')
    plt.legend()
    print('close the figure to continue...')
    # plt.show()
    fig2.savefig('Flow.png')

    # todo: plot demand for all nodes (DONE!)
    # plot demand for all nodes
    fig3 = plt.figure()
    for nodei in range(0, proj.NodeCount):
        if (proj.NodeTypeIndex[nodei] == 0):
            labelstring = 'J' + proj.NodeID[nodei]
        if (proj.NodeTypeIndex[nodei] == 1):
            labelstring = 'R' + proj.NodeID[nodei]
        if (proj.NodeTypeIndex[nodei] == 2):
            labelstring = 'TK' + proj.NodeID[nodei]
        plt.step(range(0, counterH), D[nodei], label=labelstring)

    plt.title('Demand at all nodes')
    plt.xlabel('Time (hour)')
    plt.ylabel('Demand (GPM)')
    plt.legend()
    print('close the figure to continue...')
    # plt.show()
    fig3.savefig('demand.png')

    print('Start quality simulation:')
    print('_______________________________')
    # todo: finish quality simulation and collect the concentration at all nodes and in all links
    # todo: plot chlorine concentration  for all nodes and links

    counterQ = 0
    tstep = 1
    T_Q = list()
    time_HOURS = 30
    C = np.zeros(shape=(proj.NodeCount, time_HOURS))
    proj.solveCompleteHydraulics()
    proj.openQualityAnalysis()
    proj.initializeQualityAnalysis()
    #proj.setNodeSourceType('10', 'MASS')
    #proj.setNodeSourceQuality('10', 1000)
    proj.setNodeSourceType_Quality('10', 'MASS', 1000)
    print('The type of node 10 is:', proj.getNodeSourceType('10'))
    print('The strength of node 10 is:', proj.getNodeSourceQuality('10'))

    while True:
        # print(tstep)
        proj.runQualityAnalysis()
        chlorine = proj.getNodeQuality()
        # print(chlorine)
        C[:, counterQ] = chlorine
        counterQ = counterQ + 1
        tstep = proj.nextQualityAnalysisStep()
        T_Q.append(tstep)
        if tstep <= 0:
            break

    proj.closeQualityAnalysis()
    print('Quality simulation ends')
    print('_______________________________')
    print(counterQ)  # only has a 1 in it, due to loop only iterating once
    print(T_Q)  # has a 0 in it, causing the break above
    print('Organize data and plot:')
    print('_______________________________')

    # organize data and only keep nonzero data
    C = C[:, 0:counterQ]

    # plot quality for all nodes
    fig4 = plt.figure()
    # for nodei in range(0, proj.NodeCount):
    for nodei in range(0, 2):
        if (proj.NodeTypeIndex[nodei] == 0):
            labelstring = 'J' + proj.NodeID[nodei]
        if (proj.NodeTypeIndex[nodei] == 1):
            labelstring = 'R' + proj.NodeID[nodei]
        if (proj.NodeTypeIndex[nodei] == 2):
            labelstring = 'TK' + proj.NodeID[nodei]
        plt.plot(range(0, counterQ), C[nodei], label=labelstring)

    plt.title('Quality at all nodes')
    plt.xlabel('Time (hour)')
    plt.ylabel('Chlorine (mg/L)')
    plt.legend()
    print('close the figure to continue...')
    plt.show()
    fig4.savefig('quality.png')
