
#?----------------------------------------------------------------------------------------------------------------------------------------
#?                                                         ______      __               __  
#?                                                        / __/ /_  __/ /_  ____ ______/ /__
#?                                                       / /_/ / / / / __ \/ __ `/ ___/ //_/
#?                                                      / __/ / /_/ / /_/ / /_/ / /__/ ,<   
#?                                                     /_/ /_/\__, /_.___/\__,_/\___/_/|_|  
#?                                                           /____/
#?
#?----------------------------------------------------------------------------------------------------------------------------------------
import plecs as plc
import Model_Parameters as mdl
import post_process
import cleardata
#?----------------------------------------------------------------------------------------------------------------------------------------
port                = "1080"                                                               
url                 = f"http://localhost:{port}/RPC2"                                      
mdlvar              = mdl.ModelVars                                                        
modelname           = "flyback"                                                                
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim              = plc.simpy(url=url , port=port , path=mdl.model_directory , modelvar=mdlvar)    
plcsim.rpc_connect()                                                                       
plcsim.load_model()  
cleardata.clear_data_folders()                                                                  
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim.logParams(str(mdlvar['ToFile']['logfile']),mdlvar)
# plcsim.ClearAllTraces(mdl.scopes)  
plcsim.Set_sim_param()
plcsim.launch_sim(modelname=modelname)
# plcsim.HoldAllTraces(mdl.scopes)
# plcsim.saveAllTraces(mdl.scopes,mdl,mdlvar['ToFile']['Traces'])
post_process.gen_plots(resFile= mdlvar['ToFile']['ToFile_path'], html_file=mdlvar['ToFile']['output_html'],OPEN=True)
#?----------------------------------------------------------------------------------------------------------------------------------------
