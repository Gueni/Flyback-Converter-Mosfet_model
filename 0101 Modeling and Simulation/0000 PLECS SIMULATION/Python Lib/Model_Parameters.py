
#!---------------------------------------------------------------------------------------------------------------------------------------- 
#!                                      ______      __               __
#!                                     / __/ /_  __/ /_  ____ ______/ /__   _   ______ ___________
#!                                    / /_/ / / / / __ \/ __ `/ ___/ //_/  | | / / __ `/ ___/ ___/
#!                                   / __/ / /_/ / /_/ / /_/ / /__/ ,<     | |/ / /_/ / /  (__  )
#!                                  /_/ /_/\__, /_.___/\__,_/\___/_/|_|    |___/\__,_/_/  /____/
#!                                        /____/
#!                                  
#!----------------------------------------------------------------------------------------------------------------------------------------
import os 
from datetime import datetime, timezone
#!----------------------------------------------------------------------------------------------------------------------------------------
utc_now             = datetime.now(timezone.utc)                                                            
utc_numeric         = utc_now.strftime("%H%M%S")                                                            
current_directory   = os.getcwd()                                                                           
sim_idx             = 0                                                                                     
Traces_path         = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Traces/"           
ToFile_path         = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/CSV/"              
logfile_path        = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Log/"              
output_html_path    = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/html/"             
model_path          = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Model/flyback.plecs"                  
model_directory     = (os.path.join(current_directory, model_path)).replace("\\", "/")                                        
#!----------------------------------------------------------------------------------------------------------------------------------------
Sim_param 	= {                                                                                             
                  'tSim'	    	   : 1,                                                                  #? [s]     - 
                  'tsave_i'	    	: 0.1,                                                                  #? [s]     - 
                  'load_tflip'	   : 10 * 0.5,                                                            #? [s]     -  
                  'maxStep'		   : 1e-3,                                                                  #? [/]     - 
                  'ZeroCross'       : 1000,                                                                  #? [/]     - 
                  'rel_tol'		   : 1e-7                                                                   #? [/]     - 
               }
ToFile      = {                                                                                             
                  'ToFile_path'		: (os.path.join(current_directory,                                      #? [/]      - 
                   ToFile_path+f"Results_{utc_numeric}_{sim_idx}.csv")).replace("\\", "/"),                                 
                  'logfile'		   : (os.path.join(current_directory,                                      #? [/]      - 
                   logfile_path+f"Log_{utc_numeric}_{sim_idx}.log")).replace("\\", "/"),                                 
                  'output_html'     : (os.path.join(current_directory,                                      #? [/]      - 
                   output_html_path+f"Html_{utc_numeric}_{sim_idx}.html")).replace("\\", "/"),              
                  'Traces'		      : (os.path.join(current_directory,                                      #? [/]      - 
                   Traces_path)).replace("\\", "/")  ,                                                      
                  'Ts'              : 0,                                                                    #? [s]      - 
                  'tsave' 	    	   : Sim_param['tSim']-Sim_param['tsave_i']                                #? [s]      - 
               }  
