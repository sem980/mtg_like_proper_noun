# -*- encoding: utf-8 -*-

from keras.models import load_model
from UnitTable import UnitTable
from generator_func import generator
import numpy as np
import json
import re
import warnings

def passing_warn(*args,**kwargs):
    pass

def seed_gen(filename):
    #テキスト生成の際の最初の一形態素をランダムに出力
    with open(filename,'r') as f:
        seeds = json.load(f)
    return seeds

def generate_text(maxlen,model_filename,table_filename,seeds):
    #モデルの読み込む
    model = load_model(model_filename)
    #形態素や文字とインデックスの変換用テーブル
    table = UnitTable(table_filename)
    #テキスト生成用シード
    seed = np.random.choice(seeds)
    #テキスト生成
    gen = generator(model,seed,table,maxlen)
    return gen

def main():
    warnings.warn = passing_warn

    maxlen = 5
    with open('data/seed_morph.json','r') as f:
        morph_seeds = json.load(f)
    with open('data/seed_char.json','r') as f:
        char_seeds = json.load(f)
    
    context = generate_text(maxlen,'model/proper_context.h5','data/proper_mtable.json',morph_seeds)
    for i in range(len(re.findall('<p>',context))):
        name = generate_text(maxlen,'model/proper_name.h5','data/proper_ctable.json',char_seeds)
        context = re.sub('<p>',name,context,count=1)
    print(context)

if __name__ == '__main__':
    for i in range(10):
        main()