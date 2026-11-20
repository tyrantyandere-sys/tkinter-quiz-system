import tkinter as tk
from tkinter import messagebox
import random
import os

QUESTIONS = [
    {"question": "Which is the largest planet in our Solar System?",
     "choices": ["A. Saturn", "B. Neptune", "C. Jupiter", "D. Earth"],
     "answer": "C"},
    {"question": "Which planet is closest to the Sun?",
     "choices": ["A. Mercury", "B. Venus", "C. Mars", "D. Earth"],
     "answer": "A"},
    {"question": "Which planet is nicknamed the Red Planet?",
     "choices": ["A. Jupiter", "B. Mars", "C. Venus", "D. Uranus"],
     "answer": "B"},
    {"question": "What is the name of the galaxy that contains our Solar System?",
     "choices": ["A. Andromeda", "B. Triangulum", "C. Whirlpool", "D. Milky Way"],
     "answer": "D"},
    {"question": "What kind of object is the Sun?",
     "choices": ["A. A planet", "B. A star", "C. A comet", "D. A moon"],
     "answer": "B"},
    {"question": "Which planet is best known for its bright rings?",
     "choices": ["A. Saturn", "B. Mars", "C. Mercury", "D. Earth"],
     "answer": "A"},
    {"question": "About how long does sunlight take to reach Earth?",
     "choices": ["A. 8 seconds", "B. 8 hours", "C. 8 minutes", "D. 8 days"],
     "answer": "C"},
    {"question": "Who was the first person to walk on the Moon?",
     "choices": ["A. Buzz Aldrin", "B. Yuri Gagarin", "C. Neil Armstrong", "D. John Glenn"],
     "answer": "C"},
    {"question": "Which object was reclassified as a dwarf planet in 2006?",
     "choices": ["A. Pluto", "B. Ceres", "C. Titan", "D. Europa"],
     "answer": "A"},
    {"question": "Which planet spins on its side, tilted about 98 degrees?",
     "choices": ["A. Neptune", "B. Venus", "C. Jupiter", "D. Uranus"],
     "answer": "D"},
]

TIME_LIMIT = 15
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)

BG = "#0B1026"
PANEL = "#151C3D"
PANEL2 = "#232C5C"
SELECTED = "#2A2F63"
ACCENT = "#FFB703"
ACCENT_HOVER = "#FFC93C"
TEXT = "#EAF0FF"
MUTED = "#8FA0CC"
GOOD = "#4ADE80"
BAD = "#FF5C7A"
DISABLED_BG = "#1B2347"
FONT = "Helvetica"

WIN_W, WIN_H = 760, 740
CONTENT_W = WIN_W - 60

root = tk.Tk()
root.title("Cosmic Quiz")
root.geometry(f"{WIN_W}x{WIN_H}")
root.configure(bg=BG)
root.resizable(False, False)

quiz_questions = []
current_question = 0
score = 0
time_left = TIME_LIMIT
wrong_answers = []
timer_job = None
answered = False
selected_answer = tk.StringVar()

timer_label = None
timer_bar = None
score_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []
choice_cards = []

main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=30, pady=20)


class FlatButton(tk.Label):
    def __init__(self, parent, text, command, secondary=False, width=16):
        self.base_bg = PANEL2 if secondary else ACCENT
        self.base_fg = TEXT if secondary else BG
        self.hover_bg = "#2F3A75" if secondary else ACCENT_HOVER
        super().__init__(parent, text=text, font=(FONT, 11, "bold"),
                         bg=self.base_bg, fg=self.base_fg, width=width,
                         pady=10, cursor="hand2")
        self.command = command
        self.enabled = True
        self.bind("<Enter>", lambda e: self.enabled and self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.enabled and self.config(bg=self.base_bg))
        self.bind("<Button-1>", self._click)

    def _click(self, event):
        if self.enabled:
            self.command()

    def set_enabled(self, enabled):
        self.enabled = enabled
        if enabled:
            self.config(bg=self.base_bg, fg=self.base_fg, cursor="hand2")
        else:
            self.config(bg=DISABLED_BG, fg=MUTED, cursor="arrow")


