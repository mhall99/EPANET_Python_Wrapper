# -*- coding: utf-8 -*-

import sys
import os
if 'linux' in sys.platform:
    print("linux platform")
    import epanet.toolkit as en
elif 'darwin' in sys.platform:
    print("mac")
    import epanetMac.toolkit as en
else:
    raise RuntimeError("Unsupported operating system: {}".format(sys.platform))

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

#injects chlorine at given node with given amount
#current changes not reflected in project file, reset after function call 
def inject_chlorine(str_nodeID, booster_val):
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.setqualtype(ph=epanet_proj, qualType=1, chemName='Chlorine', chemUnits='mg/L', traceNode=None)
    num_nodes = en.getcount(ph=epanet_proj, object=en.NODECOUNT)
    num_links = en.getcount(ph=epanet_proj, object=en.LINKCOUNT)
    tlist = []
    en.openH(ph=epanet_proj)
    en.initH(ph=epanet_proj, initFlag=0)
    en.openQ(ph=epanet_proj)
    booster_node = en.getnodeindex(ph=epanet_proj, id=str_nodeID)
    print('Booster node index is %d' % (booster_node))
    #sets node as Mass Booster 
    en.setnodevalue(ph=epanet_proj, index=booster_node, property=en.SOURCETYPE, value=1)
    en.setnodevalue(ph=epanet_proj, index=booster_node, property=en.SOURCEQUAL, value=booster_val)
    en.initQ(ph=epanet_proj, saveFlag=1)
    node_qual = en.getnodevalue(ph=epanet_proj, index=booster_node, property=en.SOURCEQUAL)
    print('Booster node source quality: %5.2f' % (node_qual)) 
    en.closeH(ph=epanet_proj)
    en.closeQ(ph=epanet_proj)
    en.close(ph=epanet_proj)
    clean_dir()




