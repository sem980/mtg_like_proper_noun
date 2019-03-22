## MtG風Text Generation 2@ LSTM
LSTMを用いたMtG風固有名詞生成<br>
学習にMtGのフレーバーテキストを使用

[参考 : keras/example/lstm_text_generation.py](https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py)

## 環境
python 3.6.2<br>
tensorflow 1.12.0<br>
keras 2.2.4

## データセット
<dl>
<dt>data/mtg_names.json</dt>
<dd>MtG公式APIを使って収集した日本語フレーバーテキストから得られた固有名詞</dd>
<dt>data/mtg_contexts.json</dt>
<dd>MtG公式APIを使って収集した日本語フレーバーテキストから得られた固有名詞に付属する肩書など(収集の粒度は荒いです)</dd>
<dt>data/seed_char.json</dt>
<dt>data/seed_morph.json</dt>
<dd>テキスト生成時にseedとして用いる形態素や文字</dd>
<dt>proper_mtable.json</dt>
<dt>proper_ctable.json</dt>
<dd>インデックス⇔形態素/文字の変換を行うための辞書型データ</dd>
<dl>

[MtG公式API](https://docs.magicthegathering.io/)

## sample
10文を生成

+ 暁の光の巻物射手、師範
+ 寛大なるフロカラス
+ 女王直属の副王、ポッフィーマ
+ 錆錨亭の番人、ゾギャイ
+ 蛇の毒の謎々
+ 反目殺しのデジェム
+ 独り唄のラディシュ、「ノト家の」
* 鍛冶屋の隠居、サチュヴィスチ
* 縫い師、プロコピオス
* 先導隊長、ブロフニーレ

肩書などはほぼそのままMtGのものが出やすくなっている