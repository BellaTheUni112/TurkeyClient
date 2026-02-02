import customtkinter as ctk
import pymem
APP_SIZE = "420x220"
FONT = ("Segoe UI",13)
pm = pymem.Pymem("GTAIV.exe")
module_base = pymem.process.module_from_name(
    pm.process_handle, "GTAIV.exe"
).lpBaseOfDll
def Godmode(enable: bool):
    address = module_base + 0x6296FF 
    if enable:
        pm.write_bytes(address, b"\x90" * 8, 8)
        return "Enabled! You should no longer take damage.", "lightgreen"
    else:
        original_bytes = b"\xF3\x0F\x11\x89\x14\x02\x00\x00"
        pm.write_bytes(address,original_bytes,len(original_bytes))
        return "Disabled! You should now take damage.", "red"
def Money(new_money: int):
    pm.write_int(0x08B46F04,new_money)
    return f"Money set to {new_money}!", "lightgreen"
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("Cheat Menu for GTAIV by Turkey")
app.geometry(APP_SIZE)
frame = ctk.CTkFrame(app)
frame.pack(pady=20,padx=20, fill="both",expand=True)
def toggle_health():
    msg, color = Godmode(checkbox.get())
    status.set(msg)
    status_label.configure(text_color=color) 
checkbox = ctk.CTkCheckBox(frame,text="Godmode", font=FONT,command=toggle_health,onvalue=True,offvalue=False)
checkbox.pack(anchor="w",pady=10)
ctk.CTkLabel(frame,text="Money", font=FONT).pack(anchor="w", pady=(10,0))
input_frame = ctk.CTkFrame(frame,fg_color="transparent")
input_frame.pack(fill="x",pady=8)
entry = ctk.CTkEntry(input_frame,placeholder_text="Enter amount")
entry.pack(side="left",fill="x",expand=True,padx=(0,8))
def confirm_money():
    try:
        value = int(entry.get() or 0)
        msg, color = Money(value)
        status.set(msg)
        status_label.configure(text_color=color)
    except ValueError:
        status.set("Invalid number!")
        status_label.configure(text_color="yellow")
ctk.CTkButton(input_frame,text="Confirm", font=FONT,command=confirm_money).pack(side="right")
status = ctk.StringVar(value="Ready")
status_label = ctk.CTkLabel(frame,textvariable=status, font=FONT,text_color="lightgreen")
status_label.pack(anchor="w", pady=(15,0))
app.mainloop()