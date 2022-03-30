from flask import Flask, request, json, session
from sklearn.model_selection import train_test_split
from catboost import Pool
from catboost import CatBoostClassifier
import pandas as pd
import random
from dbdesign import Results
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.app = app
db.init_app(app)


def trainer():
    df = pd.read_csv('../data/dataset.csv')
    df = df.drop(columns=['index', 'Unnamed: 0'], axis=1)
    X = df.drop(columns=['originality'], axis=1)
    #print(X.head(5))
    y = df['originality']
    global X_test
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        train_size=0.7,
                                                        random_state=42,
                                                        stratify=y)
    #print(X_test.head(5))
    train_data = Pool(
        data=X_train,
        label=y_train,
        text_features=['sentence'],
    )
    params = {
        'loss_function': 'Logloss',
        'iterations': 200,
        'custom_loss': 'AUC',
        'random_seed': 45,
        'learning_rate': 0.45
    }
    global model
    model = CatBoostClassifier(**params)
    model.fit(X=train_data)

    # preds = model.predict(X_test)
    #
    # Y_test = list(y_test)
    # count = 0
    # for i in range(len(preds)):
    #     if preds[i] == Y_test[i]:
    #         count += 1


    X_test['originality'] = y_test
    X_test = X_test.reset_index(drop=False)
    #X_test.head(5)
    #print(X_test.head(5))




@app.route("/get_answers", methods=['POST', 'GET'])
def randomizer():
    indexes = list(X_test['index'].values)
    random_index = random.choice(indexes)
    string_to_go = X_test[X_test['index'] == random_index]
    string_to_go = string_to_go['sentence'].values[0]
    dict_to_go = {int(random_index): string_to_go}
    return json.dumps(dict_to_go)


@app.route("/to_base", methods=['POST', 'GET'])
def checker():
    jdata = json.loads(request.json)
    user_check = db.session.query(Results).filter(Results.user_id == jdata['user']).first()
    if user_check:
        db.session.query(Results).filter(Results.user_id == jdata['user']).update(dict(status=Results.status + 1))
        db.session.commit()
    else:
        results = Results(
            user_id=jdata['user'],
            status=1,
            user_ok=0,
            model_ok=0,
            uwins=0,
            uloses=0,
            uequals=0
            )
        user_check = results
        db.session.add(results)
        db.session.commit()

    matching_string = X_test[X_test['index'] == int(jdata['text_id'])]
    data = {'sentence': [str(matching_string['sentence'])]}
    predicted_by_model = model.predict(pd.DataFrame.from_dict(data))
    status_togo = user_check.status
    print(status_togo)
    if status_togo != 5:
        if int(matching_string['originality']) == int(jdata['answer']):
            db.session.query(Results).filter(Results.user_id == jdata['user']).update({'user_ok': Results.user_ok+1})
            db.session.commit()
        if int(predicted_by_model) == int(matching_string['originality']):
            db.session.query(Results).filter(Results.user_id == jdata['user']).update({'model_ok': Results.model_ok+1})
            db.session.commit()
        return json.dumps({'next_text': 1})
    else:
        if user_check.user_ok > user_check.model_ok:
            db.session.query(Results).filter(Results.user_id == jdata['user']).update({'uwins': Results.uwins + 1})
            db.session.commit()
            winner_index = 'Поздравляю! Ты победил(а) с отрывом: '+str(user_check.user_ok-user_check.model_ok)
        elif user_check.user_ok < user_check.model_ok:
            db.session.query(Results).filter(Results.user_id == jdata['user']).update({'uloses': Results.uloses + 1})
            db.session.commit()
            winner_index = 'К сожалению, ты проиграл(а) с отрывом: ' + str(user_check.model_ok - user_check.user_ok)
        else:
            db.session.query(Results).filter(Results.user_id == jdata['user']).update({'uequals': Results.uloses + 1})
            db.session.commit()
            winner_index = 'Ого, у нас ничья!'
        db.session.query(Results).filter(Results.user_id == jdata['user']).update({'status': 0, 'user_ok': 0,
                                                                                   'model_ok': 0})
        db.session.commit()
        return json.dumps({'next_text': 0,
                           'result': winner_index,
                           'wins': user_check.uwins,
                           'average': (user_check.uwins + user_check.uloses + user_check.uequals)
                           })


if __name__ == "__main__":
    trainer()
    #checker()
    app.run(port=1337)
