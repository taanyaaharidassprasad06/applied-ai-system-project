# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - Simple UI, tell user how many guesses they have, has an input box to type guess, has two buttons to submit guess and start a new game, has a toggle to show hint.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  - Hints were backwards (I guessed a number and it said 'GO LOWER' when I actually needed to 'GO HIGHER')
  - New game button is not creating a new game to start over (Expected it to clear the input and reset the game but it does not do anything)
  - Normal level has range 1-100 while Hard level has range 1-50 (does not really make sense as it would be expected for hard mode to be 1-100 and normal to be 1-50)
  - Easy mode range is 1-20 but the secret number was 44 (does not make sense again as the number should stay within the range of 1-20)
  - Message at top always says "Guess a number between 1 and 100" regardless of level chosen
  - Game ended after certain number of attempts but still says I have one attempt remaining (not counting first attempt as an attempt)
    - Reveals secret number even if one attempt is still left + submitting that last attempt (to make it 0) reveals a 'Game Over' message
    - First guess is not counting as attempt 1
    - Attempts only counts every other attempt unless "Submit Guess" button is clicked multiple times after one input has been given (Expected to count every guess as an attempt)
  - Guessing a number that is "Too High" rewards points instead of subtracting on every other "Too High" guess

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude Code and ChatGPT. I primarily used Claude Code to fix bugs and I used ChatGPT to understand the code in app.py
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - One suggestion it gave that was correct was making the "New Game" button work as intended. The initial code skipped resetting some settings when the button was clicked which is why the button did not necessarily simulate a new game. Claude Code added in the missing states and reset them to their initial value which caused the New Game button to work as intended (such as status, history, score, feedback, and also generated a new game id to start a fresh game). I verified this result by clicking the "New Game" button on the app and verified if the input field was cleared as well as if the above settings were empty / 0.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - One suggestion that was misleading was that Claude Code initially had some trouble fixing the incorrect counting of attempts. At first, when the user entered a guess, the app would not count that initial guess as 1 attempt. The fix it gave was to refactor many lines of code which did not seem ideal for such a simple issue. So I rejected the suggestion and created a new chat to describe the issue I was facing in more detail and it was able to fix the issue with one line which was adding a simple rerun command towards the end of the file. However, this line led to another bug which was that the hints were no longer showing and the secret number was not revealed when the game was over. To fix this, Claude suggested to sav the feedback in a variable and display it after the rerun() is called so that the messages would persist / show even if the app was rerun. I verified this result by guessing 1 number and checked to see if attempts would increase to 1. I also submitted multiple guesses to see if hints were displaying as well as used all my guesses to see if the secret number would be revealed at the end. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - To decide whether a bug was really fixed, I mainly relied on manual testing. Each time I would fix a bug, I would go back to the app and test the fix. Whether it was clicking a button or entering an input, I would verify if my fix worked and the app displays what was intended.
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  - One test I ran using pytest was to see if the scoring was correctly displayed. Initially, the app would penalize the user on the first try as in it would deduct an extra 10 points on their first guess. This is not how the game should work. Instead, the app should only deduct 10 points on the first guess instead of 20. Using pytest I was able to verify if this worked.
- Did AI help you design or understand any tests? How?
  - I used Claude Code to write the pytest I described above. I sent it a message with the test I am trying to verify and based on that it generated a pytest for me. 

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  - The secret number did not change in the sense that a new number kept on being randomly generated. The secret number seemed like it changed because it would toggle between an interger and a string. on every odd attempt, the secret number was kept as an integer but on every even attempt the secret number was converted to a string so guessing the right number could result in a hint being displayed instead of winning the game. 
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Everytime you interact with a Streamlit app whether it is through clicking a button or typing and input, the Python script reruns from scratch and is similar to refreshing a webpage. This means any regular variables get destroyed but persistent ones such as state preserve their value across reruns.
- What change did you make that finally gave the game a stable secret number?
  - The change I made was always keeping the secret number as an integer so that the comparison is always consistent.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    - One habit from the project I want to reuse in the future is the way I prompted Claude Code. I realized that it is important to be specific with my messages rather than vague as that helps it identify the root issue causing the bugs. Sometimes when I was too vague it would identify a fix that results in many unnecessary changes or it would not accurately understand what I am trying to ask. Being more specific but also concise results in a better response and suggestions.
    - I also learned creating new chats for each bug is beneficial as each chat is focused solely on that bug instead of previous messages that might have zero correlation to the problem you are currently trying to fix.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I think right from the start I would try to be more detailed. This could save more time and help me work more efficiently rather than prompting it with more follow up messages or questions.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - This project really taught me how to work with AI generated code. I realized that this project, though generated by AI, still had many buggy features that needed attention. However, with the use of AI I was able to fix these features with minimal changes. I learned that it is still important to look over AI generated code as sometimes it is not always accurate but it can speed up development workflow.
