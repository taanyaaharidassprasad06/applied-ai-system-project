# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**GlitchGuard 1.0**  

---

## 2. Intended Use  

This system uses Google Gemini as an AI-powered reliability evaluator for a number guessing game. It is designed for developers and students who want to assess whether their game logic is working correctly after making changes to the code.
 
- It evaluates automated test results from the game's core logic functions and returns a reliability score and recommendations to enhance the system
- It assumes the user has some familiarity with running Python applications and reading test output
- This was built for a classroom final project but follows patterns used in real software quality assurance workflows

---

## 3. How the Model Works  

The game logic is tested by running a set of predefined checks such as verifying that a correct guess returns a win, that an invalid input is rejected, and that the score updates correctly. Each check records whether it passed or failed.  

Those results are then summarized and sent to Gemini with a prompt asking it to act as a software reliability evaluator. Gemini reads the summary and does four things: it checks whether the results look correct and consistent, it flags any failures that seem concerning, it assigns an overall reliability score from 0.0 to 1.0, and provides short recommemdations for improvement.

---

## 4. Data  

The system does not use a dataset in the traditional sense. Instead, it runs against the game's own logic functions as the source of truth. There are 7 test cases covering three functions:
 
- `check_guess()` — 3 tests (correct guess, too high, too low)
- `parse_guess()` — 2 tests (valid input, invalid input)
- `update_score()` — 2 tests (win scoring, wrong guess deduction). 

All test cases were written manually based on known bugs found during the base project debugging phase. Edge cases like boundary values, negative numbers, and very large integers are not currently represented.

---

## 5. Strengths  

- Gemini consistently identified passing tests as correct
- When all tests pass, the reliability score is around 0.9–1.0
- The recommendations Gemini provides are actionable and specific
- The evaluation adds context that raw pass/fail output does not, such as explaining what a failure might mean and why it matters


---

## 6. Limitations and Bias 

- Gemini's output is non-deterministic so the same test results can produce slightly different wording or scores across runs, so the reliability score should be treated as a directional signal rather than a precise measurement
- The test suite only covers cases that were known to be buggy from the base project. Unknown edge cases are not tested, so a perfect score does not guarantee the code is fully correct
- Gemini has no knowledge of the game's context beyond what is in the prompt. If a test fails for a subtle reason, it may give a generic recommendation rather than a precise diagnosis
- The system cannot test the Streamlit UI layer — only the pure logic functions in `logic_utils.py` are covered

---

## 7. Evaluation  

Several scenarios were tested to verify the evaluator behaved correctly:
 
- Running all tests after the bugs were fixed — all 7 passed and Gemini returned a score of 1.0
- Manually introducing a bug (changing a `==` to `>` in `check_guess`) to verify Gemini would flag it — it correctly identified the failure and lowered the score
- Running the tester multiple times with the same passing results to check consistency — the score stayed between 0.9 and 1.0 across runs, though the wording varied slightly
The most surprising finding was that even with all tests passing, Gemini consistently recommended adding boundary value tests — which is correct advice, since those cases genuinely are not covered.

---

## 8. Future Work  

- Add boundary value tests (guessing exactly the minimum and maximum of each difficulty range)
- Add tests for invalid inputs like negative numbers, decimals, and extremely large integers
- Extend testing to cover the scoring system across multiple attempts, not just the first attempt

---

## 9. Personal Reflection  

One thing I learned from this project is that testing individual functions is really important for catching logic issues early. Even small mistakes in functions like parsing or scoring can lead to incorrect behavior if they’re not verified properly.  

I also learned how useful structured testing is for making results measurable and consistent. Running predefined test cases helped me clearly see whether each function was working as expected, instead of just assuming it was correct.  

Overall, this project showed me how combining traditional testing with an AI evaluation layer, using the Gemini API, can help interpret results at a higher level. While the tests verify correctness at the function level, the AI adds a reflective layer that summarizes consistency and reliability, which is closer to how applied AI systems can support debugging and evaluation workflows.
