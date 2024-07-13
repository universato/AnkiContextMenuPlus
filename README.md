
# Macのターミナルから開くとき

単に開くとき
```console
open -a Anki
```

デバッグできるように開くとき ※ print()が出力される。
```console
/Applications/Anki.app/Contents/MacOS/Anki 
```
※ これで開くと、動作が変わることがある。

普通に開くとエンコードエラーになるところが、
`open -a Anki`でも`/Applications/Anki.app/Contents/MacOS/Anki`でも
ターミナルで開くと無理やりエンコードしたぽいで検索する。ex)コンパイラ->ÉRÉìÉpÉCÉâ


# MacとWindowsの違い

Macのwebview(問題を解くとき)だけうまくいかない。タイミングが揃わない。
```py
def search_in_collection():
    browser = dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(selected_text())
    browser.onSearchActivated()
```
↓
Browserを開く前に対象テキストを取得する。
```py
def search_in_collection():
    search_text = selected_text()
    browser = dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(search_text)
    browser.onSearchActivated()
```

# Python基本動作

```py
import urllib.parse
text = "あい"
print(text) #=> あい
print(urllib.parse.quote(text)) #=> %E3%81%82%E3%81%84
```

```py
import urllib.parse
text = " /+&:=?"
print(text) #=>   /+&:=?
print(urllib.parse.quote(text)) #=> %20/%2B%26%3A%3D%3F
```
・半角スペースは`%20`
・`/`はそのまま出力される。



```
    webbrowser.open(format_url.format(selected_text()))
  File "webbrowser", line 86, in open
  File "webbrowser", line 683, in open
UnicodeEncodeError: 'ascii' codec can't encode characters in position 47-54: ordinal not in range(128)
```
macOSでは、内部で異なるエンコード処理が行われる場合があり、特に非ASCII文字(日本語など)が含まれるとエンコードエラーが発生することがあるらしい。urllib.parse.quoteを使用することで、こうした文字を適切にエンコードし、エラーを回避できる。

URL全体をエンコードするとエラーにならないけど、何も起きなかった。
URLとして認識されてない動作に見える。
「https://」の「:」を「%3A」に変換してはならないのだと思う。