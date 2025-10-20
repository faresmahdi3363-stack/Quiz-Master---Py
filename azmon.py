import tkinter as tk
from tkinter import messagebox
import time
import os
import csv

SUBJECTS = ["Math", "Physics", "Chemistry"]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Checker")
        self.root.geometry("600x500")
        
        self.start_time = 0
        self.answers = []
        self.correct_answers = []
        self.current_question = 0
        self.question_times = []
        
        self.create_start_screen()
    
    def create_start_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Select Subject:", font=("Arial", 14)).pack(pady=10)
        self.subject_var = tk.StringVar(value=SUBJECTS[0])
        for subj in SUBJECTS:
            tk.Radiobutton(self.root, text=subj, variable=self.subject_var, value=subj).pack(anchor='w', padx=50)
        
        tk.Label(self.root, text="Number of Questions:", font=("Arial", 14)).pack(pady=10)
        self.num_entry = tk.Entry(self.root)
        self.num_entry.pack()
        
        tk.Button(self.root, text="Start Quiz", command=self.start_quiz).pack(pady=20)
    
    def start_quiz(self):
        num = self.num_entry.get()
        if not num.isdigit() or int(num) <= 0:
            messagebox.showerror("Error", "Enter a valid positive number of questions.")
            return
        self.num_questions = int(num)
        self.subject = self.subject_var.get()
        self.answers = []
        self.question_times = []
        self.current_question = 0
        self.start_time = time.time()
        self.show_question_screen()
    
    def show_question_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Question {self.current_question + 1}", font=("Arial", 16)).pack(pady=20)
        self.question_start_time = time.time()
        for i in range(1, 5):
            tk.Button(self.root, text=str(i), width=10, command=lambda i=i: self.save_answer(i)).pack(pady=5)
        tk.Button(self.root, text="Skip", width=10, fg="red", command=lambda: self.save_answer(None)).pack(pady=10)
    
    def save_answer(self, option):
        self.answers.append(option)
        time_taken = int(time.time() - self.question_start_time)
        self.question_times.append(time_taken)
        self.current_question += 1
        if self.current_question < self.num_questions:
            self.show_question_screen()
        else:
            self.end_answering()
    
    def end_answering(self):
        self.answer_time = time.time() - self.start_time
        self.current_question = 0
        self.correct_answers = []
        self.show_correct_screen()
    
    def show_correct_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Correct Answers", font=("Arial", 14)).pack(pady=10)
        self.correct_entries = []
        for i in range(self.num_questions):
            frame = tk.Frame(self.root)
            tk.Label(frame, text=f"Q{i+1}:", width=5).pack(side='left')
            entry = tk.Entry(frame, width=5)
            entry.pack(side='left')
            frame.pack(pady=2)
            self.correct_entries.append(entry)
        tk.Button(self.root, text="Submit Correct Answers", command=self.calculate_score).pack(pady=20)
    
    def calculate_score(self):
        for entry in self.correct_entries:
            val = entry.get()
            if not val.isdigit() or int(val) not in [1,2,3,4]:
                messagebox.showerror("Error", "All correct answers must be 1–4 numbers.")
                return
            self.correct_answers.append(int(val))
        
        self.show_result()
        self.save_csv()
    
    def show_result(self):
        wrong_count = 0
        correct_count = 0
        answered_questions = 0
        details = []
        
        for ua, ca in zip(self.answers, self.correct_answers):
            if ua is None:
                details.append("⏭")
                continue
            answered_questions += 1
            if ua == ca:
                correct_count += 1
                details.append("✅")
            else:
                wrong_count += 1
                details.append("❌")
        
        if answered_questions == 0:
            percent = 0
        else:
            raw_score = (3 * correct_count) - wrong_count
            if raw_score < 0:
                raw_score = 0
            percent = (raw_score / (3 * answered_questions)) * 100
        
        total_time = time.time() - self.start_time
        
        self.clear_screen()
        tk.Label(self.root, text=f"Quiz Result - {self.subject}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Answered Questions: {answered_questions}/{self.num_questions}").pack()
        tk.Label(self.root, text=f"Correct: {correct_count} | Wrong: {wrong_count}").pack()
        tk.Label(self.root, text=f"Score: {percent:.2f}%").pack()
        tk.Label(self.root, text=f"Answering time: {int(self.answer_time)} sec").pack()
        tk.Label(self.root, text=f"Total time: {int(total_time)} sec").pack(pady=10)
        
        tk.Label(self.root, text="Details (✅=Correct, ❌=Wrong, ⏭=Skipped):").pack()
        detail_text = " ".join(details)
        tk.Label(self.root, text=detail_text, font=("Arial", 12)).pack(pady=5)
        
        tk.Button(self.root, text="Restart", command=self.create_start_screen).pack(pady=15)
    
    def save_csv(self):
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        filename = os.path.join(desktop, "quiz_results.csv")
        
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Question", "Your Answer", "Correct Answer", "Status", "Time Taken (s)", "Total Time (s)"])
            
            for idx, (ua, ca, qt) in enumerate(zip(self.answers, self.correct_answers, self.question_times), start=1):
                if ua is None:
                 status = "Skipped"
                 ua_str = ""
                elif ua == ca:
                 status = "Correct"
                 ua_str = str(ua)
                else:
                 status = "Wrong"
                 ua_str = str(ua)

                total_time = int(time.time() - self.start_time)
                writer.writerow([idx, ua_str, ca, status, qt, total_time])
        
        messagebox.showinfo("Saved", f"Results saved to Desktop as 'quiz_results.csv'")
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
