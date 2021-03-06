# -*- encoding:utf-8 -*-
import numpy as np

def lottery(y_pred):
    #次に予測される形態素の確率が与えられた際に抽選を行う関数
    #多項分布で抽選を行い，np.argmaxでインデックスを返す
    pred_f64 = np.asarray(y_pred).astype('float64')
    pred_norm = pred_f64/sum(pred_f64)
    hit_index = np.argmax(np.random.multinomial(1,pred_norm,1))
    return hit_index

def generator(model,seed,table,maxlen=5,eps=1):
    #文頭の形態素seedからtableに基づくインデックスのリストを作成
    seed_seq = ['<BOS>']*(maxlen-1)+[seed]
    seq_index = [table.unit2index(m) for m in seed_seq]
 
    #テキストの生成
    #<EOS>か文字20個が出力されるまでテキストを生成
    generate_list = list()
    n = 0
    next = ''
    while(n<20 and next != '<EOS>'):
        #学習済みモデルへの入力となるx_predはseq_indexのOne-Hot表現
        x_pred = np.zeros((1,maxlen,table.ret_typenum()),dtype=np.bool)
        for i,index in enumerate(seq_index):
            x_pred[0,i,index] = 1
        #x_predに基づき次の形態素を予測する確率y_predを取得
        y_pred = model.predict(x_pred,verbose=0)[0]

        #ランダムに得られたeps_choiceがeps以下の値であれば抽選
        #以上であれば最大の確率となる形態素を取得
        eps_choice = np.random.random()
        hit = np.argmax(y_pred) if eps_choice > eps else lottery(y_pred)
        next = table.index2unit(hit)

        #seq_indexの最初の形態素を捨て, 予測された形態素を最後に追加
        seq_index.pop(0)
        seq_index.append(hit)
        generate_list.append(next)
        n+=1
    
    return ''.join(seed_seq[-1:]+generate_list[:-1])