SW          = {                                                                                             
                  'Config'          : 1,                                                                    #? [/]      - 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   #? [/]      - 
                  'Rgon'            : 2.5,                                                                  #? [Ohm]    - 
                  'Rgoff'           : 2.5,                                                                  #? [Ohm]    - 
                  'Vdsmax'          : 1200,                                                                 #? [/]      - 
                  'Idsmax'          : 100,                                                                  #? [/]      - 
                  'Tjmax'           : 175,                                                                  #? [/]      -                   
                  'Tjmin'           : -40,                                                                  #? [/]      -                  
                  'TcDerating'      : [-55,27,45,70,95,108,120,132,145,158,170,175],                        #? [/]      -         
                  'IdsMaxDerated'   : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0],                       #? [/]      -   
                  'ron_mosfet'      : 0.021,                                                                #? [Ohm]    - 
                  'Rds_off'         : 0,                                                                    #? [Ohm]    - 
                  'Iinit'           : 0,                                                                    #? [/]      - 
                  'Coss'            :  {                                                                                           
                                          'Config'		      : 5,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-12,                                        #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    - 
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -       
                                          },                                                               
                  'vblock'          : 0,                                                                    #? [/]      - 
                  'Idrain'          : 0,                                                                    #? [/]      - 
                  'Trise'           : 0,                                                                    #? [/]      - 
                  'Tfall'           : 0,                                                                    #? [/]      - 
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         #? [/]      - 
                  'ron_body_diode'  : 0.033,                                                                #? [Ohm]    - 
                  'Rdb_off'         : 0,                                                                    #? [Ohm]    - 
                  'vf_body_diode'   : 2.3,                                                                  #? [/]      - 
                  'BD_If'           : 0,                                                                    #? [/]      - 
                  'T_reverse'       : 0,                                                                    #? [/]      - 
                  'Q_reverse'       : 0,                                                                    #? [/]      -      
                  'Ldr'             : 1e-12,                                                                #? [/]      - 
                  'Ldr_Iinit'       : 0,                                                                    #? [/]      - 
                  'Lso'             : 1e-12,                                                                #? [/]      - 
                  'Lso_Iinit'       : 0,                                                                    #? [/]      - 
                  'nPara'           : 0,                                                                    #? [/]      - 
                  'T_init'          : 25,                                                                   #? [/]      - 
                  'Tamb'            : 25,                                                                   #? [/]      - 
                  't_init'          : 25,                                                                   #? [/]      - 
                  'rth_sw'          : 0.09,                                                                 #? [/]      - 
                  'rth_ch'          : 0.5,                                                                  #? [/]      - 
                  'Rth'             : 0.34 	                                                               #? [/]      - 				    	                           
               }
Trafo       = {                                                                                             
                  'eq_per_leak'     : 5.9e-9,                                                               #? [/]      -                                   
                  'MMF_leak'        : 0,                                                                    #? [/]      -                      
                  'NP'              : 13,                                                                   #? [/]      -                       
                  'NS'              : 7,                                                                    #? [/]      -                 
                  'NS2'             : 3,                                                                    #? [/]      -
                  'CSA_core'		   : 9.39e-5,                                                              #? [/]      - diode thermal description       
                  'Lflux_core'		: 0.0376,                                                               #? [Ohm]    - diode forward voltage    
                  'rel_per_core'		: 9550,                                                                 #? [V]      - diode forward voltage
                  'Sat_per_core'		: 1,                                                                    #? [K/W]    - thermal resistance case-heatsink (grease)       
                  'flux_dens_core'  : 0.47,                                                                 #? [/]      - Number of parallel diodes      
                  'MMF_core'		   : 0,                                                                    #? [K/W]    - Heatsink to ambient thermal resistance    
                  'CSA_gap'		   : 9.39e-5,                                                              #? [C]      - initial temperature   
                  'Lflux_gap'		   : 0.00022,                                                              #? [C]      - initial temperature   
                  'MMF_gap'		   : 0                                                                     #? [C]      - initial temperature   
               }	
CTRL        = {                                                                                             
                  'Vref'    		   :  400,                                                                 #? [/]      - 
                  'fs'    		      :  70e-3,                                                               #? [/]      -  
                  'Ri_Kp'           :  0.1,                                                                 #? [/]      - 
                  'Ri_Ki'           :  600,                                                                 #? [/]      - 
                  'Rv_Kp'           :  5,                                                                   #? [/]      - 
                  'Rv_Ki'           :  800                                                                  #? [/]      - 
               }
Cout1       = {                                                                                             
                  'Config'		      : 1,                                                                    #? [/]      - 
                  'Cap_s'    		   : 100e-6,                                                               #? [/]      -  
                  'Resr_s'	         : 19e-9,                                                                #? [Ohm]    - 
                  'Lesl_s'	         : 1e-19,                                                                #? [/]      - 
                  'Npara'		      : 6,                                                                    #? [/]      - 
                  'Nseri'		      : 1,                                                                    #? [/]      - 
                  'Vinit'		      : 0,                                                                    #? [/]      - 
                  'Iinit'		      : 1e-3                                                                  #? [/]      - 
               }
