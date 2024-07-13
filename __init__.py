from aqt import dialogs
from aqt import gui_hooks, mw
from aqt.qt import QAction
from datetime import datetime, timedelta
import os
import webbrowser

def google_search()-> None:
    webbrowser.open(f"https://www.google.com/search?q={selected_text()}")

def google_image_search() -> None:
    webbrowser.open(f"https://www.google.com/search?q={selected_text()}&udm=2")

def open_wikipedia()-> None:
    webbrowser.open(f"https://ja.wikipedia.org/wiki/{selected_text()}")

def search_in_collection():
    browser = dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(selected_text())
    browser.onSearchActivated()

def open_pixiv()-> None:
    webbrowser.open(f"https://dic.pixiv.net/a/{selected_text()}")

def open_niconico_pedia() -> None:
    webbrowser.open(f"https://dic.nicovideo.jp/a/{selected_text()}")

def twitter_search() -> None:
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    webbrowser.open(f"https://x.com/search?q={selected_text()} lang:ja until:{tomorrow_str}&f=live")

def open_ansaikuropedia()-> None:
    webbrowser.open(f"https://m.ansaikuropedia.org/wiki/{selected_text()}")

def selected_text() -> str:
    obj = mw.app.activeWindow()
    if hasattr(obj,'editor'):
        obj = obj.editor
    return obj.web.selectedText().strip()

def log_message(message:str) -> None:
    addon_folder = os.path.dirname(__file__)
    log_file:str = os.path.join(addon_folder, "debug_log.log")
    print(message)
    ## "このlog fileがサクラエディタ等で開かれていると書き込めなくてエラー"
    # with open(log_file, "a", encoding="utf-8") as f:
    #     f.write(message + "\n")

def on_context_menu(_webview, menu) -> None:
    if selected_text():
        actions = [
            ("Googleで検索", google_search),
            ("Googleで画像を検索", google_image_search),
            ("Wikipedia", open_wikipedia),
            ("Anki内で検索", search_in_collection),
            ("Pixiv大百科", open_pixiv),
            ("Twitter", twitter_search),
            ("ニコニコ大百科", open_niconico_pedia),
            ("アンサイクロペディア", open_ansaikuropedia),
        ]

        for title, func in actions:
            action = QAction(title, menu)
            action.triggered.connect(func)
            menu.addAction(action)

gui_hooks.editor_will_show_context_menu.append(on_context_menu) # Editor
gui_hooks.webview_will_show_context_menu.append(on_context_menu) # Problem