def get_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except ValueError:
            return 0
    return 0


def save_high_score(new_score):
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(new_score))
        return True
    return False


def clear_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()


def get_choice_text(question, letter):
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"


def draw_stars(canvas, width, height, count=60):
    rng = random.Random(7)
    for _ in range(count):
        x, y = rng.randint(0, width), rng.randint(0, height)
        size = rng.choice([1, 1, 2, 3])
        color = rng.choice([TEXT, MUTED, ACCENT])
        canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")


def stat_card(parent, big_text, small_text):
    card = tk.Frame(parent, bg=PANEL, padx=26, pady=16)
    tk.Label(card, text=big_text, font=(FONT, 22, "bold"),
             bg=PANEL, fg=ACCENT).pack()
    tk.Label(card, text=small_text, font=(FONT, 10),
             bg=PANEL, fg=MUTED).pack()
    return card


def show_start_screen():
    clear_screen()

    banner = tk.Canvas(main_frame, width=CONTENT_W, height=190,
                       bg=BG, highlightthickness=0)
    banner.pack(pady=(30, 0))
    draw_stars(banner, CONTENT_W, 190, 80)
    banner.create_text(CONTENT_W // 2, 85, text="COSMIC QUIZ",
                       font=(FONT, 40, "bold"), fill=ACCENT)
    banner.create_text(CONTENT_W // 2, 140,
                       text="How well do you know our Solar System?",
                       font=(FONT, 13), fill=MUTED)

    stats = tk.Frame(main_frame, bg=BG)
    stats.pack(pady=35)
    stat_card(stats, str(len(QUESTIONS)), "questions").pack(side="left", padx=8)
    stat_card(stats, f"{TIME_LIMIT}s", "per question").pack(side="left", padx=8)
    stat_card(stats, f"{get_high_score()}/{len(QUESTIONS)}",
              "best score").pack(side="left", padx=8)

    FlatButton(main_frame, "LAUNCH QUIZ  ➜", start_quiz, width=24).pack(pady=10)
    tk.Label(main_frame, text="Pick an answer, then press Submit before time runs out.",
             font=(FONT, 10), bg=BG, fg=MUTED).pack(pady=(14, 0))


def start_quiz():
    global quiz_questions, current_question, score, wrong_answers
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()


def pick_choice(letter):
    if not answered:
        selected_answer.set(letter)


def refresh_choice_styles(*args):
    if answered:
        return
    chosen = selected_answer.get()
    for letter, card, button in choice_cards:
        selected = (letter == chosen)
        bg = SELECTED if selected else PANEL
        border = ACCENT if selected else PANEL
        try:
            card.config(bg=bg, highlightbackground=border)
            button.config(bg=bg, activebackground=bg)
        except tk.TclError:
            pass


selected_answer.trace_add("write", refresh_choice_styles)


def reveal_answer(correct_letter, chosen_letter):
    for letter, card, button in choice_cards:
        if letter == correct_letter:
            color = GOOD
        elif letter == chosen_letter:
            color = BAD
        else:
            continue
        card.config(highlightbackground=color, highlightcolor=color)
        button.config(fg=color)


