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
- 込み入った処理は、成功時にフラグとなるファイルを置くと良い。

基本は launch.pyを使って pip install を行う程度。

```python
import launch

if not launch.is_installed("yaml"):
    launch.run_pip("install yaml", desc='yaml')
```

install.pyの中では
- __file__が使えない
- scripts.basedir()は使えない

## preload.py

- sd_dreambooth_extensionの作者が要望してつけた機能。
- 基本的には使わないほうが良い。
  - コマンドラインオプションを追加してからExtensionを外すと1111本体が起動しなくなる。
  - 自分自身の場所を知る方法が無い。

- 本当はExtension直下を示して欲しいのだが常にwebui直下を示している

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
def example_func():
    import pathlib
    p = pathlib.Path(__file__).parts[-4:-2]
    input_dir = os.path.join(p[0], p[1], 'input')
```

### 設定ファイルやログファイルを置く

- ファイルはgitに入れない(pull時に上書きして初期化してしまうので)
- ディレクトリを作ったほうがベター

```python
def get_config_path():
    import pathlib
    p = pathlib.Path(__file__).parts[-4:-2]
    input_dir = os.path.join(p[0], p[1], 'json', 'config.json')
```
