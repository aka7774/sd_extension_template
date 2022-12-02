# sd_extension_template

- Extension開発で変に詰まったところをテンプレ化していく
- 公式ドキュメント
  - https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Developing-extensions

## Python 3.8以降か3.9以降に対応する

- 3.10をすんなり導入できるのはWindowsくらい
- ColabやROCmなどの一部環境で3.8ユーザーが残っている
- condaユーザーは3.9までしか上げられない
- pipとxformersの両立が難しいっぽい
- 3.8のEoLは2024年10月らしい...

### 3.8と3.9と3.10の違い

- 3.8の__file__は相対パス os.path.abspath(__file__) で絶対パスに出来る
- 3.9以前はmatch構文が使えない

## scripts.basedir()は使えない

- 本当はExtension直下を示して欲しいのだが常にwebui直下を示している

## 基本は scripts/main.py に書く

- 他のファイル名にすると Script ドロップダウンで選択しないと動かなくなるので不便
  - 逆に txt2img/img2img専用機能であることを示すには Script ドロップダウン用にすると良いかも
- だいたいはタブを追加してその中で自由にUIを配置する実装になっているように見える

## pythonのコード置き場を作る

- main.pyに全部詰め込むと長くなるのでファイルを分割したいが、同一ディレクトリに置くとScriptドロップダウンに干渉する。
- そこで、pyファイルの置き場としてpyディレクトリを想定する
- scriptsからpyディレクトリを見るには from py で済む

### pyディレクトリ内で同一ディレクトリの別ファイルをimportする

- from .ファイル名 でいける(先頭の.が大事)

### pyディレクトリから別ディレクトリのpyファイルをimportする

- py2ディレクトリを想定する(他人が作ったモジュール等、明確な違いが無ければ同一ディレクトリにまとめたほうが楽)
- from ..py2 はエラーになるためimportilbを使う

## そのほか、Extension以下のファイルやフォルダにアクセスする

- pathlibを使って自分のpathを取得することで対応できる
- Python 3.8と3.9で__file__の取り扱いが異なるが、pathの右側から切り取れば挙動は一致するはず