def show_question():
    global time_left, answered, timer_label, timer_bar, score_label
    global feedback_label, submit_button, next_button
    global choice_buttons, choice_cards

    clear_screen()
    choice_buttons = []
    choice_cards = []
    answered = False
    selected_answer.set("")
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]
    total = len(quiz_questions)

    top = tk.Frame(main_frame, bg=BG)
    top.pack(fill="x")
    tk.Label(top, text=f"Question {current_question + 1} of {total}",
             font=(FONT, 14, "bold"), bg=BG, fg=TEXT).pack(side="left")
    timer_label = tk.Label(top, text="", font=(FONT, 14, "bold"),
                           bg=BG, fg=ACCENT)
    timer_label.pack(side="right")
    score_label = tk.Label(top, text=f"★ {score}", font=(FONT, 11, "bold"),
                           bg=PANEL, fg=ACCENT, padx=12, pady=3)
    score_label.pack(side="right", padx=18)

    strip = tk.Canvas(main_frame, width=CONTENT_W, height=8,
                      bg=BG, highlightthickness=0)
    strip.pack(pady=(12, 6), anchor="w")
    seg_w = CONTENT_W / total
    for i in range(total):
        color = ACCENT if i <= current_question else PANEL2
        strip.create_rectangle(i * seg_w + 2, 0, (i + 1) * seg_w - 2, 8,
                               fill=color, outline="")

    timer_bar = tk.Canvas(main_frame, width=CONTENT_W, height=10,
                          bg=PANEL, highlightthickness=0)
    timer_bar.pack(anchor="w")

    card = tk.Frame(main_frame, bg=PANEL)
    card.pack(fill="x", pady=20)
    tk.Frame(card, bg=ACCENT, width=6).pack(side="left", fill="y")
    tk.Label(card, text=question["question"], font=(FONT, 16, "bold"),
             wraplength=CONTENT_W - 70, justify="left", bg=PANEL, fg=TEXT,
             padx=20, pady=22).pack(side="left", anchor="w")

    for choice in question["choices"]:
        letter = choice[0]
        choice_card = tk.Frame(main_frame, bg=PANEL, highlightthickness=2,
                               highlightbackground=PANEL, highlightcolor=PANEL,
                               cursor="hand2")
        choice_card.pack(fill="x", pady=4)
        button = tk.Radiobutton(choice_card, text=choice,
                                variable=selected_answer, value=letter,
                                font=(FONT, 13), bg=PANEL, fg=TEXT,
                                selectcolor=PANEL2, activebackground=PANEL,
                                activeforeground=ACCENT,
                                disabledforeground=MUTED, anchor="w",
                                bd=0, highlightthickness=0, padx=14, pady=8)
        button.pack(fill="x")
        choice_card.bind("<Button-1>", lambda e, l=letter: pick_choice(l))
        choice_buttons.append(button)
        choice_cards.append((letter, choice_card, button))

    feedback_label = tk.Label(main_frame, text="", font=(FONT, 12, "bold"),
                              bg=BG, fg=TEXT, wraplength=CONTENT_W)
    feedback_label.pack(pady=12)

    row = tk.Frame(main_frame, bg=BG)
    row.pack()
    submit_button = FlatButton(row, "SUBMIT", submit_answer)
    submit_button.pack(side="left", padx=8)

    last = current_question == total - 1
    next_button = FlatButton(row, "SEE RESULTS" if last else "NEXT  ➜",
                             next_question)
    next_button.set_enabled(False)
    next_button.pack(side="left", padx=8)

    update_timer()


def draw_timer_bar():
    timer_bar.delete("all")
    fraction = time_left / TIME_LIMIT
    color = BAD if time_left <= 5 else ACCENT
    timer_bar.create_rectangle(0, 0, CONTENT_W * fraction, 10,
                               fill=color, outline="")


def update_timer():
    global time_left, timer_job
    if answered:
        return
    timer_label.config(text=f"⏱ {time_left}s",
                       fg=BAD if time_left <= 5 else ACCENT)
    draw_timer_bar()
    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)


def stop_timer():
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None


def lock_choices():
    for button in choice_buttons:
        button.config(state="disabled")


def submit_answer():
    global score, answered
    if answered:
        return
    choice = selected_answer.get()
    if choice == "":
        messagebox.showwarning("No answer", "Please select an answer first.")
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.set_enabled(False)

    question = quiz_questions[current_question]
    correct_text = get_choice_text(question, question["answer"])
    if choice == question["answer"]:
        score += 1
        score_label.config(text=f"★ {score}")
        feedback_label.config(text="✔  Correct!", fg=GOOD)
    else:
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": correct_text,
        })
        feedback_label.config(text=f"✘  Wrong!  Correct answer: {correct_text}",
                              fg=BAD)
    reveal_answer(question["answer"], choice)
    next_button.set_enabled(True)


