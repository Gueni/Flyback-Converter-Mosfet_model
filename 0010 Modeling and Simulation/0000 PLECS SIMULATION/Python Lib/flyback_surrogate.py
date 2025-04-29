import os
import glob
import pandas as pd
import numpy as np
from joblib import dump, load
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from skopt import gp_minimize
from skopt.space import Real, Integer

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
import cleardata
import time
import os
#?----------------------------------------------------------------------------------------------------------------------------------------
port                                          = "7777"                                                               
url                                           = f"http://localhost:{port}/RPC2"                                      
modelname                                     = "flyback" 
mdlvar                                        = mdl.ModelVars
Vset                                          = (np.arange(15    ,24    +2    ,2    )).tolist()
Fs                                            = np.linspace(20e3, 250e3, num=len(Vset)).tolist()
plcsim                                        = plc.simpy(url=url , port=port , path=mdl.model_directory , modelvar=mdlvar)   
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim.rpc_connect()                                                                    
plcsim.load_model()
plcsim.ClearAllTraces(mdl.scopes)
# cleardata.clear_data_folders()                                                                  
inc  = 0
# 1) Parameters for your PLECS sweep (as in your original script)
#    Adjust ranges and steps as needed
Vset_range = np.linspace(10, 20, 10)    # example: 10V to 20V in 1V steps
Fs_range   = np.linspace(50e3, 200e3, 50)  # 50kHz to 200kHz
Iload_range= np.linspace(0.1, 1.0, 1)   # 0.1A to 1A

# Directory where PLECS CSV outputs are stored
CSV_DIR = 'D:\WORKSPACE\Flyback-Converter-Mosfet_model/0010 Modeling and Simulation/0000 PLECS SIMULATION\Python Lib\RES\CSV'
os.makedirs(CSV_DIR, exist_ok=True)

# (Optional) Function to launch your PLECS simulations in a loop
for i, item1 in enumerate(Fs):
    for j, item2 in enumerate(Vset):

        utc_numeric                            = str(int(time.strftime("%Y%m%d%H%M%S",  time.gmtime() )))
        sim_idx                                = inc+1
        mdlvar['ToFile']['sim_idx']            = sim_idx
        mdlvar['ToFile']['utc_numeric']        = utc_numeric
        mdlvar['ToFile']['ToFile_path']        = str((os.path.join(mdl.current_directory,mdl.ToFile_path+f"Results_{utc_numeric}_{sim_idx}.csv")).replace("\\", "/"))
        mdlvar['ToFile']['logfile']            = str((os.path.join(mdl.current_directory,mdl.logfile_path+f"Log_{utc_numeric}_{sim_idx}.log")).replace("\\", "/"))
        mdlvar['ToFile']['output_html']        = str((os.path.join(mdl.current_directory,mdl.output_html_path+f"Html_{utc_numeric}_{sim_idx}.html")).replace("\\", "/"))
        mdlvar['ToFile']['Traces']             = str((os.path.join(mdl.current_directory,mdl.Traces_path)).replace("\\", "/"))
        mdlvar['CTRL']['Vset']                 = Vset[j]
        mdlvar['CTRL']['Fs']                   = Fs[i]

        plcsim.logParams(mdlvar['ToFile']['logfile'],mdlvar)
        plcsim.Set_sim_param(mdlvar)
        plcsim.launch_sim(modelname=modelname)
        # plcsim.HoldAllTraces(mdl.scopes)
        # plcsim.saveAllTraces(mdlvar['scopes'],mdl,mdlvar['ToFile']['Traces'])
        # post_process.gen_plots(resFile= mdlvar['ToFile']['ToFile_path'], html_file=mdlvar['ToFile']['output_html'],OPEN=False)
        inc+=1
#?----------------------------------------------------------------------------------------------------------------------------------------

# 2) Ingest all CSVs into a single DataFrame
def load_csv_data(csv_folder=CSV_DIR):
    files = glob.glob(os.path.join(csv_folder, "*.csv"))
    df_list = []
    for f in files:
        df = pd.read_csv(f)
        # If CSVs lack parameter columns, extract them from filename
        # Example filename: "sweep_Vset_12_Fs_100000_Iload_0.5.csv"
        try:
            base = os.path.basename(f).replace('.csv','').split('_')
            df['Vset']   = float(base[2])
            df['Fs']     = float(base[4])
            df['Iload']  = float(base[6])
        except:
            pass
        df_list.append(df)
    data = pd.concat(df_list, ignore_index=True)
    return data

data = load_csv_data()

# 3) Define features/targets
#    Update column names as in your CSV structure
target_cols = ['Vout', 'Efficiency']
feature_cols = ['Vset', 'Fs', 'Iload']
X = data[feature_cols]
y = data[target_cols]

# 4) Train/test split
test_size = 0.2
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42
)

# 5) Fit surrogate (Random Forest)
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
print(f"Surrogate trained. Test R^2: {model.score(X_test, y_test):.3f}")

# 6) Save the surrogate model
dump(model, 'surrogate_rf.joblib')
print("Model saved to surrogate_rf.joblib")

# 7) Define an objective for optimization (maximize efficiency, penalize Vout error)
V_target = 15.0  # example desired output voltage

def surrogate_obj(x):
    # x = [Vset, Fs, Iload]
    y_pred = model.predict(np.array(x).reshape(1, -1))[0]
    Vout_pred, eta_pred = y_pred
    # objective: negative of (efficiency minus voltage error fraction)
    return -(eta_pred - abs(Vout_pred - V_target) / V_target)

# 8) Setup Bayesian Optimization
domain = [
    Real(min(Vset_range), max(Vset_range), name='Vset'),
    Real(min(Fs_range), max(Fs_range), name='Fs'),
    Real(min(Iload_range), max(Iload_range), name='Iload'),
]

print("Starting Bayesian Optimization...")
res = gp_minimize(
    func=surrogate_obj,
    dimensions=domain,
    n_calls=30,
    random_state=0
)
print("Optimization complete.")
print(f"Best inputs: Vset={res.x[0]:.3f}, Fs={res.x[1]:.1f}, Iload={res.x[2]:.3f}")
print(f"Predicted outputs at optimum: {model.predict([res.x])[0]}")

# Save optimization result
pd.DataFrame([{
    'Vset':res.x[0], 'Fs':res.x[1], 'Iload':res.x[2],
    'Vout_pred':model.predict([res.x])[0][0],
    'Eff_pred':model.predict([res.x])[0][1]
}]).to_csv('optimization_result.csv', index=False)
print("Optimization result saved to optimization_result.csv")
