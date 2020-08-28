# -*- coding: utf-8 -*-

import os
import epanet.toolkit as en
from test.data import example_1_path

def clean_dir():
    if os.path.exists('report.rpt'):
        os.remove('report.rpt')
    if os.path.exists('output.out'):
        os.remove('output.out')
    if os.path.exists('saved_inp_file.inp'):
        os.remove('saved_inp_file.inp')

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
    #print('End of inject chlorine function.')
    en.closeH(ph=epanet_proj)
    en.closeQ(ph=epanet_proj)
    en.close(ph=epanet_proj)
    clean_dir()

#in progress
#current changes not reflected in project file, reset after function call 
def setNodeSourceQuality(str_nodeID, booster_val):
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.setqualtype(ph=epanet_proj, qualType=1, chemName='Chlorine', chemUnits='mg/L', traceNode=None)
    num_nodes = en.getcount(ph=epanet_proj, object=en.NODECOUNT)
    num_links = en.getcount(ph=epanet_proj, object=en.LINKCOUNT)
    source_ind = en.getnodeindex(ph=epanet_proj, id=str_nodeID)
    '''en.openH(ph=epanet_proj)
    en.initH(ph=epanet_proj, initFlag=0)
    en.openQ(ph=epanet_proj)
    en.initQ(ph=epanet_proj, saveFlag=1)'''
    #setting source_ind as booster, need to find a way to acknowledge pre-set boosters
    #en.setnodevalue(ph=epanet_proj, index=source_ind, property=en.SOURCETYPE, value=1)
    node_type = en.getnodevalue(ph=epanet_proj, index=source_ind, property=en.SOURCETYPE)
    if node_type == 1:
        en.setnodevalue(ph=epanet_proj, index=source_ind, property=en.SOURCEQUAL, value=booster_val)
        print('Node (index %d) source quality set to value %5.2f' % (source_ind, booster_val))
    else:
        print('Specified node is not designated as mass booster.')
    print('End of setNodeSourceQuality function.')
    '''en.closeH(ph=epanet_proj)
    en.closeQ(ph=epanet_proj)
    en.close(ph=epanet_proj)'''
    clean_dir()

def getNodeSourceQuality():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.setqualtype(ph=epanet_proj, qualType=1, chemName='Chlorine', chemUnits='mg/L', traceNode=None)
    num_nodes = en.getcount(ph=epanet_proj, object=en.NODECOUNT)
    source_qual_list = []
    en.openH(ph=epanet_proj)
    en.initH(ph=epanet_proj, initFlag=0)
    en.openQ(ph=epanet_proj)
    en.initQ(ph=epanet_proj, saveFlag=1)
    #sets source_ind as booster, need to find a way to acknowledge pre-set boosters
    #en.setnodevalue(ph=epanet_proj, index=source_ind, property=en.SOURCETYPE, value=1)
    for i in range(1, num_nodes+1):
            node_type = en.getnodevalue(ph=epanet_proj, index=i, property=en.SOURCETYPE)
            if node_type == 1:
                source_qual = en.getnodevalue(ph=epanet_proj, index=source_ind, property=en.SOURCEQUAL)
                print('Node (index %d) source quality: %5.2f' % (i, source_qual))
                source_qual_list.append(source_qual)
    print('End of getNodeSourceQuality function.')
    en.closeH(ph=epanet_proj)
    en.closeQ(ph=epanet_proj)
    en.close(ph=epanet_proj)
    clean_dir()


