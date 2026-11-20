# Cosmic Quiz

**Name:** Charls Ryan Garlito
**Section:** BSInfoTech SE 3A
**Topic:** Solar System
## How to Run
1. Install Python 3 (tkinter comes with it).
2. Open a terminal in the project folder.
3. Run: `python quiz.py`

## Features Completed
- 10 multiple-choice questions
- Random question order
- 15-second countdown timer
- Answer checking and time-out handling
- Score and percentage
- Answer review
- High score saved in a text file
- Restart button

### **How the Questions Are Stored and Shuffled**

The questions are stored in a list called `QUESTIONS`. Each question has four choices and one correct answer. When the quiz starts, the program shuffles the questions so they appear in a different order every time.

### **How the Timer Works**

The timer starts at 15 seconds. It goes down by 1 every second. If the time reaches 0, the answer is automatically marked wrong. If the player answers early, the timer stops.

### **How the Program Checks the Correct Answer**

The player chooses one answer from A, B, C, or D. The program checks if the chosen letter matches the correct answer. If they match, the player gets a point.

### **How the Score and High Score Work**

The score increases by 1 for every correct answer. At the end, the program calculates the percentage of correct answers. The highest score is saved in a file called `high_score.txt`, so it will still be there even after closing the program.

## Function Explanations
| Function | Purpose | Called when |
|----------|---------|-------------|
| `start_quiz()` | Resets the score and shuffles the questions | Launch or Restart is clicked |
| `show_question()` | Builds the question screen with the choices and buttons | A new question starts |
| `update_timer()` | Shows the time left and counts down every second | A question is displayed |
| `stop_timer()` | Cancels the timer | An answer is submitted |
| `submit_answer()` | Checks the answer and updates the score | Submit is clicked |
| `time_up()` | Marks the question wrong when time reaches 0 | The timer hits 0 |
| `save_high_score()` | Writes the score to the file if it is higher | The results screen is shown |
| `show_results()` | Shows the score, percentage, message, and review | After question 10 |

## Screenshots
![Start screen](screenshots/start.png)
![Question screen](screenshots/question.png)
![Answer feedback](screenshots/feedback.png)
![Results screen](screenshots/results.png)
![High score after reopening](screenshots/high_score.png)

## Challenges I Faced
The hardest part for me was that coding is confusing. At first, I didn't understand Python well. I solved it by watching tutorials on YouTube and TikTok, and by reading the code slowly and running the program to see what it does. One part I found difficult in this quiz was the timer, but after running the program and watching it count down, I understood how it works. Now I understand that coding is worth learning, but it needs patience.
