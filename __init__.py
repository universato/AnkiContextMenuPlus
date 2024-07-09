from aqt import gui_hooks, mw
from aqt.qt import QAction
import webbrowser
import os

def google_search():
    editor = mw.app.activeWindow().editor
    if editor:
        selected_text = editor.web.selectedText()
        if selected_text:
            url = f"https://www.google.com/search?q={selected_text}"
            webbrowser.open(url)
            log_message(f"Searching for: {selected_text}")

def log_message(message):
    addon_folder = os.path.dirname(__file__)
    log_file = os.path.join(addon_folder, "debug_log.log")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def on_context_menu(webview, menu):
    action = QAction("Googleで検索", menu)
    action.triggered.connect(google_search)
    menu.addAction(action)
    log_message("Google検索オプションが追加されました")

gui_hooks.editor_will_show_context_menu.append(on_context_menu)
log_message("GoogleSearchAddonがロードされました")
log_message("このlogファイルがエディタなどで開かれているとアドオンがエラーになることが……閉じよ")
