import tkinter as tk
from PIL import Image, ImageTk
import pickle

# Load AI model
with open("stream_selection_model.pkl", "rb") as f:
    model, feature_names = pickle.load(f)

subjects = ["Maths", "Science", "English", "Sinhala", "ICT", "History", "Commerce", "Buddhism"]
interest_options = ["Science", "Maths", "Commerce", "Arts", "Technology"]

root = tk.Tk()
root.title("A/L Stream Advisor Chatbot")
root.geometry("1000x700")
root.state('zoomed')

# 🌄 Background (University Image)
bg_img = Image.open("background.png").resize((1920,1080))
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# 🎨 Gradient-like Chat Frame
chat_frame = tk.Frame(root, bg="#f0f8ff", bd=3, relief="ridge")
chat_frame.place(relwidth=0.65, relheight=0.75, relx=0.18, rely=0.05)

canvas = tk.Canvas(chat_frame, bg="#f0f8ff", highlightthickness=0)
scrollbar = tk.Scrollbar(chat_frame, command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

state = {"step": 0, "inputs": [], "interest": None}

# 🤖 Bot Avatar
bot_img = Image.open("bot.png").resize((40, 40))
bot_photo = ImageTk.PhotoImage(bot_img)

typing_label = tk.Label(root, text="", font=("Helvetica", 11, "italic"), bg="#ffffff", fg="#444")
typing_label.place(relx=0.18, rely=0.82)

# 💬 Colorful Chat Bubbles
def add_message(msg, sender="bot"):
    typing_label.config(text="")
    bubble_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")

    if sender == "user":
        bubble = tk.Label(
            bubble_frame, text=msg, bg="#4CAF50", fg="white",
            font=("Helvetica", 12, "bold"), wraplength=400,
            justify="left", padx=12, pady=8, bd=0, relief="flat"
        )
        bubble.pack(anchor="e", pady=5, padx=10)
        bubble.configure(highlightbackground="#388e3c", highlightthickness=1)
    else:
        msg_container = tk.Frame(bubble_frame, bg="#f0f8ff")
        avatar_label = tk.Label(msg_container, image=bot_photo, bg="#f0f8ff")
        avatar_label.pack(side="left", padx=5)
        bubble = tk.Label(
            msg_container, text=msg, bg="#ff9800", fg="white",
            font=("Helvetica", 12), wraplength=350,
            justify="left", padx=12, pady=8, bd=0, relief="flat"
        )
        bubble.pack(side="left", pady=5)
        bubble.configure(highlightbackground="#e65100", highlightthickness=1)
        msg_container.pack(anchor="w")

    bubble_frame.pack(fill=tk.BOTH, anchor="w")
    root.update_idletasks()
    canvas.yview_moveto(1.0)

def bot_typing(msg, delay=1000):
    typing_label.config(text="Bot is typing...")
    root.after(delay, lambda: add_message(msg))

# 🎛 Colorful Buttons
button_frame = tk.Frame(root, bg="#ffffff")
button_frame.place(relx=0.18, rely=0.87, relwidth=0.65, height=70)

def show_rating_buttons():
    for w in button_frame.winfo_children():
        w.destroy()
    colors = ["#e91e63","#9c27b0","#3f51b5","#009688","#ff5722"]
    for i in range(1, 6):
        tk.Button(
            button_frame, text=str(i), width=5, bg=colors[i-1], fg="white",
            font=("Helvetica", 12, "bold"), relief="raised", bd=2,
            activebackground="#333", command=lambda val=i: rating_selected(val)
        ).pack(side=tk.LEFT, padx=8, pady=8)

def rating_selected(val):
    add_message(str(val), sender="user")
    state["inputs"].append(val*20)
    state["step"] += 1
    next_step()

def show_interest_buttons():
    for w in button_frame.winfo_children():
        w.destroy()
    colors = ["#f44336","#2196f3","#ff9800","#4caf50","#9c27b0"]
    for idx, opt in enumerate(interest_options):
        tk.Button(
            button_frame, text=opt, width=12, bg=colors[idx], fg="white",
            font=("Helvetica", 11, "bold"), relief="groove", bd=2,
            activebackground="#222",
            command=lambda choice=opt: interest_selected(choice)
        ).pack(side=tk.LEFT, padx=5, pady=5)

def interest_selected(choice):
    add_message(choice, sender="user")
    state["interest"] = choice
    make_prediction()

def next_step():
    if state["step"] < len(subjects):
        bot_typing(f"How much do you like {subjects[state['step']]}? (1-5)")
        show_rating_buttons()
    else:
        bot_typing("What is your overall main interest?")
        show_interest_buttons()

def make_prediction():
    input_dict = {f: 0 for f in feature_names}
    for i, sub in enumerate(subjects):
        input_dict[sub] = state["inputs"][i]
    interest_col = "Interest_" + state["interest"]
    if interest_col in input_dict:
        input_dict[interest_col] = 1
    input_data = [input_dict[f] for f in feature_names]
    prediction = model.predict([input_data])[0]
    bot_typing(f"🎓 Based on your answers, I recommend: {prediction} Stream ✨")
    bot_typing("To check another student, click rating for Maths.", delay=1500)
    state["step"] = 0
    state["inputs"] = []
    state["interest"] = None
    show_rating_buttons()

# 🚀 Start Chat
bot_typing("🌟 Hi! I’m your A/L Stream Advisor Chatbot 🤖", delay=500)
bot_typing(f"📘 How much do you like {subjects[0]}? (1-5)", delay=1200)
show_rating_buttons()

root.mainloop()
