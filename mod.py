from pandas import read_csv
from sklearn.model_selection import train_test_split, GridSearchCV
from numpy import unique, arange, random, array, around, amax
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, MaxPooling1D, BatchNormalization, Flatten
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import MultinomialNB
from vfi import VFI
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import warnings
import tensorflow as tf

warnings.filterwarnings("ignore")


def read_data(address):
    data = read_csv(address)
    try:
        del data['Unnamed: 0']
    except KeyError:
        'Unnamed: 0'
    (r, c) = data.shape
    x = data.iloc[:, :c - 1]
    y = data.iloc[:, c - 1]
    nclass = len(unique(y))
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=0)

    return x_train, x_test, y_train, y_test, nclass, c


def read_data_cv(address):
    data = read_csv(address)
    try:
        del data['Unnamed: 0']
    except KeyError:
        'Unnamed: 0'

    (r, c) = data.shape
    x = data.iloc[:, :c - 1]
    y = data.iloc[:, c - 1]
    return x, y


def save_score_ml(result, name):
    mean_res = 100 * around(result.mean(), decimals=3)
    plt.plot(arange(len(result)), result, c=random.rand(3,), marker='o')
    plt.xlabel('K - Fold')
    plt.ylabel('Scores')
    plt.legend(name)
    plt.grid(True)
    plt.title(name)
    img_ad = name + '.png'
    plt.savefig(img_ad)
    plt.clf()
    return img_ad,mean_res


def save_score_dl(history):
    fig, axs = plt.subplots(1, 2, figsize=(15, 4))
    keys = list(history.history.keys())
    training_loss = history.history[keys[0]]
    validation_loss = history.history[keys[2]]

    training_accuracy = history.history[keys[1]]
    validation_accuracy = array(history.history[keys[3]])

    epoch_count = range(1, len(training_loss) + 1)

    axs[0].plot(epoch_count, training_loss, 'r--')
    axs[0].plot(epoch_count, validation_loss, 'b-')
    axs[0].legend(['Training Loss', 'Validation Loss'])

    axs[1].plot(epoch_count, training_accuracy, 'r--')
    axs[1].plot(epoch_count, validation_accuracy, 'b-')
    axs[1].legend(['Training Accuracy', 'Validation Accuracy'])
    img_path = 'cnn.png'
    plt.savefig(img_path)
    plt.clf()
    return  img_path,amax(validation_accuracy) * 100

def nayve_bayes(address):
    kfold = KFold(n_splits=10, shuffle=True, random_state=0)
    x, y = read_data_cv(address)
    sc = MinMaxScaler(feature_range=(0, 1))
    rX = sc.fit_transform(x)
    nb = MultinomialNB()
    result = cross_val_score(nb, rX, y, cv=kfold)
    name = 'Nayve Bayes'
    return save_score_ml(result, name)


def Vfi(address):
    kfold = KFold(n_splits=10, shuffle=True, random_state=0)
    x = ['uniform', 'quantile', 'kmeans']
    b = [80, 90, 120]
    valores_grid = dict(strategy=x, n_bins=b)
    X, Y = read_data_cv(address)
    model = VFI()
    grid = GridSearchCV(model,valores_grid, cv=kfold)
    name = "VFI"
    grid_result = grid.fit(X, Y)
    result = array([grid.best_score_,grid.best_score_,grid.best_score_])
    return save_score_ml(result, name)


def KNN(address):
    X, Y = read_data_cv(address)
    kfold = KFold(n_splits=10, shuffle=True, random_state=0)
    knn = KNeighborsClassifier()
    result = cross_val_score(knn, X, Y, cv=kfold)
    name = 'KNN'
    return save_score_ml(result, name)


def SVM(address):
    X, Y = read_data_cv(address)
    kfold = KFold(n_splits=10, shuffle=True, random_state=0)
    svm = SVC()
    result = cross_val_score(svm, X, Y, cv=kfold)
    name = 'SVM'
    return save_score_ml(result, name)