def time_up():
    global answered
    if answered:
        return
    answered = True
    lock_choices()
    submit_button.set_enabled(False)

    question = quiz_questions[current_question]
    correct_text = get_choice_text(question, question["answer"])
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": correct_text,
    })
    feedback_label.config(text=f"⌛  Time is up!  Correct answer: {correct_text}",
                          fg=BAD)
    reveal_answer(question["answer"], None)
    next_button.set_enabled(True)


def next_question():
    global current_question
    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()


def draw_score_ring(parent, percentage):
    size = 170
    canvas = tk.Canvas(parent, width=size, height=size, bg=BG,
                       highlightthickness=0)
    pad = 14
    canvas.create_oval(pad, pad, size - pad, size - pad,
                       outline=PANEL2, width=14)
    extent = -359.9 if percentage >= 100 else -3.6 * percentage
    color = GOOD if percentage >= 70 else (ACCENT if percentage >= 50 else BAD)
    if percentage > 0:
        canvas.create_arc(pad, pad, size - pad, size - pad, start=90,
                          extent=extent, style="arc", outline=color, width=14)
    canvas.create_text(size // 2, size // 2 - 8, text=f"{percentage:.0f}%",
                       font=(FONT, 28, "bold"), fill=TEXT)
    canvas.create_text(size // 2, size // 2 + 24, text="score",
                       font=(FONT, 10), fill=MUTED)
    return canvas


def show_results():
    clear_screen()
    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)

    if percentage >= 90:
        message = "Stellar! You're a true astronomer."
    elif percentage >= 70:
        message = "Great orbit! Nearly there."
    elif percentage >= 50:
        message = "Decent flight. Keep exploring!"
    else:
        message = "Back to mission control - try again."

    tk.Label(main_frame, text="MISSION COMPLETE", font=(FONT, 24, "bold"),
             bg=BG, fg=ACCENT).pack(pady=(0, 10))

    summary = tk.Frame(main_frame, bg=BG)
    summary.pack()
    draw_score_ring(summary, percentage).pack(side="left", padx=(0, 30))

    info = tk.Frame(summary, bg=BG)
    info.pack(side="left")
    tk.Label(info, text=f"{score} / {total} correct",
             font=(FONT, 20, "bold"), bg=BG, fg=TEXT).pack(anchor="w")
    tk.Label(info, text=message, font=(FONT, 12), bg=BG,
             fg=MUTED).pack(anchor="w", pady=4)
    record_text = ("★ New high score! ★" if new_record
                   else f"High score: {get_high_score()} / {total}")
    tk.Label(info, text=record_text, font=(FONT, 12, "bold"),
             bg=PANEL, fg=GOOD, padx=12, pady=5).pack(anchor="w", pady=6)

    tk.Label(main_frame, text="ANSWER REVIEW  (incorrect answers)",
             font=(FONT, 11, "bold"), bg=BG, fg=TEXT).pack(pady=(16, 4), anchor="w")

    review_frame = tk.Frame(main_frame, bg=BG)
    review_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")
    review_box = tk.Text(review_frame, height=9, wrap="word",
                         font=(FONT, 11), bg=PANEL, fg=TEXT, bd=0,
                         padx=14, pady=10, spacing3=2,
                         yscrollcommand=scrollbar.set)
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)

    review_box.tag_config("q", font=(FONT, 11, "bold"), foreground=TEXT)
    review_box.tag_config("yours", foreground=BAD)
    review_box.tag_config("correct", foreground=GOOD)

    if not wrong_answers:
        review_box.insert("end", "Perfect! You answered every question correctly.",
                          "correct")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n", "q")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n", "yours")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n",
                              "correct")
    review_box.config(state="disabled")

    row = tk.Frame(main_frame, bg=BG)
    row.pack(pady=16)
    FlatButton(row, "RESTART", restart_quiz).pack(side="left", padx=8)
    FlatButton(row, "EXIT", on_close, secondary=True).pack(side="left", padx=8)


def restart_quiz():
    start_quiz()


def on_close():
    stop_timer()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()