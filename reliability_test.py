import os
import logging
from dotenv import load_dotenv
from google import genai
from logic_utils import check_guess, parse_guess, update_score

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

test_cases = [
    # CHECK GUESS TEST CASES
    {
        "description": "Correct guess should be a win",
        "function": "check_guess",
        "input": (50, 50),
        "expected": "Win"
    },
    {
        "description": "Guess too high should return Too High",
        "function": "check_guess",
        "input": (60, 50),
        "expected": "Too High"
    },
    {
        "description": "Guess too low should return Too Low",
        "function": "check_guess",
        "input": (40, 50),
        "expected": "Too Low"
    },
    # PARSE GUESS TEST CASES
    {
        "description": "Valid number string should parse correctly",
        "function": "parse_guess",
        "input": ("42",),
        "expected": True
    },
    {
        "description": "Non-number guess should fail to parse",
        "function": "parse_guess",
        "input": ("abc",),
        "expected": False
    },
    # UPDATE SCORE TEST CASES
    {
        "description": "Win on first attempt should score 90",
        "function": "update_score",
        "input": (0, "Win", 1),
        "expected": 90
    },
    {
        "description": "Wrong guess Too Low should deduct 5 points",
        "function": "update_score",
        "input": (100, "Too Low", 1),
        "expected": 95
    },
]

# Create log file to timestamp every entry so every test result gets saved there
logging.basicConfig(
    filename="reliability_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

results = []

for test in test_cases:
    fn = test["function"]
    args = test["input"]
    expected = test["expected"]

    try:
        if fn == "check_guess":
            actual_outcome, _ = check_guess(*args)
            actual = actual_outcome
        elif fn == "parse_guess":
            ok, _, _ = parse_guess(*args)
            actual = ok
        elif fn == "update_score":
            actual = update_score(*args)

        passed = actual == expected
        status = "PASS" if passed else "FAIL"
        
        logging.info(f"{status} | {test['description']} | expected={expected}, got={actual}")
        results.append({
            "description": test["description"],
            "expected": expected,
            "actual": actual,
            "status": status
        })
    except Exception as e:
        logging.error(f"ERROR | {test['description']} | {e}")
        results.append({
            "description": test["description"],
            "expected": expected,
            "actual": "ERROR",
            "status": "ERROR"
        })

lines = []

for r in results:
    line = f"- [{r['status']}] {r['description']} | expected={r['expected']}, got={r['actual']}"
    lines.append(line)

summary = "\n".join(lines)

prompt = f"""
You are a software reliability evaluator for a number guessing game.

Here are the test results from running the game logic:

{summary}

Please evaluate:
1. Are the results correct and consistent?
2. Are there any concerning failures?
3. Give an overall reliability score from 0.0 to 1.0 as a percentage
4. Give a short recommendation for improvement.

Be concise and specific.
"""

try:
    print("\n⏳ Sending results to Gemini for evaluation...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    print("\n===== GEMINI RELIABILITY REPORT =====")
    print(response.text)
    logging.info(f"Gemini report generated successfully")
except Exception as e:
    print(f"Gemini error: {e}")
    logging.error(f"Gemini API error: {e}")

print("\n===== TEST SUMMARY =====")
for r in results:
    print(f"[{r['status']}] {r['description']}")

passed = 0
for r in results:
    if r["status"] == "PASS":
        passed += 1
print(f"\n{passed}/{len(results)} tests passed")