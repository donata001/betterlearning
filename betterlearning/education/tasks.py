import os
import json
from sklearn.externals import joblib
from .models import Prediction, Training
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score, ShuffleSplit


K=10
test_size=0.1

def train():
    data = Prediction.objects.filter(predict=False)
    df = pd.DataFrame(list(data.values()))
    users = [o.user for o in data]
    df['age'] = pd.DataFrame(list([user.userprofile.age for user in users]))
    for x in ['id', 'base_personal', 'base_general', 'predict', 'created', 'user_id', 'training_id']:
        df = df.drop(x, axis=1)

    y = df['next_level']
    df = df.drop('next_level', axis=1)
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(df, y) 

    #kf = KFold(len(ft[features]), n_folds=10)
    kf = ShuffleSplit(len(df), n_iter=K, test_size=test_size, random_state=0)
    # score is accuracy here 

    accuracy = cross_val_score(neigh, df, y, cv=kf)
    batch = Training.objects.create(training_accuracy=sum(accuracy[:(1-test_size)*K])/K/(1-test_size),
                                    sample_size=len(df.index),
                                    fold=K,
                                    subset_accuracy=json.dumps(accuracy.tolist()),
                                    test_accuracy=sum(accuracy[(1-test_size)*K:])/K/test_size
                                    )
    Prediction.objects.all().update(training=batch)
    
    if not os.path.exists('./models'):
            os.makedirs('./models')

    joblib.dump(neigh, './models/model.pkl')
                      
    