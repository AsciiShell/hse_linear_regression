from pandas import read_csv, DataFrame
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

dataset = read_csv('EnergyEfficiency/ENB2012_data.csv', ';')
dataset.head()
dataset.corr()
dataset = dataset.drop(['X1', 'X4'], axis=1)
dataset.head()
trg = dataset[['Y1', 'Y2']]
trn = dataset.drop(['Y1', 'Y2'], axis=1)
models = [LinearRegression(),  # метод наименьших квадратов
          RandomForestRegressor(n_estimators=100, max_features='sqrt'),  # случайный лес
          KNeighborsRegressor(n_neighbors=6),  # метод ближайших соседей
          SVR(kernel='linear'),  # метод опорных векторов с линейным ядром
          LogisticRegression()  # логистическая регрессия
          ]
Xtrn, Xtest, Ytrn, Ytest = train_test_split(trn, trg, test_size=0.4)
# создаем временные структуры
TestModels = DataFrame()
tmp = {}
# для каждой модели из списка
for model in models:
    # получаем имя модели
    m = str(model)
    tmp['Model'] = m[:m.index('(')]
    # для каждого столбцам результирующего набора
    for i in range(Ytrn.shape[1]):
        # обучаем модель
        model.fit(Xtrn, Ytrn[:, i])
        # вычисляем коэффициент детерминации
        tmp['R2_Y%s' % str(i + 1)] = r2_score(Ytest[:, 0], model.predict(Xtest))
    # записываем данные и итоговый DataFrame
    TestModels = TestModels.append([tmp])
# делаем индекс по названию модели
TestModels.set_index('Model', inplace=True)
