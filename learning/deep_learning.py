from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.regularizers import l2
import keras
from learning_base import LearningBase
from keras.callbacks import EarlyStopping



class DeepLearning(LearningBase):
    def run_learning(self, test_size=0.3, output_activation='sigmoid', output_size=1, random_state=None):
        self._divide_test_train(test_size, random_state=random_state)
        # create model
        print self._features_train.shape[1]
        early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=50,mode='min', verbose=1)
        self._classifier = Sequential()
        self._classifier.add(Dense(300, activation="relu", kernel_initializer="he_normal", input_dim=self._features_train.shape[1]))
        self._classifier.add(Dropout(0.2))
        self._classifier.add(Dense(100, init='he_normal', activation='relu', W_regularizer=l2(0.1)))
        self._classifier.add(Dropout(0.2))
        self._classifier.add(Dense(output_size, init='uniform', activation=output_activation, W_regularizer=l2(0.01)))

        # self.classifier.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Fit the model
        if(output_activation == 'softmax'):
            self._classifier.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            self._tags_train = keras.utils.to_categorical(self._tags_train, num_classes=max(self._tags_train)+1)
            self._tags_test = keras.utils.to_categorical(self._tags_test, num_classes=max(self._tags_test)+1)
        else:
            self._classifier.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        self._classifier.fit(self._features_train, self._tags_train,
                             validation_split=0.1, callbacks=[early_stopping],
                             epochs=1000, batch_size=10, verbose=2)

        return self._classifier

