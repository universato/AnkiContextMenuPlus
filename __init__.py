from aqt import gui_hooks, mw
from aqt.qt import QAction
import webbrowser
import os

def google_search(text):
    webbrowser.open(f"https://www.google.com/search?q={text}")

def google_image_search(text):
    webbrowser.open(f"https://www.google.com/search?q={text}&udm=2")

def open_wikipedia(title):
    webbrowser.open(f"https://ja.wikipedia.org/wiki/{title}")

def open_pixiv(title):
    webbrowser.open(f"https://dic.pixiv.net/a/{title}")

def open_ansaikuropedia(title):
    webbrowser.open(f"https://m.ansaikuropedia.org/wiki/{title}")

def editor_google_search():
    editor = mw.app.activeWindow().editor
    if editor:
        selected_text = editor.web.selectedText()
        if selected_text:
            google_search(selected_text)

def webview_google_search():
    selected_text = mw.app.activeWindow().web.selectedText()
    if selected_text:
        google_search(selected_text)

def log_message(message):
    addon_folder = os.path.dirname(__file__)
    log_file = os.path.join(addon_folder, "debug_log.log")
    print(message)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def on_editor_context_menu(editor, menu):
    if mw.app.activeWindow().editor.web.selectedText().strip():
        action = QAction("Googleで検索", menu)
        action.triggered.connect(editor_google_search)
        menu.addAction(action)

def on_webview_context_menu(webview, menu):
    if mw.app.activeWindow().web.selectedText().strip():
        action = QAction("Googleで検索", menu)
        action.triggered.connect(webview_google_search)
        menu.addAction(action)

gui_hooks.editor_will_show_context_menu.append(on_editor_context_menu) # Editor
gui_hooks.webview_will_show_context_menu.append(on_webview_context_menu) # Problem
log_message("GoogleSearchAddonがロードされました")
log_message("このlogファイルがエディタなどで開かれているとアドオンがエラーになることが……閉じよ")
