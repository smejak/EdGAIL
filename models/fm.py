from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, log_loss
from utils.eval_metrics import all_metrics
from scipy.sparse import load_npz, vstack
from datetime import datetime
import pandas as pd
import pywFM
import argparse
import numpy as np
import os
import sys
import glob
import json


# Location of libFM's compiled binary file
os.environ['LIBFM_PATH'] = os.path.join(os.path.dirname(__file__),
                                        'libfm/bin/')

parser = argparse.ArgumentParser(description='Run FM')
parser.add_argument('X_file', type=str, nargs='?')
parser.add_argument('--iter', type=int, nargs='?', default=20)
parser.add_argument('--d', type=int, nargs='?', default=20)
parser.add_argument('--subset', type=int, nargs='?', default=0)
options = parser.parse_args()

X_file = options.X_file
y_file = X_file.replace('X', 'y').replace('npz', 'npy')
folder = os.path.dirname(X_file)

X = load_npz(X_file)
y = np.load(y_file)
nb_samples = len(y)

# Are folds fixed already?
X_trains = {}
y_trains = {}
X_tests = {}
y_tests = {}
FOLD = 'strong'
folds = glob.glob(os.path.join(folder, 'folds/60weak{}fold*.npy'.format(nb_samples)))

if folds:
    for i, filename in enumerate(folds):
        i_test = np.load(filename)
        print('Fold', i, i_test.shape)
        i_train = list(set(range(nb_samples)) - set(i_test))
        X_trains[i] = X[i_train]
        y_trains[i] = y[i_train]
        X_tests[i] = X[i_test]
        y_tests[i] = y[i_test]
else:
    print('No folds found')


if X_trains:
    X_train, X_test, y_train, y_test = (X_trains[0], X_tests[0],
                                        y_trains[0], y_tests[0])
    print(X_train.shape, X_test.shape)
else:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        shuffle=False)

predictions = []
params = {
    'task': 'classification',
    'num_iter': options.iter,
    'rlog': True,
    'learning_method': 'mcmc',
    'k2': options.d
}
fm = pywFM.FM(**params)
model = fm.run(X_train, y_train, X_test, y_test)
y_pred_test = np.array(model.predictions)
np.save(os.path.join(folder, 'y_pred{}.npy'.format(options.subset)), y_pred_test)

predictions.append({
    'fold': 0,
    'pred': y_pred_test.tolist(),
    'y': y_test.tolist()
})

print('Test predict:', y_pred_test)
print('Test was:', y_test)
print('Test ACC:', np.mean(y_test == np.round(y_pred_test)))
try:
    print('Test AUC', roc_auc_score(y_test, y_pred_test))
    print('Test NLL', log_loss(y_test, y_pred_test))
except ValueError:
    pass

iso_date = datetime.now().isoformat()
np.save(os.path.join(folder, 'w.npy'), np.array(model.weights))
np.save(os.path.join(folder, 'V.npy'), model.pairwise_interactions)
saved_results = {
    'predictions': predictions,
    'model': vars(options),
    'mu': model.global_bias,
    'folds': FOLD
}
with open(os.path.join(folder, 'results-{}.json'.format(iso_date)), 'w') as f:
    json.dump(saved_results, f)

df = pd.read_csv(os.path.join(folder, 'needed.csv'))
indices = np.load(folds[0])
test = df.iloc[indices]
    
all_metrics(saved_results, test)