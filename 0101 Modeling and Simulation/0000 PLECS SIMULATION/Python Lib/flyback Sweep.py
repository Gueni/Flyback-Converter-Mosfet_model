
#?----------------------------------------------------------------------------------------------------------------------------------------
#?                                      ______      __               __
#?                                     / __/ /_  __/ /_  ____ ______/ /__   ______      _____  ___  ____
#?                                    / /_/ / / / / __ \/ __ `/ ___/ //_/  / ___/ | /| / / _ \/ _ \/ __ \
#?                                   / __/ / /_/ / /_/ / /_/ / /__/ ,<    (__  )| |/ |/ /  __/  __/ /_/ /
#?                                  /_/ /_/\__, /_.___/\__,_/\___/_/|_|  /____/ |__/|__/\___/\___/ .___/
#?                                        /____/                                                /_/
#?                                  
#?----------------------------------------------------------------------------------------------------------------------------------------
import plecs as plc
import Model_Parameters as mdl
import numpy as np 
import post_process
#?----------------------------------------------------------------------------------------------------------------------------------------
port                = "1080"                                                               
url                 = f"http://localhost:{port}/RPC2"                                      
mdlvar              = mdl.ModelVars                                                        
modelname           = "flyback" 
Rsunb               = (np.arange(1    ,100    +10    ,10    )).tolist()
Csnub               = (np.arange(1    ,10     +1     ,1     )*1e-6).tolist()
plcsim              = plc.simpy(url=url , port=port , path=mdl.model_directory , modelvar=mdlvar)   
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim.rpc_connect()                                                                    
plcsim.load_model()
plcsim.ClearAllTraces(mdl.scopes)
for i, item1 in enumerate(Rsunb):
    for j, item2 in enumerate(Csnub):
        mdlvar['RC_snub']['Rsnub']              = Rsunb[i]
        mdlvar['RC_snub']['Csnub']['Cap_s']     = Csnub[j]
        plcsim.logParams(mdlvar['ToFile']['logfile'],mdlvar)
        plcsim.Set_sim_param()
        plcsim.launch_sim(modelname=modelname)
        plcsim.HoldAllTraces(mdl.scopes)
        # plcsim.saveAllTraces(mdlvar['scopes'],mdl,mdlvar['ToFile']['Traces'])
        post_process.gen_plots(resFile= mdlvar['ToFile']['ToFile_path'], html_file=mdlvar['ToFile']['output_html'],OPEN=False)
#?----------------------------------------------------------------------------------------------------------------------------------------


