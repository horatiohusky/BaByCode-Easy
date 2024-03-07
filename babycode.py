import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import markdown2
from tkhtmlview import HTMLLabel
import threading
import bbcode

def bbcode_to_html(bbcode_text):
    """
    Convert BBCode to HTML using the bbcode package.
    """
    parser = bbcode.Parser()
    parser.add_simple_formatter('hr', '<hr />', standalone=True)
    parser.add_simple_formatter('sub', '<sub>%(value)s</sub>')
    parser.add_simple_formatter('sup', '<sup>%(value)s</sup>')
    html = parser.format(bbcode_text)
    return html

class MarkdownEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown & BBCode Editor")
        self.root.geometry("1200x600")
        self.dark_mode_active = False
        self.create_widgets()
        self.apply_light_theme()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Welcome to the markdown/bbcode editor, friend! <3", font=("Helvetica", 16))
        self.title_label.pack(side=tk.TOP, fill=tk.X)
        
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.edit_frame = ttk.Frame(self.paned_window, width=600, height=600)
        self.preview_frame = ttk.Frame(self.paned_window, width=600, height=600)
        
        self.paned_window.add(self.edit_frame, weight=1)
        self.paned_window.add(self.preview_frame, weight=1)
        
        self.text_area = tk.Text(self.edit_frame, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=1)
        self.text_area.config(wrap="word")
        
        self.buttons_frame = tk.Frame(self.edit_frame)
        self.buttons_frame.pack(side=tk.BOTTOM, pady=10)

        self.update_preview_button = tk.Button(self.buttons_frame, text="Update Preview", command=self.update_preview)
        self.update_preview_button.grid(row=0, column=0, padx=5, pady=5)

        self.open_file_button = tk.Button(self.buttons_frame, text="Open File", command=self.open_file)
        self.open_file_button.grid(row=0, column=1, padx=5, pady=5)

        self.save_file_button = tk.Button(self.buttons_frame, text="Save File", command=self.save_file)
        self.save_file_button.grid(row=1, column=0, padx=5, pady=5)

        self.markdown_syntax_button = tk.Button(self.buttons_frame, text="Markdown Syntax", command=self.show_markdown_syntax)
        self.markdown_syntax_button.grid(row=1, column=1, padx=5, pady=5)

        self.toggle_theme_button = tk.Button(self.buttons_frame, text="Toggle Theme", command=self.toggle_theme)
        self.toggle_theme_button.grid(row=2, column=0, padx=5, pady=5)

        self.html_preview = HTMLLabel(self.preview_frame, html="<h3>Live Preview</h3>")
        self.html_preview.pack(fill=tk.BOTH, expand=True)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)

    def update_preview(self):
        content = self.text_area.get(1.0, tk.END)
        html_content = markdown2.markdown(bbcode_to_html(content), extras=["fenced-code-blocks", "tables", "spoiler"])
        self.html_preview.set_html(html_content)

    def show_markdown_syntax(self):
        messagebox.showinfo("Markdown Syntax", "Basic syntax help goes here...")

    def toggle_theme(self):
        self.dark_mode_active = not self.dark_mode_active
        self.apply_dark_theme() if self.dark_mode_active else self.apply_light_theme()

    def apply_light_theme(self):
        self.text_area.config(bg="white", fg="black")
        self.html_preview.config(bg="white", fg="black")
        self.root.config(bg="white")

    def apply_dark_theme(self):
        self.text_area.config(bg="#2d2d2d", fg="white")
        self.html_preview.config(bg="#2d2d2d", fg="white")
        self.root.config(bg="#2d2d2d")

def launch_main_app():
    splash_root.destroy()
    root = tk.Tk()
    app = MarkdownEditor(root)
    root.mainloop()

def show_splash_screen():
    global splash_root
    splash_root = tk.Tk()
    splash_root.title("Welcome!")
    splash_root.geometry("400x250")
    message = tk.Label(splash_root, text="🎉 Welcome to Markdown Party! by HoratioHusky! 🐾\nA cute and fun way to edit your Markdown/BBCode documents! 📝❤️ Click 'Launch Editor' to start.", justify="center")
    message.pack(pady=(40, 20))

    launch_button = tk.Button(splash_root, text="Launch Editor 🚀", command=launch_main_app)
    launch_button.pack()

    splash_root.mainloop()

show_splash_screen()
	
