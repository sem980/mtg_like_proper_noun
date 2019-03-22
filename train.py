# -*- encoding:utf-8 -*-

from keras.callbacks import Callback
from keras.models import Sequential
from keras.layers import Dense,LSTM,BatchNormalization
from keras.optimizers import RMSprop
from UnitTable import UnitTable
import numpy as np 
import json
from generator_func import generator

def build_model(seq_size,num_class):
    #単層LSTM
    lstm = LSTM(units=128,input_shape=(seq_size,num_class))
    
    model = Sequential()
    model.add(lstm)
    model.add(BatchNormalization(axis=-1))
    model.add(Dense(num_class,activation='softmax'))
    
    model.compile(loss='categorical_crossentropy',optimizer=RMSprop(lr=0.01))
    return model

def make_seq_vec(data,unit_table,maxlen=5):
    #学習用データの整形
    #最大形態素長maxlenのシーケンスとそれに対応する次の形態素をone-hotで表現
    sentences = list()
    next_unit = list()
    
    #データから学習用シーケンスを切り取り
    for v in data:
        text = ['<BOS>']*(maxlen-1)+list(v)+['<EOS>']
        sentences.extend([text[i:i+maxlen] for i in range(0,len(text)-maxlen)])
        next_unit.extend([text[i] for i in range(maxlen,len(text))])
    
    #データを学習のためのOne-hotに整形
    x = np.zeros((len(sentences),maxlen,unit_table.ret_typenum()),dtype=np.bool)
    y = np.zeros((len(next_unit),unit_table.ret_typenum()),dtype=np.bool)
    for i ,sentence in enumerate(sentences):
        for j,unit in enumerate(sentence):
            x[i,j,unit_table.unit2index(unit)] = 1
        y[i,unit_table.unit2index(next_unit[i])] = 1
    return x,y

#学習エポック毎のコールバック
class make_proper_test(Callback):
    def __init__(self,char_table,seed_char,proper_names,**kwargs):
        super().__init__(**kwargs)
        self.names_per_epoch = dict()
        self.char_table = char_table
        self.seed_char = seed_char
        self.proper_names = proper_names
    
    def on_epoch_end(self,epoch,logs={}):
        name_list = list()
        for i in range(100):
            name_list.append(generator(self.model,self.seed_char,self.char_table,eps=1))
        unique = list(set(name_list))
        original = [i for i in list(set(unique)) if i not in self.proper_names]
        self.names_per_epoch[epoch] = name_list
        print('unique: {0}  original: {1}\n'.format(len(unique)/100,len(original)/len(unique)))

def train(maxlen,epochs,data_filename,table_filename,modelname,seed = None):
    with open(data_filename,'r') as f:
        proper = json.load(f)
    table = UnitTable(table_filename)

    #学習データ作成
    x,y = make_seq_vec(proper,table)
    #モデルデータの作成
    model = build_model(maxlen,table.ret_typenum())
    #学習
    if seed != None:
        test = make_proper_test(table,seed,proper)
        model.fit(x,y,batch_size=128,epochs=epochs,callbacks=[test])
    else:
        model.fit(x,y,batch_size=128,epochs=epochs)
    #保存
    #model.save(modelname,include_optimizer=False)

def main():
    maxlen = 5
    epochs = 15

    train(maxlen,epochs,'data/proper_names.json','data/proper_ctable.json','proper_names.h5','ア')
    train(maxlen,epochs,'data/proper_contexts.json','data/proper_mtable.json','proper_contexts.h5')

if __name__ == '__main__':
    main()