Cout2       = {                                                                                             
                  'Config'		      : 1,                                                                    #? [/]      - 
                  'Cap_s'    		   : 100e-6,                                                               #? [/]      -  
                  'Resr_s'	         : 19e-9,                                                                #? [Ohm]    - 
                  'Lesl_s'	         : 1e-19,                                                                #? [/]      - 
                  'Npara'		      : 6,                                                                    #? [/]      - 
                  'Nseri'		      : 1,                                                                    #? [/]      - 
                  'Vinit'		      : 0,                                                                    #? [/]      - 
                  'Iinit'		      : 1e-3                                                                  #? [/]      - 
               }
Load        = {                                                                                             
                  'Config'		      : 1,                                                                    #? [/]      - 
                  'CL'    		      : 0,                                                                    #? [/]      - 
                  'RL'		         : 100,                                                                   #? [Ohm]    -
                  'LL'		         : 0,                                                                    #? [/]      - 
                  'Vinit'		      : 0,                                                                    #? [/]      - 
                  'Iinit'		      : 0,                                                                    #? [/]      - 
                  't_switch'        : Sim_param['tSim']-Sim_param['load_tflip'],                            #? [/]      - 
                  't_dead'          : (Sim_param['tSim']-Sim_param['load_tflip'])/2                         #? [/]      - 
               }
RCD         = {                                                                                             
                  'R'               : 80,                                                                   #? [Ohm]    - 
                  'C'               :  {                                                                                
                                          'Config'		      : 1,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-8,                                         #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    -           
                                          'Lesl_s'		      : 0,                                            #? [/]      -       
                                          'Npara'		      : 1,                                            #? [/]      -          
                                          'Nseri'		      : 1,                                            #? [/]      -       
                                          'Vinit'		      : 0,                                            #? [/]      -          
                                          'Iinit'		      : 0                                             #? [/]      -                 
                                          },
                  'diode'		         : 'file:C4D40120D',                                                  #? [/]      - diode thermal description       
                  'ron_diode'		      : 0.04,                                                              #? [Ohm]    - diode forward voltage    
                  'vf_diode'		      : 0.6,                                                               #? [V]      - diode forward voltage
                  'rth_ch_diode'		   : 0.5,                                                               #? [K/W]    - thermal resistance case-heatsink (grease)       
                  'num_par_diode'		: 4,                                                                 #? [/]      - Number of parallel diodes      
                  'rth_ch'		         : 0.1,                                                               #? [K/W]    - Heatsink to ambient thermal resistance    
                  't_init'		         : 25                                                                 #? [C]      - initial temperature   
               }
diode       = {
                  'diode'		         : 'file:C4D40120D',                                                  #? [/]      - diode thermal description       
                  'ron_diode'		      : 0.04,                                                              #? [Ohm]    - diode forward voltage    
                  'vf_diode'		      : 0.6,                                                               #? [V]      - diode forward voltage
                  'rth_ch_diode'		   : 0.5,                                                               #? [K/W]    - thermal resistance case-heatsink (grease)       
                  'num_par_diode'		: 4,                                                                 #? [/]      - Number of parallel diodes      
                  'Rth'		            : 0.1,                                                               #? [K/W]    - Heatsink to ambient thermal resistance    
                  't_init'		         : 25                                                                 #? [C]      - initial temperature   
               }
Thermals    = {                                                                                             
                  'T_amb'           :  25.0,                                                                #? [/]      - 
                  'rth_Amb'         :  0.09                                                                 #? [/]      - 
               }

