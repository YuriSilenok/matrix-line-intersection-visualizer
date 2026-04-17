def center_window(window):
    """Центрирование окна относительно родителя"""
    window.update_idletasks()
    x = window.parent.winfo_x() + (window.parent.winfo_width() // 2) - (window.winfo_width() // 2)
    y = window.parent.winfo_y() + (window.parent.winfo_height() // 2) - (window.winfo_height() // 2)
    window.geometry(f"+{x}+{y}")