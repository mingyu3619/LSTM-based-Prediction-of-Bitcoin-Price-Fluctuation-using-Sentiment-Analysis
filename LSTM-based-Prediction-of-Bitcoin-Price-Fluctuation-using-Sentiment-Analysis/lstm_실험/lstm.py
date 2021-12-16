import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.layers import LSTM
from keras import backend as K
import tensorflow as tf


################################################################################################################
def make_dataset(data, label, window_size=1):
    feature_list = []
    label_list = []
    for i in range(len(data) - window_size):
        feature_list.append(np.array(data.iloc[i:i+window_size]))
        label_list.append(np.array(label.iloc[i+window_size]))
    return np.array(feature_list), np.array(label_list)
################################################################################################################
dens=[32]
TEST_SIZE=260
score=[]
for den in dens:
    score=[]
    for i in range(1,2):

        print("i order:",i)
        data_path="C:\\Users\\d\\PycharmProjects\\LSTM_4news_1window"
        df_price = pd.read_csv(os.path.join(data_path, 'merge.csv'), encoding='euc-kr')
        df_price.describe()

        pd.to_datetime(df_price['일자'], format='%Y-%m-%d')


        df_price['일자'] = pd.to_datetime(df_price['일자'], format='%Y-%m-%d')
        df_price['연도'] =df_price['일자'].dt.year
        df_price['월'] =df_price['일자'].dt.month
        df_price['일'] =df_price['일자'].dt.day

        plt.figure(figsize=(16, 9))
        sns.lineplot(y=df_price['등락'], x=df_price['일자'])
        plt.xlabel('time')
        plt.ylabel('price')


        #plt.show()

        scaler = MinMaxScaler()

        scale_cols = ['수치','등락']
        #scale_cols = ['수치', '비율', '기사', '등락']
        df_scaled = scaler.fit_transform(df_price[scale_cols])              #########9천 몇까지 뜸

        df_scaled=df_price
        df_scaled = pd.DataFrame(df_scaled[scale_cols])
        df_scaled.columns = scale_cols

        print(df_scaled)

        train = df_scaled[:-TEST_SIZE]
        test = df_scaled[-TEST_SIZE:]

        feature_cols=['수치']
        print(feature_cols)
        #feature_cols = ['수치', '비율', '기사']
        label_cols = ['등락']

        train_feature = train[feature_cols]
        train_label = train[label_cols]
        print(train_feature)
        # train dataset
        train_feature, train_label = make_dataset(train_feature, train_label, 20)

        x_train, x_valid, y_train, y_valid = train_test_split(train_feature, train_label, test_size=0.2)
        print(x_train)
        x_train.shape, x_valid.shape
        print(x_train.shape, x_valid.shape)



        test_feature = test[feature_cols]          ###없던거
        test_label = test[label_cols]


        test_feature, test_label = make_dataset(test_feature,test_label, 20)                   #####################
        test_feature.shape, test_label.shape

        print(test_feature.shape, test_label.shape)




        model = Sequential()

        model.add(LSTM(den,
                       input_shape=(train_feature.shape[1], train_feature.shape[2]),
                       return_sequences=True)
                  )
        model.add(LSTM(den,
                       input_shape=(train_feature.shape[1], train_feature.shape[2]),
                       return_sequences=False)
                  )
        #model.add(LSTM(20, return_sequences = True))
        #model.add(Dense(den,activation='relu'))
        model.add(Dense(1,activation='sigmoid'))

        #mean_squared_error
        model.compile(loss='binary_crossentropy', optimizer='adam',metrics='accuracy')
        early_stop = EarlyStopping(monitor='val_loss', patience=5)

        filename = os.path.join(data_path, 'hid_'+str(den)+'__'+str(i)+'번째'+'.h5')

        checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')



        history = model.fit(x_train, y_train,
                            epochs=200,
                            batch_size=1,
                            validation_data=(x_valid, y_valid),
                            callbacks=[early_stop,checkpoint])
        model.save("model.h5")
        val_loss = history.history['val_loss']
        val_acc = history.history['val_accuracy']
        print("val:",val_loss,"acc:",val_acc)
        plt.figure(111)
        plt.plot(val_acc, label='acc')
        plt.plot(val_loss, label='loss')



        print("model.evaluate")
        scores = model.evaluate(test_feature, test_label,batch_size=1)
        print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))
        pred_before=model.predict(test_feature)
        pred = model.predict_classes(test_feature)
        print(pred,pred_before)
        print(pred.shape)

        plt.figure(figsize=(12, 9))
        plt.title('i번째: %d Accuracy: %.2f%%' % (i, scores[1] * 100))
        plt.plot(test_label, label='actual')
        plt.plot(pred, label='prediction')

        plt.legend()
        plt.savefig('hidden_'+str(den)+'__'+str(i)+'order'+'accuracy_'+ str(scores[1]*100)+'.png')
        model.summary()

        # f=open("output.txt","w",encoding="utf-8")
        # for i in pred_before:
        #     print(i)
        #     f.write(str(i))
        # f.close()
