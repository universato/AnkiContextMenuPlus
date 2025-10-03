from aqt import mw, dialogs, gui_hooks
from aqt.qt import QAction
from datetime import datetime, timedelta
import os
import urllib.parse
import webbrowser


def open_selected_text_web(format_url) -> None:
    webbrowser.open(format_url.format(urllib.parse.quote(selected_text())))


def google_search() -> None:
    open_selected_text_web("https://www.google.com/search?q={}")


def google_image_search() -> None:
    open_selected_text_web("https://www.google.com/search?q={}&udm=2")


def open_wikipedia() -> None:
    open_selected_text_web("https://ja.wikipedia.org/wiki/{}")


def search_in_anki_collection():
    search_text = selected_text()
    browser = dialogs.open('Browser', mw)
    browser.form.searchEdit.lineEdit().setText(search_text)
    browser.onSearchActivated()


def open_pixiv_dic() -> None:
    open_selected_text_web("https://dic.pixiv.net/a/{}")


def open_niconico_dic() -> None:
    open_selected_text_web("https://dic.nicovideo.jp/a/{}")


def twitter_search() -> None:
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str: str = tomorrow.strftime('%Y-%m-%d')
    url = "https://x.com/search?f=live&q={}".format(
        urllib.parse.quote(f"{selected_text()} lang:ja until:{tomorrow_str}"))
    webbrowser.open(url)


def open_ansaikuropedia() -> None:
    open_selected_text_web("https://ansaikuropedia.org/wiki/{}")


def selected_text() -> str:
    obj = mw.app.activeWindow()
    if hasattr(obj, 'editor'):
        obj = obj.editor
    if hasattr(obj, 'web'):
        return obj.web.selectedText().strip()
    else:
        return ''


def log_message(message: str) -> None:
    addon_folder = os.path.dirname(__file__)
    log_file: str = os.path.join(addon_folder, 'debug_log.log')
    print(message)
    # 'このlog fileがサクラエディタ等で開かれていると書き込めなくてエラー'
    # with open(log_file, 'a', encoding='utf-8') as f:
    #     f.write(message + "\n")

# _webview: aqt.webview.AnkiWebView or aqt.editor.EditorWebView
# menu: QMenu
def on_context_menu(_webview, menu) -> None:
    if selected_text():
        actions = [
            ('Googleで検索', google_search),
            ('Googleで画像を検索', google_image_search),
            ('Wikipedia', open_wikipedia),
            ('Anki内で検索', search_in_anki_collection),
            ('Pixiv百科事典', open_pixiv_dic),
            ('Twitter', twitter_search),
            ('ニコニコ大百科', open_niconico_dic),
            ('アンサイクロペディア', open_ansaikuropedia),
        ]

        for title, func in actions:
            action = QAction(title, menu)
            action.triggered.connect(func)
            menu.addAction(action)
    else:
        for action in menu.actions():
            if action.text() in ('Copy', 'コピー', 'Cut', 'カット'):
                menu.removeAction(action)


gui_hooks.editor_will_show_context_menu.append(on_context_menu)  # Editor
gui_hooks.webview_will_show_context_menu.append(on_context_menu)  # Problem


def search_in_anki_collection2(text) -> None:
    browser = dialogs.open('Browser', mw)
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()

# args=["handled: tuple[bool, Any]", "message: str", "context: Any"],
# return_type="tuple[bool, Any]",
def on_js_message(handled, message, _context):
    if message.startswith('search_button('):
        search_in_anki_collection2(message[14:-1])
        return (True, None)
    return handled


gui_hooks.webview_did_receive_js_message.append(on_js_message)
