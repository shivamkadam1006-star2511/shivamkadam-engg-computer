from tkinter import *
from PIL import Image, ImageTk
import speech_to_text
import action


# =========================
# MAIN WINDOW
# =========================

root = Tk()
root.title("JARVIS AI ASSISTANT")
root.geometry("550x675")
root.resizable(False, False)
root.config(bg="#0f172a")


# =========================
# FUNCTIONS
# =========================

def ask():
    status_label.config(text="🎤 Listening...")
    root.update()

    user_val = speech_to_text.speech_to_text()

    if not user_val:
        text.insert(END, "Jarvis ---> Sorry, I could not hear you.\n\n")
        status_label.config(text="● Ready")
        return

    text.insert(END, "You ---> " + str(user_val) + "\n")

    status_label.config(text="🤖 Thinking...")
    root.update()

    bot_val = action.Action(user_val)

    if bot_val is not None:
        text.insert(END, "Jarvis ---> " + str(bot_val) + "\n\n")

    status_label.config(text="● Ready")

    if bot_val == "ok sir":
        root.destroy()


def send():

    user_val = entry_box.get().strip()

    if not user_val:
        text.insert(END, "Jarvis ---> Please type something first.\n\n")
        return

    text.insert(END, "You ---> " + user_val + "\n")

    status_label.config(text="🤖 Thinking...")
    root.update()

    bot_val = action.Action(user_val)

    if bot_val is not None:
        text.insert(END, "Jarvis ---> " + str(bot_val) + "\n\n")

    entry_box.delete(0, END)

    status_label.config(text="● Ready")

    if bot_val == "ok sir":
        root.destroy()


def del_text():
    text.delete("1.0", END)
    entry_box.delete(0, END)
    status_label.config(text="● Ready")


def enter_key(event):
    send()


# =========================
# HEADER
# =========================

header = Frame(
    root,
    bg="#1e293b",
    height=70
)

header.pack(fill=X)


title = Label(
    header,
    text="⚡ JARVIS AI",
    font=("Segoe UI", 22, "bold"),
    fg="#38bdf8",
    bg="#1e293b"
)

title.pack(pady=(8, 0))


subtitle = Label(
    header,
    text="Your Intelligent Virtual Assistant",
    font=("Segoe UI", 9),
    fg="#94a3b8",
    bg="#1e293b"
)

subtitle.pack()


# =========================
# STATUS
# =========================

status_label = Label(
    root,
    text="● Ready",
    font=("Segoe UI", 10, "bold"),
    fg="#22c55e",
    bg="#0f172a"
)

status_label.pack(pady=5)


# =========================
# ASSISTANT IMAGE
# =========================

image_frame = Frame(
    root,
    bg="#1e293b",
    highlightbackground="#38bdf8",
    highlightthickness=2,
    width=250,
    height=245
)

image_frame.pack(pady=3)

image_frame.pack_propagate(False)


try:

    assistant_image = Image.open("Image/assistant.png")

    assistant_image = assistant_image.resize(
        (210, 210)
    )

    assistant_photo = ImageTk.PhotoImage(
        assistant_image
    )

    image_label = Label(
        image_frame,
        image=assistant_photo,
        bg="#1e293b"
    )

    image_label.pack(pady=15)

except Exception as e:

    image_label = Label(
        image_frame,
        text="JARVIS",
        font=("Segoe UI", 30, "bold"),
        fg="#38bdf8",
        bg="#1e293b"
    )

    image_label.pack(pady=80)


# =========================
# CHAT BOX
# =========================

chat_frame = Frame(
    root,
    bg="#1e293b"
)

chat_frame.pack(
    padx=45,
    pady=5
)


text = Text(
    chat_frame,
    width=50,
    height=6,
    font=("Segoe UI", 9),
    bg="#020617",
    fg="#e2e8f0",
    insertbackground="white",
    selectbackground="#334155",
    relief=FLAT,
    wrap=WORD,
    padx=8,
    pady=8
)

text.pack(side=LEFT)


scrollbar = Scrollbar(
    chat_frame,
    command=text.yview
)

scrollbar.pack(
    side=RIGHT,
    fill=Y
)

text.config(
    yscrollcommand=scrollbar.set
)


# =========================
# WELCOME MESSAGE
# =========================

text.insert(
    END,
    "Jarvis ---> Hello! I am Jarvis.\n"
    "Jarvis ---> How can I help you?\n\n"
)


# =========================
# INPUT BOX
# =========================

entry_box = Entry(
    root,
    font=("Segoe UI", 11),
    bg="#1e293b",
    fg="white",
    insertbackground="white",
    relief=FLAT
)

entry_box.pack(
    padx=45,
    pady=5,
    fill=X,
    ipady=7
)

entry_box.bind(
    "<Return>",
    enter_key
)


# =========================
# BUTTON FRAME
# =========================

button_frame = Frame(
    root,
    bg="#0f172a"
)

button_frame.pack(
    pady=10
)


# =========================
# ASK
# =========================

button1 = Button(
    button_frame,
    text="🎤 ASK",
    font=("Segoe UI", 9, "bold"),
    fg="white",
    bg="#2563eb",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief=FLAT,
    cursor="hand2",
    command=ask,
    padx=18,
    pady=10
)

button1.grid(
    row=0,
    column=0,
    padx=5
)


# =========================
# DELETE
# =========================

button3 = Button(
    button_frame,
    text="🗑 DELETE",
    font=("Segoe UI", 9, "bold"),
    fg="white",
    bg="#dc2626",
    activebackground="#b91c1c",
    activeforeground="white",
    relief=FLAT,
    cursor="hand2",
    command=del_text,
    padx=15,
    pady=10
)

button3.grid(
    row=0,
    column=1,
    padx=5
)


# =========================
# SEND
# =========================

button2 = Button(
    button_frame,
    text="➤ SEND",
    font=("Segoe UI", 9, "bold"),
    fg="white",
    bg="#16a34a",
    activebackground="#15803d",
    activeforeground="white",
    relief=FLAT,
    cursor="hand2",
    command=send,
    padx=18,
    pady=10
)

button2.grid(
    row=0,
    column=2,
    padx=5
)


# =========================
# FOOTER
# =========================

footer = Label(
    root,
    text="JARVIS AI • Voice + Text Assistant",
    font=("Segoe UI", 8),
    fg="#64748b",
    bg="#0f172a"
)

footer.pack()


# =========================
# START
# =========================

root.mainloop()