from skopt import Optimizer
from skopt.space import Real
import plecs as plc
import Model_Parameters as mdl
import numpy as np
import post_process
import cleardata
import time
import os
import pandas as pd

# --------------------------------------------------------------------------------
# Initialize the necessary ports and variables
port = "7777"
url = f"http://localhost:{port}/RPC2"
modelname = "flyback"
mdlvar = mdl.ModelVars
plcsim = plc.simpy(url=url, port=port, path=mdl.model_directory, modelvar=mdlvar)

# Define parameter bounds for skopt
search_space = [
    Real(1, 24, name='Vset'),   # Voltage setpoint range
    Real(20e3, 250e3, name='Fs')  # Switching frequency range
]

# Initialize Bayesian optimizer
optimizer = Optimizer(dimensions=search_space, random_state=5)

# Connect to PLECS
plcsim.rpc_connect()
plcsim.load_model()
plcsim.ClearAllTraces(mdl.scopes)
cleardata.clear_data_folders()

# How many iterations to run
n_iter = 24
inc = 0

def log_error(error_message):
    """Function to log errors to a log file."""
    log_file_path = "simulation_errors.log"  # Change this path if needed
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")

def run_simulation(params):
    global inc

    Vset_val, Fs_val = params
    mdlvar['CTRL']['Vset'] = float(Vset_val)
    mdlvar['CTRL']['Fs'] = float(Fs_val)

    utc_numeric = str(int(time.strftime("%Y%m%d%H%M%S", time.gmtime())))
    sim_idx = inc + 1
    mdlvar['ToFile']['sim_idx'] = sim_idx
    mdlvar['ToFile']['utc_numeric'] = utc_numeric
    mdlvar['ToFile']['ToFile_path'] = str((os.path.join(mdl.current_directory, mdl.ToFile_path + f"Results_{utc_numeric}_{sim_idx}.csv")).replace("\\", "/"))
    mdlvar['ToFile']['logfile'] = str((os.path.join(mdl.current_directory, mdl.logfile_path + f"Log_{utc_numeric}_{sim_idx}.log")).replace("\\", "/"))
    mdlvar['ToFile']['output_html'] = str((os.path.join(mdl.current_directory, mdl.output_html_path + f"Html_{utc_numeric}_{sim_idx}.html")).replace("\\", "/"))
    mdlvar['ToFile']['Traces'] = str((os.path.join(mdl.current_directory, mdl.Traces_path)).replace("\\", "/"))

    # Set simulation parameters in PLECS
    plcsim.logParams(mdlvar['ToFile']['logfile'], mdlvar)
    plcsim.Set_sim_param(mdlvar)

    # Run the simulation and save results to CSV
    try:
        # Uncomment the following line to run the simulation (currently commented for testing)
        plcsim.launch_sim(modelname=modelname)
        # post_process.gen_plots(resFile=mdlvar['ToFile']['ToFile_path'], html_file=mdlvar['ToFile']['output_html'], OPEN=False)

    except Exception as e:
        # Catch specific errors related to PLECS state discontinuities or other issues
        error_message = f"Error during simulation for parameters {params}: {str(e)}"
        log_error(error_message)
        print(f"Warning: {error_message}")
        return float('inf')  # Return a high value to ensure optimization skips this point

    # Read the CSV file to extract Load Voltage from column index 7
    try:
        # Check if the file exists before trying to read
        if not os.path.exists(mdlvar['ToFile']['ToFile_path']):
            error_message = f"Error: CSV file does not exist at {mdlvar['ToFile']['ToFile_path']}"
            log_error(error_message)
            print(f"Error: {error_message}")
            return float('inf')

        data = pd.read_csv(mdlvar['ToFile']['ToFile_path'])
        load_voltage = data.iloc[:, 7]  # Get column index 7 (Load Voltage)

        # Ensure the values are valid (no NaN or Inf)
        if load_voltage.isnull().any() or np.isinf(load_voltage).any():
            error_message = f"Warning: Found NaN or Inf values in Load Voltage data for parameters {params}"
            log_error(error_message)
            print(f"Warning: {error_message}")
            objective_val = float('inf')  # Return a very high value in case of invalid data
        else:
            # Objective function: Here, I use the mean load voltage, but you can change to other metrics
            objective_val = load_voltage.mean()  # Change this to min() or max() if preferred
    except Exception as e:
        error_message = f"Error reading CSV or processing data: {e}"
        log_error(error_message)
        print(f"Error: {error_message}")
        objective_val = float('inf')  # In case of error, return a high value

    # Increment simulation count
    inc += 1
    return objective_val  # Return the calculated objective for optimization

# --------------------------------------------------------------------------------
# Main optimization loop using Bayesian Optimization

# Set the number of iterations for the optimization loop
max_iterations = 20  # You can set this to your desired number of iterations

for iteration in range(max_iterations):
    # Get the next point from the optimizer
    next_point = optimizer.ask()
    print(f"\n[Iteration {iteration+1}] Testing parameters: {next_point}")
    # Run the simulation and get the objective value
    objective_val = run_simulation(next_point)
    print(f"→ Objective (to minimize): {objective_val:.5f}")

    # Ensure the objective value is valid before passing to the optimizer
    if np.isfinite(objective_val):  # Only pass finite values
        optimizer.tell(next_point, objective_val)
    else:
        print(f"Warning: Invalid objective value {objective_val} at parameters {next_point}. Skipping this point.")
        # Optionally log or handle the invalid point
        log_error(f"Invalid objective at {next_point}: {objective_val}")

# Save the optimization results
import pandas as pd
results_df = pd.DataFrame(optimizer.Xi, columns=['Vset', 'Fs'])
results_df['Objective'] = optimizer.yi
results_df.to_csv("bayes_opt_results.csv", index=False)

print("Bayesian Optimization complete. Results saved.")
