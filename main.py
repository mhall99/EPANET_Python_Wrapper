# EPAENT PYTHON PROJECT FOR WATER RESEARCH
# SHEN WANG
# MACKENZIE
# TIME: 08/08/2020

from test import *
from test import Example_owa_epanet
from test import Chlorine_owa_epanet
from test import SourceQual_owa_epanet
from test.data import *
if __name__ == '__main__':
    Example_owa_epanet.test_run_project()
    Example_owa_epanet.test_get_count()
    #Example_owa_epanet.test_inith_runh_nexth()
    #Example_owa_epanet.test_hydraulic()
    #Example_owa_epanet.test_water_quality()
    #injects 10mg of chlorine at nodeID 2 
    SourceQual_owa_epanet.inject_chlorine('2', 10)
    SourceQual_owa_epanet.setNodeSourceQuality('2', 10)
    #SourceQual_owa_epanet.getNodeSourceQuality(11)
    #Chlorine_owa_epanet.test_water_quality()