def DeyCNN(address):
    x_train, x_test, y_train, y_test, nclass, c = read_data(address)
    x_train = x_train.values.reshape(x_train.values.shape[0], c - 1, 1)
    x_test = x_test.values.reshape(x_test.values.shape[0], c - 1, 1)

    model = Sequential()

    model.add(BatchNormalization(input_shape=(c - 1, 1)))

    model.add(Conv1D(20, kernel_size=60, strides=10, activation='relu'))
    model.add(MaxPooling1D(pool_size=4, strides=4))
    model.add(Dropout(0.25))
    model.add(Conv1D(20, kernel_size=60, activation='relu'))
    model.add(MaxPooling1D(pool_size=4, strides=4))
    model.add(Dropout(0.25))
    model.add(Conv1D(28, kernel_size=3, activation='relu'))
    model.add(Conv1D(28, kernel_size=3, activation='relu'))
    model.add(MaxPooling1D(pool_size=2, strides=2))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1029, activation='relu'))
    model.add(Dense(2058, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(nclass, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    device_name = tf.test.gpu_device_name()
    if device_name != '':
        with  tf.device(device_name):
            history = model.fit(x_train, y_train, batch_size=256, epochs=800, steps_per_epoch=900,
                                validation_data=(x_test, y_test))
            return save_score_dl(history)
    else:
        history = model.fit(x_train, y_train, batch_size=256, epochs=800, steps_per_epoch=900,
                            validation_data=(x_test, y_test))
        return save_score_dl(history)


def UrtCNN(address):
    x_train, x_test, y_train, y_test, nclass, c = read_data(address)
    x_train = x_train.values.reshape(x_train.values.shape[0], c - 1, 1)
    x_test = x_test.values.reshape(x_test.values.shape[0], c - 1, 1)

    model = Sequential()
    model.add(BatchNormalization(input_shape=(c - 1, 1)))
    model.add(Conv1D(20, kernel_size=50, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Conv1D(20, kernel_size=50, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))
    model.add(Conv1D(24, kernel_size=30, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))
    model.add(Conv1D(24, kernel_size=30, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))
    model.add(Conv1D(24, kernel_size=10, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))
    model.add(Conv1D(12, kernel_size=10, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(192, activation='relu'))
    model.add(Dense(192, activation='relu'))
    model.add(Dense(nclass, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    device_name = tf.test.gpu_device_name()
    if device_name != '':
        with  tf.device(device_name):
            history = model.fit(x_train, y_train, batch_size=128, epochs=90, steps_per_epoch=1000,
                                validation_data=(x_test, y_test))
            return save_score_dl(history)
    else:
        history = model.fit(x_train, y_train, batch_size=128, epochs=90, steps_per_epoch=1000,
                            validation_data=(x_test, y_test))
        return save_score_dl(history)


def HsiehCNN(address):
    x_train, x_test, y_train, y_test, nclass, c = read_data(address)
    x_train = x_train.values.reshape(x_train.values.shape[0], c - 1, 1)
    x_test = x_test.values.reshape(x_test.values.shape[0], c - 1, 1)

    model = Sequential()
    model.add(Conv1D(32, kernel_size=5, activation='relu', input_shape=(c - 1, 1)))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(2))
    model.add(Conv1D(32, kernel_size=5, activation='relu'))
    model.add(MaxPooling1D(2))
    model.add(Conv1D(64, kernel_size=5, activation='relu'))
    model.add(MaxPooling1D(2))
    model.add(Conv1D(64, kernel_size=5, activation='relu'))
    model.add(MaxPooling1D(2))
    model.add(Conv1D(128, kernel_size=5, activation='relu'))
    # model.add(MaxPooling1D(2))
    # model.add(Conv1D(128, kernel_size = 5, activation ='relu'))
    # model.add(MaxPooling1D(2))
    # model.add(Dropout(0.5))
    # model.add(Conv1D(256, kernel_size = 5, activation ='relu'))
    # model.add(MaxPooling1D(2))
    # model.add(Conv1D(256, kernel_size = 5, activation ='relu'))
    # model.add(MaxPooling1D(2))
    # model.add(Dropout(0.5))
    # model.add(Conv1D(512, kernel_size = 5, activation='relu'))
    # model.add(MaxPooling1D(2))
    # model.add(Dropout(0.5))
    # model.add(Conv1D(512, kernel_size = 5, activation ='relu'))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(nclass, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    steps_epoch = len (x_train)//128
    steps_valid = len(x_test)//128
    device_name = tf.test.gpu_device_name()
    if device_name != '':
        with  tf.device(device_name):
            history = model.fit(x_train, y_train, batch_size=128, epochs=10, steps_per_epoch=steps_epoch,
                                validation_data=(x_test, y_test),validation_steps = steps_valid)
            return save_score_dl(history)
    else:
        history = model.fit(x_train, y_train, batch_size=128, epochs=10, steps_per_epoch=steps_epoch,
                            validation_data=(x_test, y_test),validation_steps = steps_valid)
        return save_score_dl(history)