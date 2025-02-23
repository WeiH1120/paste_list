import tkinter as tk
import platform

system_name = platform.system()
if system_name == "Darwin":   # macOS 的識別名稱
    from pynput import keyboard as keyboard_mac
    from pynput.keyboard import Controller
    from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
    clipboard_key = {keyboard_mac.Key.cmd, keyboard_mac.Key.ctrl, keyboard_mac.KeyCode(char='v')}
    paste_key = {keyboard_mac.Key.cmd, keyboard_mac.KeyCode(char='v')}
elif system_name == "Windows":
    import keyboard
    clipboard_key =  "ctrl+windows+v"
    paste_key = "ctrl+v"
else:
    import keyboard
    clipboard_key =  "ctrl+windows+v"
    paste_key = "ctrl+v"

 
class paste_list:
    def __init__(self, root):
        self.root = root
        self.root.title("Paste List")
        self.clipboard_history = []
        self.max_items = 30
        self.history_window = None
 
        self.create_widgets()
        self.setup_keyboard_listener()
 
    def create_widgets(self):
        # app主視窗
        self.label = tk.Label(self.root, text="Clipboard History")
        self.root.geometry("200x50")
        self.root.resizable(False, False)
 
        self.max_items_label = tk.Label(self.root, text="Max Items:")
        self.max_items_label.grid(row=0, column=0)
 
        self.max_items_entry = tk.Entry(self.root, width=7)
        self.max_items_entry.insert(0, str(self.max_items))
        self.max_items_entry.grid(row=0, column=1)
 
        self.update_button = tk.Button(self.root, text="Update", command=self.update_max_items)
        self.update_button.grid(row=1, column=0)
 
        self.close_button = tk.Button(self.root, text="Close the app", command=self.root.quit)
        self.close_button.grid(row=1, column=1)
       # self.label.pack()
    def update_max_items(self):
        try:
            self.max_items = int(self.max_items_entry.get())
        except ValueError:
            self.max_items_entry.delete(0, tk.END)
            self.max_items_entry.insert(0, str(self.max_items))
        self.clipboard_history = self.clipboard_history[-self.max_items:]
 
    def setup_keyboard_listener(self):
        if system_name == "Darwin":
            def on_press(key):
                if all(k in self.pressed_keys for k in clipboard_key):
                    self.show_clipboard_history()
            def on_release(key):
                try:
                    self.pressed_keys.remove(key)
                except KeyError:
                    pass
            self.pressed_keys = set()
            listener = keyboard_mac.Listener(on_press=lambda key: self.pressed_keys.add(key) or on_press(key),
                                        on_release=on_release)
            listener.start()
        elif system_name == "Windows":
            keyboard.add_hotkey(clipboard_key, self.show_clipboard_history)
        else:
            keyboard.add_hotkey(clipboard_key, self.show_clipboard_history)
        
    def show_clipboard_history(self):
        if system_name == "Darwin":
            self.original_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        else:
            self.original_app = None
        if not self.clipboard_history:
            return
        if self.history_window and self.history_window.winfo_exists():
            self.history_window.lift()
            self.history_window.focus_force()
            return
        self.history_window = tk.Toplevel(self.root)
        self.history_window.title("Select Clipboard Item")
        self.history_window.geometry("300x200")
        self.history_window.bind('<Left>', self.previous_item)
        self.history_window.bind('<Right>', self.next_item)
        self.history_window.bind('<Return>', self.select_item)
        self.history_window.bind('<Escape>', self.close_clipboard)
        self.history_window.attributes('-topmost', True)
        self.history_window.focus_force()
 
        display_text = f"Item {str(len(self.clipboard_history))} of {str(len(self.clipboard_history))}\n" + \
            "____________________\n" + \
            self.clipboard_history[-1]
        self.history_label = tk.Label(self.history_window, text=display_text)
        self.history_label.pack()
        self.current_index = len(self.clipboard_history) - 1
    def previous_item(self, event):
        if self.current_index > 0:
            self.current_index -= 1
            display_text = f"Item {str(self.current_index + 1)} of {str(len(self.clipboard_history))}\n" + \
                       "____________________\n" + \
                       self.clipboard_history[self.current_index]
            self.history_label.config(text=display_text)
 
    def next_item(self, event):
        if self.current_index < len(self.clipboard_history) - 1:
            self.current_index += 1
            display_text = f"Item {str(self.current_index + 1)} of {str(len(self.clipboard_history))}\n" + \
                       "____________________\n" + \
                       self.clipboard_history[self.current_index]
            self.history_label.config(text=display_text)
 
    def select_item(self, event):
        selected_text = self.clipboard_history[self.current_index]
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)
        self.history_window.destroy()
        if system_name == "Darwin":
            self.original_app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            keyboard_controller = Controller()
            keyboard_controller.press(keyboard_mac.Key.cmd)
            keyboard_controller.press('v')
            keyboard_controller.release('v')
            keyboard_controller.release(keyboard_mac.Key.cmd)
        elif system_name == "Windows":
            # keyboard.write(selected_text)  # 觸發貼上文字到當前游標處
            keyboard.send(paste_key)  # 觸發貼上文字到當前游標處
        else:
            keyboard.send(paste_key)  # 觸發貼上文字到當前游標處
 
    def close_clipboard(self, event):
        if self.history_window:
            self.history_window.destroy()
 
    def add_to_clipboard_history(self, text):
        if text not in self.clipboard_history:
            self.clipboard_history.append(text)
            if len(self.clipboard_history) > self.max_items:
                self.clipboard_history.pop(0)
 
if __name__ == "__main__":
    root = tk.Tk()
    # root.withdraw()  # 隱藏主視窗
    app = paste_list(root)
 
    def on_clipboard_change():
        try:
            text = root.clipboard_get()
            app.add_to_clipboard_history(text)
        except tk.TclError:
            pass
        root.after(1000, on_clipboard_change)
 
    root.after(1000, on_clipboard_change)
    root.mainloop()