from aqt import gui_hooks, mw
from aqt.qt import QAction
import webbrowser
import os
from datetime import datetime, timedelta

def google_search()-> None:
    webbrowser.open(f"https://www.google.com/search?q={selected_text()}")

def google_image_search() -> None:
    webbrowser.open(f"https://www.google.com/search?q={selected_text()}&udm=2")

def open_wikipedia()-> None:
    webbrowser.open(f"https://ja.wikipedia.org/wiki/{selected_text()}")

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
    return obj.web.selectedText()

def log_message(message:str) -> None:
    addon_folder = os.path.dirname(__file__)
    log_file:str = os.path.join(addon_folder, "debug_log.log")
    print(message)
    ## "このlog fileがサクラエディタ等で開かれていると書き込めなくてエラー"
    # with open(log_file, "a", encoding="utf-8") as f:
    #     f.write(message + "\n")

def on_context_menu(_webview, menu)-> None:
    if selected_text().strip():
        action = QAction("Googleで検索", menu)
        action.triggered.connect(google_search)
        menu.addAction(action)

        action2 = QAction("Googleで画像を検索", menu)
        action2.triggered.connect(google_image_search)
        menu.addAction(action2)

        action3 = QAction("Wikipedia", menu)
        action3.triggered.connect(open_wikipedia)
        menu.addAction(action3)

        action4 = QAction("Pixiv大百科", menu)
        action4.triggered.connect(open_pixiv)
        menu.addAction(action4)

        action5 = QAction("Twitter", menu)
        action5.triggered.connect(twitter_search)
        menu.addAction(action5)

        action6 = QAction("ニコニコ大百科", menu)
        action6.triggered.connect(open_niconico_pedia)
        menu.addAction(action6)

        action7 = QAction("アンサイクロペディア", menu)
        action7.triggered.connect(open_ansaikuropedia)
        menu.addAction(action7)

gui_hooks.editor_will_show_context_menu.append(on_context_menu) # Editor
gui_hooks.webview_will_show_context_menu.append(on_context_menu) # Problem
# log_message("GoogleSearchAddonがロードされました")
