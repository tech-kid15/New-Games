import random

# Available choices
choices = ['rock', 'paper', 'scissors']
your_score=0

computer_score=0

def check_wins(user_choice, computer_choice, your_score, computer_score):
    # Check if the computer wins
    if (computer_choice == "rock" and user_choice == "scissors") or \
       (computer_choice == "paper" and user_choice == "rock") or \
       (computer_choice == "scissors" and user_choice == "paper"):
        print("You lose")
        computer_score += 1
    # Check if you win
    elif (computer_choice == "scissors" and user_choice == "rock") or \
         (computer_choice == "rock" and user_choice == "paper") or \
         (computer_choice == "paper" and user_choice == "scissors"):
        print("You win")
        your_score += 1
    else:
         print("It is a tie")

    return your_score, computer_score  # Return updated scores


    

# Main game loop
while True:
    # Get user input
    user_choice = input("Enter rock, paper, or scissors (or quit to stop): ").lower()
    
    if user_choice == 'quit':
        print("Thanks for playing!")
        break

    if user_choice not in choices:
        print("Invalid choice. Try again.")
        continue

    # Computer makes a random choice
    computer_choice = random.choice(choices)
    print(f"Computer chose: {computer_choice}")

    
    your_score, computer_score = check_wins(user_choice, computer_choice, your_score, computer_score)

    print(f"You:{your_score}")
    print(f"Computer:{computer_score}")

    if computer_score==3:
        print("Computer Beat You! You goofy!")
        break
        
    elif your_score ==3:
        print("You beat the computer👍")
        break



