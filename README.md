# sd_extension_template

- Extension開発で変に詰まったところをテンプレ化していく
- 公式ドキュメント
  - https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Developing-extensions

# 対応バージョン

## Python

### Python 3.8以降に対応する

- 3.10をすんなり導入できるのはWindowsくらい
- ColabやROCmなどの一部環境で3.8ユーザーが残っている
- condaユーザーは3.9までしか上げられない
- pipとxformersの両立が難しいっぽい
- 3.8のEoLは2024年10月らしい...

3.8と3.9と3.10の違い

- 3.8の__file__は相対パス os.path.abspath(__file__) で絶対パスに出来る
- 3.9以前はmatch構文が使えないのでifで代用する

## Git

- 勝手に lfs をインストールしたいが、やりすぎな感もある。

## CUDA

- 11.6でも大丈夫そう

## requirements.txt記載のモジュール

- 本体バージョンに従うのが無難
- 本体が勝手にバージョンアップするが従わざるを得ない

# ファイル名と場所

## リポジトリ名

- ハイフンは使わずアンダーバーを使ったほうが無難。
- ハイフンを使ったディレクトリのインポートは importlib が必要になる。

## Extensionの入ったフォルダ名の変更

- 1111本体の機能として指定可能だが対応が結構難しい。
  - たとえば sd_dreambooth_extension は動作しない。
- 作者としては可能な限りで対応する。
- ユーザーとしては名前を変更しないで使うほうが無難。

## install.py

- インストール時と起動時に毎回呼ばれる。
- なので重たい処理は厳禁。

基本は launch.pyを使って pip install を行う程度。

```python
import launch

if not launch.is_installed("yaml"):
    launch.run_pip("install yaml", desc='yaml')
```

込み入った処理は、成功時にフラグとなるファイルを置くと良い。

```python
import pathlib
p = pathlib.Path(__file__).parts[-3:-1]
checked_path = os.path.join(p[0], p[1], 'install.checked')
if not os.path.exists(checked_path):
    # 込み入った処理...
    pathlib.Path(checked_path).write_text('1')
```

- install.pyの中ではscripts.basedir()は使えない

## preload.py

- sd_dreambooth_extensionの作者が要望してつけた機能。
- 基本的には使わないほうが良い。
  - コマンドラインオプションを追加してからExtensionを外すと1111本体が起動しなくなる。
  - 自分自身の場所を知る方法が無い。

## scripts/ 内にpyファイルを置く

- ファイル名は何でもよい。
- 種類としては以下のように分かれる(他にもあるかも)。
  - API: script_callbacks.on_app_started(APIfunc)
    - --apiオプションをつけて起動するもの
  - Tab: script_callbacks.on_ui_tabs(on_ui_tabs)
    - 画面にタブとして表示されるUI
  - Script: class Script(scripts.Script)
    - txt2img/img2imgのScriptドロップダウンで選択するUI
  - その他: 上記3つの指定が無いもの
- おそらく gradio の起動時に全ファイルが一度読み込まれる。

### scripts/ 内のimport

```python
from scripts import foo, bar, baz
```

### 単体のスクリプトファイルをExtension化する方法

- scripts/foo.py ごとgitリポジトリに入れるだけ
- あとは1111本体がやってくれる

## scripts/ 外にpyファイルを置く

- たとえば py/ ディレクトリを作りたいとする。
- scriptsからpyディレクトリを見るには from py で済む

```python
from py import foo, bar, baz
```

### pyディレクトリ内で同一ディレクトリの別ファイルをimportする

```python
from . import foo, bar, baz
from .foo import foofanc
```

### pyディレクトリから別ディレクトリのpyファイルをimportする

- しないほうが楽

```python
def example_func():
    import pathlib
    p = pathlib.Path(__file__).parts[-4:-2]
    import importlib
    example3 = importlib.import_module(f"{p[0]}.{p[1]}.py2.example3")
```

## ファイルを置かせる、ファイルを出力する

- Extensionの中に入れたほうが綺麗ではある。

```python
def get_input_dir():
    import pathlib
    p = pathlib.Path(__file__).parts[-4:-2]
    input_dir = os.path.join(p[0], p[1], 'input')
    return input_dir
```

### 設定ファイルやログファイルを置く

- ファイルはgitに入れない(pull時に上書きして初期化してしまうので)
- ディレクトリを作ったほうがベター

```python
def get_config_path():
    import pathlib
    p = pathlib.Path(__file__).parts[-4:-2]
    config_path = os.path.join(p[0], p[1], 'json', 'config.json')
    return config_path
```

# Gradio

- Gradio Docsに書いてないことが多すぎる。

## Blocks

- 基本的には大量のwithで掘り下げていく
- Tabにはイベントが無いはず
- Boxにはlabelが無く、最初のオブジェクトのlabelが使われる
- すべてのオブジェクトは gradio 起動時に描画される
  - 重いリスト表示とかはボタンを押してから読み込む仕組みにしたほうが無難

## update()

- 外からのオブジェクトのアップデートはどうもうまくいかない
- イベントのoutputsに指定すれば動くが挙動が限定的
- 凝ったUIを思いついたときはそれが本当に実装できるか最初に試す

## change()

- 多重定義をすると無限ループを起こす
- たとえばドロップダウンAを選択するとドロップダウンBの内容が変わり、ドロップダウンBを選択するとテキストボックスに値が入る、というのは無理
- そういう処理はボタンを挟む

## Textbox

- linesは内容に応じた可変にはならない
- interactive=Falseでもリサイズできる
- 文字列は勝手にunescape()される。この仕様はWindowsでpathを扱うときにとても困る
  - 有効な回避策は入力時点でスラッシュにしておくこと

## Image

- change()を使っていいのはそれで作業フローが終わる時だけ
- アップロード完了後にクリアして別のファイルをアップロードするにはユーザーが×ボタンを押すしかない
- サイズがでかくてうざい

## Audio

- 1ファイルしか再生できないので非常に不便

## Files

- ユーザーにダウンロードを促す方法はこれしかない
- 自動的にダウンロードを開始することもできない
- 表示内容をいじることもできない
- 処理するとtmpフォルダにファイルのコピーをとる
  - 複数ファイルに対応できるが全ファイルのコピーをとるので要注意

## テーブル表示

- gradioにはオブジェクトつきの一覧表示をする機能が無い
- tableタグとstyle.cssとjavascriptで頑張って実装することになる

## イベント

- .click() とか
- インデントレベルは with gr.Blocks() と同じ階層

### _js

- ドキュメントにない引数
- javascriptの関数名を入れる
- fnより先に呼ばれる
- returnの内容がinputs[]に上書きされる
  - returnの要素数が足りないぶんはinputs[]の値が使われる

引数は使えないが無名関数が使える。

```python
_js="function(){return rows('"+tab1.lower()+"_"+tab2.lower()+"')}",
```

### fn

クラス名とメソッド名に変数を使いたい場合は getattr と globals を組み合わせる。

```python
fn=getattr(globals()[f"FilerGroup{tab1}"], f"download_{tab2.lower()}"),
```

### outputs

- 空のvalueがNoneになる時は指定することができない
  - Textboxに対して''を返して空文字列を表示させることはできる
  - Imageに対してNoneを返して画像をクリアすることはできない
