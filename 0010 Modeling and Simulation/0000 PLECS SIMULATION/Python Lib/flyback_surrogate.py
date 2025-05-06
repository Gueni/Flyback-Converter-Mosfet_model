import os
import glob
import sys
import argparse
import pandas as pd
import numpy as np
from joblib import dump, load
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from skopt import gp_minimize
from skopt.space import Real

# --- 0) Argument parsing --------------------------------------------------
parser = argparse.ArgumentParser(
    description='Train surrogate or predict LoadVoltage for a flyback converter'
)
parser.add_argument('--mode', choices=['train', 'predict'], default='train',
                    help='Operation mode: train surrogate+optimize or predict only')
parser.add_argument('--vset', type=float, nargs=1,
                    help='Vset value for prediction')
parser.add_argument('--fs', type=float, nargs=1,
                    help='Switching frequency (Hz) for prediction')
args = parser.parse_args()

# --- 1) Predict mode -------------------------------------------------------
if args.mode == 'predict':
    if not (args.vset and args.fs):
        print('Error: --vset and --fs must be provided in predict mode')
        sys.exit(1)
    # Load existing surrogate
    try:
        model = load('surrogate_rf.joblib')
    except Exception as e:
        print(f"Error: failed to load surrogate model: {e}")
        sys.exit(1)
    v = args.vset[0]
    f = args.fs[0]
    y_pred = model.predict(np.array([v, f]).reshape(1, -1))[0]
    print(f"Predicted Load Voltage at Vset={v}, Fs={f}: {y_pred:.3f}")
    sys.exit(0)

# --- 2) Train mode ---------------------------------------------------------
# User-configurable sweep parameters (only used for bounds, not data loading)
CSV_DIR = 'D:\WORKSPACE\Flyback-Converter-Mosfet_model/0010 Modeling and Simulation/0000 PLECS SIMULATION\Python Lib\RES\CSV'
V_target  =  9 # Target voltage for optimization
files = sorted(glob.glob(os.path.join(CSV_DIR, '*.csv')))
total_files = len(files)

Vset_list = np.linspace(0.1, 24, int(total_files))
Fs_list = np.linspace(10e3, 500e3, int(total_files))

# --- 3) Load and preprocess CSVs -----------------------------------------
def load_csv_data(csv_folder, v_list, fs_list):
    files = sorted(glob.glob(os.path.join(csv_folder, '*.csv')))
    for idx, fpath in enumerate(files):
        # 1) Skip & delete truly empty files
        if os.stat(fpath).st_size == 0:
            print(f"Removing empty file: {fpath}")
            os.remove(fpath)
            continue
    if len(files) != len(v_list) or len(files) != len(fs_list):
        raise RuntimeError(
            f"Length mismatch: {len(files)} files vs {len(v_list)} VSET entries vs {len(fs_list)} FS entries"
        )
    records = []
    for idx, fpath in enumerate(files):
        arr = pd.read_csv(fpath, header=None).values
        if arr.shape[1] <= 7:
            raise RuntimeError(
                f"File {fpath} has {arr.shape[1]} columns; need at least 8 to extract index 7"
            )
        load_v_ss = arr[-1, 7]
        records.append([v_list[idx], fs_list[idx], load_v_ss])
    return pd.DataFrame(records, columns=['Vset', 'Fs', 'LoadVoltage'])

data = load_csv_data(CSV_DIR, Vset_list, Fs_list)

# --- 4) Prepare features and targets --------------------------------------
X = data[['Vset', 'Fs']].values
y = data['LoadVoltage'].values

# --- 5) Train/test split --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- 6) Fit surrogate model -----------------------------------------------
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
print(f"Surrogate trained. Test R² = {model.score(X_test, y_test):.3f}")
# Save the surrogate
dump(model, 'surrogate_rf.joblib')

# --- 7) Define optimization objective -------------------------------------
def surrogate_obj(x):
    v_out = model.predict(np.array(x).reshape(1, -1))[0]
    return abs(v_out - V_target)

# --- 8) Bayesian optimization ---------------------------------------------
domain = [
    Real(min(Vset_list), max(Vset_list), name='Vset'),
    Real(min(Fs_list),   max(Fs_list),   name='Fs')
]
print('Starting Bayesian Optimization...')
res = gp_minimize(
    func=surrogate_obj,
    dimensions=domain,
    n_calls=30,
    random_state=0
)
print('Optimization complete.')
print(f"Optimal inputs: Vset={res.x[0]:.3f}, Fs={res.x[1]:.1f}")
print(f"Predicted Load Voltage: {model.predict(data['LoadVoltage'].values)[0]:.3f}")

# --- 9) Save optimization result -----------------------------------------
opt_df = pd.DataFrame([{  
    'Vset': res.x[0],
    'Fs':   res.x[1],
    'LoadVoltage_pred': model.predict([res.x])[0]
}])
opt_df.to_csv('optimization_result.csv', index=False)
print('Optimization result saved to optimization_result.csv')
