# AnkiContectMenuPlus

Ankiアドオン

- 選択したテキストをコンテキストメニューから簡単に検索
- 何も選択してないときに、不要なコンテキストメニューを非表示
- 簡単にAnki内コレクションを検索できるように。

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



```log
    webbrowser.open(format_url.format(selected_text()))
  File "webbrowser", line 86, in open
  File "webbrowser", line 683, in open
UnicodeEncodeError: 'ascii' codec can't encode characters in position 47-54: ordinal not in range(128)
```
macOSでは、内部で異なるエンコード処理が行われる場合があり、特に非ASCII文字(日本語など)が含まれるとエンコードエラーが発生することがあるらしい。urllib.parse.quoteを使用することで、こうした文字を適切にエンコードし、エラーを回避できる。

URL全体をエンコードするとエラーにならないけど、何も起きなかった。
URLとして認識されてない動作に見える。
「https://」の「:」を「%3A」に変換してはならないのだと思う。

#

PyQt6.QtGui.QAction

# HTMLからPythonを呼ぶ

```py
def search_in_collection2(text):
    browser = dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()

def on_js_message(handled, message, context):
    if message.startswith('search_button('):
        search_in_collection2(message[14:-1])
        return True, False
    return handled

gui_hooks.webview_did_receive_js_message.append(on_js_message)
```

```html
<span class="link_button" onclick="pycmd('search_button({{Back}})')">Anki</span>
```

# Anki


```py anki/qt/tools/genhooks_gui.py
    Hook(
        name="webview_did_receive_js_message",
        args=["handled: tuple[bool, Any]", "message: str", "context: Any"],
        return_type="tuple[bool, Any]",
        doc="""Used to handle pycmd() messages sent from Javascript.

Message is the string passed to pycmd().

For messages you don't want to handle, return 'handled' unchanged.

If you handle a message and don't want it passed to the original
bridge command handler, return (True, None).

If you want to pass a value to pycmd's result callback, you can
return it with (True, some_value).

Context is the instance that was passed to set_bridge_command().
It can be inspected to check which screen this hook is firing
in, and to get a reference to the screen. For example, if your
code wishes to function only in the review screen, you could do:

            if not isinstance(context, aqt.reviewer.Reviewer):
                # not reviewer, pass on message
                return handled

            if message == "my-mark-action":
                # our message, call onMark() on the reviewer instance
                context.onMark()
                # and don't pass message to other handlers
                return (True, None)
            else:
                # some other command, pass it on
                return handled
        """,
    ),
# 中略
    Hook(
        name="webview_will_show_context_menu",
        args=["webview: aqt.webview.AnkiWebView", "menu: QMenu"],
        legacy_hook="AnkiWebView.contextMenuEvent",
    ),
# 中略
    Hook(
        name="editor_will_show_context_menu",
        args=["editor_webview: aqt.editor.EditorWebView", "menu: QMenu"],
        legacy_hook="EditorWebView.contextMenuEvent",
    ),
```

翻訳。
Hook
    name="webview_did_receive_js_message",
    args=["handled: tuple[bool, Any]", "message: str", "context: Any"],
    return_type="tuple[bool, Any]",

JavaScriptから送信されるpycmd()メッセージを処理するために使用します。
messageはpycmd()に渡される文字列です。
処理したくないmessageについては、変更せずに 'handled' を返します。

messageを処理し、それを元のブリッジコマンドハンドラに渡したくない場合は、(True, None)を返します。

pycmdの結果コールバックに値を渡したい場合は、(True, some_value)を返します。

Contextは、set_bridge_command()に渡されたインスタンスです。
これは、このフックがどのスクリーンで実行されているかをチェックし、スクリーンへの参照を取得するために検査することができます。例えば、あなたのコードがレビュー画面でのみ機能したい場合、次のようにすることができる：

```py
if not isinstance(context, aqt.reviewer.Reviewer)：
    # reviewerではない場合、メッセージを渡す
    return handled

if message == "my-mark-action":
    # 私たちのmessage、reviewerのインスタンスでonMark()を呼び出す
    context.onMark()
    # そして他のハンドラにmessageを渡さない
    return (True, None)
else:
    # 他のコマンドに渡す
    return handled
```


```py
gui_hooks.editor_will_show_context_menu.append(on_context_menu)  # Editor
gui_hooks.webview_will_show_context_menu.append(on_context_menu)  # Problem
gui_hooks.browser_will_show_context_menu.append(on_context_menu)
gui_hooks.browser_header_will_show_context_menu.append(on_context_menu)
gui_hooks.reviewer_will_show_context_menu.append(on_context_menu)
```

下3つはエラーにならないけど、特に不要。