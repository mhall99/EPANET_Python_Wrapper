# -*- coding: utf-8 -*-

import os
import epanet.toolkit as en
from test.data import example_1_path


timesteps = [3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 1954, 1646, 3600,
             3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 2490, 1110, 3600, 0]
wq_times = [86100, 85800, 85500, 85200, 84900, 84600, 84300, 84000, 83700, 83400, 83100, 82800, 82500, 82200, 81900,
            81600, 81300, 81000, 80700, 80400, 80100, 79800, 79500, 79200, 78900, 78600, 78300, 78000, 77700, 77400,
            77100, 76800, 76500, 76200, 75900, 75600, 75300, 75000, 74700, 74400, 74100, 73800, 73500, 73200, 72900,
            72600, 72300, 72000, 71700, 71400, 71100, 70800, 70500, 70200, 69900, 69600, 69300, 69000, 68700, 68400]


def clean_dir():
    if os.path.exists('report.rpt'):
        os.remove('report.rpt')
    if os.path.exists('output.out'):
        os.remove('output.out')
    if os.path.exists('saved_inp_file.inp'):
        os.remove('saved_inp_file.inp')

#injects chlorine at node 2
def inject_chlorine():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.setqualtype(ph=epanet_proj, qualType=1, chemName='Chlorine', chemUnits='mg/L', traceNode=None)
    num_nodes = en.getcount(ph=epanet_proj, object=en.NODECOUNT)
    num_links = en.getcount(ph=epanet_proj, object=en.LINKCOUNT)
    tlist = []
    en.openH(ph=epanet_proj)
    en.initH(ph=epanet_proj, initFlag=0)
    print('Printing hydraulic time step:')
    while True:
        en.runH(ph=epanet_proj)
        t = en.nextH(ph=epanet_proj)
        print(t)
        tlist.append(t)
        if t <= 0:
            break
    assert tlist == timesteps 
    en.openQ(ph=epanet_proj)
    node_2 = en.getnodeindex(ph=epanet_proj, id='2')
    print('Node 2 index is %d' % (node_2))
    #sets node 2 as Mass Booster 
    en.setnodevalue(ph=epanet_proj, index=node_2, property=en.SOURCETYPE, value=1)
    en.setnodevalue(ph=epanet_proj, index=node_2, property=en.SOURCEQUAL, value=10)
    en.initQ(ph=epanet_proj, saveFlag=1)
    node_qual = en.getnodevalue(ph=epanet_proj, index=node_2, property=en.SOURCEQUAL)
    print('Node 2: %5.2f' % (node_qual)) 
    print('Printing chlorine concentration in nodes')
    while True:
        en.runQ(ph=epanet_proj)
        t = en.nextQ(ph=epanet_proj)
        for i in range(1, num_nodes+1):
            node_qual = en.getnodevalue(ph=epanet_proj, index=i, property=en.MASS)
            print('Node %d: %5.2f' % (i, node_qual))
        if t <= 0:
            break
    en.closeH(ph=epanet_proj)
    en.closeQ(ph=epanet_proj)
    en.close(ph=epanet_proj)
    clean_dir()




