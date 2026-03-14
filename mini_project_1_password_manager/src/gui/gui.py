'''Graphical User Interface for the Password Manager'''
from core.password_entries import Passwords
from core.save_data import save_data
import customtkinter as ctk

def copy_to_clipboard(root, password):
    root.clipboard_clear()
    root.clipboard_append(password)

def toggle_password(label, password):
    if label.cget("text") == "*" * len(password):
        label.configure(text=password)
    else:
        label.configure(text="*" * len(password))


class Login_page:

    def __init__(self, check_function):
        self.password = None
        self.check_function = check_function
    
    def setPassword(self, entry):
        password = entry.get()
        if self.check_function(password):
            self.password = password
            self.root.destroy()
        else:
            self.error_label.configure(text="Invalid master password", text_color="#E74C3C")
            entry.delete(0, 'end')

    def login_page(self):
        self.root = ctk.CTk()
        self.root.geometry("400x350")
        self.root.title("PM - Login")

        # Container
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title field
        title_label = ctk.CTkLabel(main_frame, text="🔒", font=("Arial", 40))
        title_label.pack(pady=(0, 10))

        title_text = ctk.CTkLabel(main_frame, text="Vault Locked", 
                                font=ctk.CTkFont(size=22, weight="bold"))
        title_text.pack(pady=(0, 25))

        # Password field
        entry = ctk.CTkEntry(main_frame, 
                            placeholder_text="Master Password", 
                            show="*", 
                            width=250, 
                            height=40,
                            border_color="#85B33C")
        entry.pack(pady=5)
        
        entry.focus()
        self.root.bind('<Return>', lambda event: self.setPassword(entry))

        # Submit button
        submit_button = ctk.CTkButton(
            main_frame,
            text="Unlock",
            width=250,
            height=40,
            font=ctk.CTkFont(weight="bold"),
            command=lambda: self.setPassword(entry),
            fg_color="#85B33C",
            hover_color="#6D9331"
        )
        submit_button.pack(pady=(15, 5))

        # Error Label
        self.error_label = ctk.CTkLabel(main_frame, text="", font=("Arial", 12))
        self.error_label.pack(pady=5)

        self.root.mainloop()
        
def main_menu(password_list, keySafe):
    root = ctk.CTk()
    root.geometry("850x600")
    root.title("Password Manager")

    # Header
    ctk.CTkLabel(root, text="Password Manager", font=("Arial", 24, "bold")).pack(pady=(30, 20))

    # Input
    input_frame = ctk.CTkFrame(root, fg_color="transparent")
    input_frame.pack(fill="x", padx=40, pady=(0, 20))

    s_entry = ctk.CTkEntry(input_frame, placeholder_text="Service", height=35, border_color="#AADE58")
    s_entry.pack(side="left", padx=5, expand=True, fill="x")

    u_entry = ctk.CTkEntry(input_frame, placeholder_text="Username", height=35, border_color="#AADE58")
    u_entry.pack(side="left", padx=5, expand=True, fill="x")

    p_entry = ctk.CTkEntry(input_frame, placeholder_text="Password", show="*", height=35, border_color="#AADE58")
    p_entry.pack(side="left", padx=5, expand=True, fill="x")

    add_btn = ctk.CTkButton(input_frame, text="+ Add", width=80, height=35, fg_color="#85B33C",
                            command=lambda: add_entry(keySafe, scrollable_frame, password_list, s_entry, u_entry, p_entry))
    add_btn.pack(side="left", padx=5)

    # Display
    scrollable_frame = ctk.CTkScrollableFrame(root, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True, padx=30, pady=10)
    
    scrollable_frame.grid_columnconfigure(0, weight=2) 
    scrollable_frame.grid_columnconfigure(1, weight=2)
    scrollable_frame.grid_columnconfigure(2, weight=2)
    scrollable_frame.grid_columnconfigure(3, weight=0)

    show_password_list(scrollable_frame, password_list, keySafe)
    root.mainloop()

# Button functions and password display
def add_entry(keySafe, scrollable_frame, password_list, service_label, user_label, password_label):
    service = service_label.get()
    username = user_label.get()
    password = password_label.get()
    if service == "" or username == "" or password == "":
        return

    # Add password to database
    password_list.append(Passwords(service, username, password))
    save_data(password_list, keySafe)
    show_password_list(scrollable_frame, password_list, keySafe)

    service_label.delete(0, "end")
    user_label.delete(0, "end")
    password_label.delete(0, "end")

def remove_entry(scrollable_frame, password_list, service, username, keySafe):

    # Find correct Object to remove from database
    for potential_entry in password_list:
        if potential_entry.service == service and potential_entry.username == username:
            password_list.remove(potential_entry)
            save_data(password_list, keySafe)
            show_password_list(scrollable_frame, password_list, keySafe)
            break


def show_password_list(scrollable_frame, password_list, keySafe):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Table Header
    headers = ["Service", "Username", "Password", "Actions"]
    for i, text in enumerate(headers):
        ctk.CTkLabel(scrollable_frame, text=text, font=("Arial", 12, "bold"), text_color="gray").grid(row=0, column=i, sticky="w", padx=10, pady=(0, 10))

    root = scrollable_frame.winfo_toplevel()

    for i, entry in enumerate(password_list, start=1):
        # Service
        ctk.CTkLabel(scrollable_frame, text=entry.service, font=("Arial", 13, "bold")).grid(row=i, column=0, sticky="w", padx=10, pady=8)
        
        # Username
        ctk.CTkLabel(scrollable_frame, text=entry.username, text_color="#AAAAAA").grid(row=i, column=1, sticky="w", padx=10)
        
        # Passwort label
        pw_label = ctk.CTkLabel(scrollable_frame, text="*" * len(entry.password))
        pw_label.grid(row=i, column=2, sticky="w", padx=10)

        # Button group
        btn_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        btn_frame.grid(row=i, column=3, sticky="e", padx=10)

        # Show button
        ctk.CTkButton(btn_frame, text="👁", width=35, height=28, fg_color="#333333", hover_color="#444444",
                      command=lambda l=pw_label, p=entry.password: toggle_password(l, p)).pack(side="left", padx=2)

        # Copy button
        ctk.CTkButton(btn_frame, text="📋", width=35, height=28, fg_color="#333333", hover_color="#444444",
                      command=lambda p=entry.password: copy_to_clipboard(root, p)).pack(side="left", padx=2)

        # Remove button
        ctk.CTkButton(btn_frame, text="🗑", width=35, height=28, fg_color="#442222", hover_color="#772222",
                      command=lambda e=entry: remove_entry(scrollable_frame, password_list, e.service, e.username, keySafe)).pack(side="left", padx=2)