#!----------------------------------------------------------------------------------------------------------------------------------------
ModelVars   = {                                                                                             
                  'Sim_param'       :  Sim_param   ,      
                  'ToFile'          :  ToFile      ,    
                  'SW'              :  SW          ,                                                             
                  'Trafo'           :  Trafo       ,                                                                 
                  'CTRL'            :  CTRL        ,                                                            
                  'Cout1'           :  Cout1       ,  
                  'Cout2'           :  Cout2       ,                                                                                                                          
                  'Load'            :  Load        ,                                                                
                  'RCD'             :  RCD         ,                                                                
                  'diode'           :  diode       ,                                                                
                  'Thermals'        :  Thermals    ,
               }	
#!----------------------------------------------------------------------------------------------------------------------------------------	
scopes      =  [                                                                                            
				      "flyback/Scopes/input",                                                                 
				      "flyback/Scopes/RCD",                                                                                         
				      "flyback/Scopes/load_scope",                                                                                         
				      "flyback/Scopes/load_scope1",                                                                                        
				      "flyback/Scopes/BHLoop",                                                                                        
				      "flyback/Scopes/MMF",                                                                                      
				      "flyback/Scopes/primary",                                                                                    
				      "flyback/Scopes/secondary1",                                                                                    
				      "flyback/Scopes/secondary2",                                                                                    
				      "flyback/Scopes/Mos",                                                                                  
				      "flyback/Scopes/diodes",                                                                                
				      "flyback/Scopes/'cout",                                                                                
				      "flyback/Scopes/Power",                                                                                 
				      "flyback/Scopes/Outputs",                                                                                
				      "flyback/Scopes/PI"                                                                                 
               ]	
Waveforms   =  [                                                                                            
                  'Source Voltage',                  
                  'Source Current',
                  'Source Power',
                  #!-------------------------
                  'RCD Clamp Current',
                  'RCD C Current',
                  'RCD R Current',
                  'RCD Clamp Voltage',                  
                  'RCD C Voltage',                  
                  'RCD R Voltage',                  
                  'RCD Clamp Dissipation',
                  #!-------------------------
                  'Load1 Voltage',
                  'Load1 Current',
                  #!-------------------------
                  'Load2 Voltage',
                  'Load2 Current',
                  #!-------------------------
                  'PFC output voltage',
                  #!-------------------------
                  'Core Field Strength',
                  'Core Flux Density',
                  'Air gap Field Strength',
                  'Air gap Flux Density',
                  #!-------------------------
                  'Core MMF',
                  'Core Flux',
                  'Air gap MMF',
                  'Air gap Flux',
                  #!-------------------------
                  'Primary Winding voltage',
                  'Primary Winding Current',
                  'Secondary1 Winding voltage',
                  'Secondary1 Winding Current',
                  'Secondary2 Winding voltage',
                  'Secondary2 Winding Current',
                  #!-------------------------
                  'MOSFET voltage',
                  'BD voltage',
                  'MOSFET Current',
                  'BD Current',
                  'MOSFET junction Temp',
                  'BD junction Temp',
                  'MOSFET case Temp',
                  'MOSFET switching losses',
                  'BD switching losses',
                  'MOSFET conduction losses',
                  'BD conduction losses',
                  #!-------------------------
                  'Diode1 voltage',
                  'Diode1 Current',
                  'Diode1 junction Temp',
                  'Diode1 case Temp',
                  'Diode1 switching losses',
                  'Diode1 Diode LS1 junction Temp',
                  'Diode1 conduction losses',

                  'Diode2 voltage',
                  'Diode2 Current',
                  'Diode2 junction Temp',
                  'Diode2 case Temp',
                  'Diode2 switching losses',
                  'Diode2 Diode LS1 junction Temp',
                  'Diode2 conduction losses',
                  #!-------------------------
                  'Cout1 Voltage',                  
                  'Cout1 Current',
                  'Cout1 Dissipation',
                  #!-------------------------
                  'Cout2 Voltage',                  
                  'Cout2 Current',
                  'Cout2 Dissipation',
                  #!-------------------------                 
                  'Power',
                  'Vout',
                  'Iout',
                  'Vout2',
                  'Iout2',
               ]		
#!----------------------------------------------------------------------------------------------------------------------------------------	