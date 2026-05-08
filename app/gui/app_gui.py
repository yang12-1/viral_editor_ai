import customtkinter as ctk

app = ctk.CTk()

app.geometry("1000x700")

app.title("VTuber Viral Editor AI")

label = ctk.CTkLabel(
    app,
    text="VTuber Viral Editing System",
    font=("Arial", 30)
)

label.pack(pady=30)

button = ctk.CTkButton(
    app,
    text="Start Editing"
)

button.pack(pady=20)

app.mainloop()

