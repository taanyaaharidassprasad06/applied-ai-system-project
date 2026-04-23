# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🧩 Overview
This project involved debugging and a "Number Guessing Game" that was built using Streamlit. The app was full of broken features that made the game unplayable and my role was manual testing, identifying bugs, and using AI tools such as Claude Code and ChatGPT to implement fixes and tests. This project taught me how to prompt AI effectively and verify its suggestions line by line.


## 🚨 The Situation
The AI-generated app had multiple issues:
- You can't win
- Hints were misleading
- Secret number seemed to change randomly

The goal: Guess a secret number within a limited number of attempts.
The app had many buggy features that made this impossible.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🔎 My Mission

1. **Manual Testing**: Play the game to identify broken features.
2. **Bug Investigation**: Tracked down state issues, scoring errors, inconsistent hints, and more.
3. **AI-assisted fixes**: Used Claude Code to implement all bug fixes and generate pytests.
4. **Code Comprehension**: Read every line of the original code to verify AI suggestions. Consulted ChatGPT for further code explanations when stuck.
5. **Prompting Strategy**: Learned to write precise prompts to get accurate AI suggestions.
6. **Verification**: Tested all fixes manually and with automated tests.

## 🐞 Key Bugs I Found
1. Hints were backwards
2. New game button did not create a new game to start over (did not do anything)
3. Normal level had a higher range than Hard level which meant Normal was more difficult than Hard
4. Easy mode range is 1-20 but the secret number was 44 which was out of range
5. Message at top always says "Guess a number between 1 and 100" regardless of level chosen
6. Game ended even with 1 attempt remaining
7. First guess is not counted as attempt 1
8. Attempts only count every other attempt / secret number keeps changing
9. Guessing a number that is "Too High" every other time rewards points instead of deducting
10. "Out of attempts" message not showing after fixing attempts 
11. Final score message not showing when won after fixing attempts
12. Attempts incremented even if string was entered

## 🪄 Fixes Implemented
1. Swapped hint messages
2. Initialized all states back to empty or 0
3. Changed the range
4. Fixed with range change
5. Used variables to reflect bounds rather than hardcoding
6. Rerun app after every guess
7. Initialized attempt to 0
8. Always took secret number as integer instead a string like it did on every even attempt previously
9. Deducted points instead of adding
10. Stored message in session state instead of displaying directly so it persists across reruns
11. Stored message in session state instead of displaying directly so it persists across reruns
12. Made sure to only increment if integer was entered using condition


## 💡 What I Learned
- AI can accelerate debugging and development but careful review is critical.
- Writing specific, concise prompts improve AI-generated code suggestions.
- Manual testing is essential even when AI writes fixes.

## 📸 Demo

- ![App Screenshot](screenshot-win.png)
