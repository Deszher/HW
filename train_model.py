# принудительно отключим предупреждения системы
import warnings

import pandas as pd

warnings.simplefilter(action='ignore', category=Warning)

# импортируем класс модели
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

train = pd.read_csv(r'data_train.csv', header=None, index_col=0)
test = pd.read_csv(r'data_test.csv', header=None, index_col=0)

model = SARIMAX(train,
                order=(1, 0, 0),
                seasonal_order=(0, 0, 0, 12))
model = model.fit()

# тестовый прогнозный период начнется с конца обучающего периода
start = len(train)

# и закончится в конце тестового
end = len(train) + len(test) - 1

# применим метод predict
predictions = model.predict(start, end)

mae = mean_absolute_error(test, predictions)
# squared True returns MSE value, False returns RMSE value
mse = mean_squared_error(test, predictions)
rmse = mean_squared_error(test, predictions, squared=False)

print(f"mae={mae}")
print(f"mse={mse}")
print(f"rmse={rmse}")
