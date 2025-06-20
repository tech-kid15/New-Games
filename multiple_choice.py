import tkinter as tk
from tkinter import messagebox

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiple Choice Quiz Game")
        self.root.geometry("600x400")

        # Define questions, options, and correct answers
        self.questions = [
            {"question": "What is the capital of France?", 
             "options": ["Berlin", "Madrid", "Paris", "Rome"], 
             "correct": "Paris"},

            {"question": "Which planet is known as the Red Planet?", 
             "options": ["Earth", "Mars", "Jupiter", "Saturn"], 
             "correct": "Mars"},

            {"question": "Who wrote 'Romeo and Juliet'?", 
             "options": ["Shakespeare", "Dickens", "Hemingway", "Austen"], 
             "correct": "Shakespeare"},

            {"question": "Which is the largest ocean?", 
             "options": ["Atlantic", "Indian", "Pacific", "Arctic"], 
             "correct": "Pacific"},

            {"question": "What is the largest mammal in the world?", 
             "options": ["Elephant", "Blue Whale", "Giraffe", "Polar Bear"], 
             "correct": "Blue Whale"},

            {"question": "What year did the first iPhone release?", 
             "options": ["2005", "2006", "2007", "2008"], 
             "correct": "2007"},

            {"question": "Which planet is closest to the Sun?", 
             "options": ["Venus", "Mercury", "Earth", "Mars"], 
             "correct": "Mercury"},

            {"question": "Which company created the video game Fortnite?", 
             "options": ["Ubisoft", "Valve", "Epic Games", "Blizzard"], 
             "correct": "Epic Games"},

            {"question": "Which language has the most native speakers worldwide?", 
             "options": ["English", "Spanish", "Hindi", "Mandarin Chinese"], 
             "correct": "Mandarin Chinese"}
        ]
        
        self.score = 0
        self.question_index = 0
        
        # Set up the question label
        self.question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=500, justify="center")
        self.question_label.pack(pady=20)
        
        # Set up option buttons
        self.option_buttons = []
        for i in range(4):  # Only 4 options per question
            button = tk.Button(root, text="", width=30, height=2, font=("Arial", 12),
                               command=lambda i=i: self.check_answer(i))
            button.pack(pady=5)
            self.option_buttons.append(button)
        
        self.load_question()
    
    def load_question(self):
        question_data = self.questions[self.question_index]
        self.question_label.config(text=question_data["question"])
        
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option)
    
    def check_answer(self, selected_index):
        selected_text = self.option_buttons[selected_index]["text"]
        correct_answer = self.questions[self.question_index]["correct"]
        
        if selected_text == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "Good job! That's the correct answer.")
        else:
            messagebox.showerror("Wrong!", f"Oops! The correct answer was: {correct_answer}")
        
        self.question_index += 1
        if self.question_index < len(self.questions):
            self.load_question()
        else:
            messagebox.showinfo("Game Over", f"Your score is {self.score} out of {len(self.questions)}.")
            self.root.quit()

# Create and run the game
root = tk.Tk()
game = QuizGame(root)
root.mainloop()
