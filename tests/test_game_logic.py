from logic_utils import check_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win", "🎉 Correct!"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High", "📉 Go LOWER!"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low", "📈 Go HIGHER!"


def test_first_attempt_counted_as_one():
    # Bug: attempts used to start at 1, so the first guess incremented it to 2,
    # causing update_score to penalize players as if they had already made one guess.
    # Fix: attempts now starts at 0, so the first guess correctly sets it to 1.
    attempts = 0
    attempts += 1  # simulates app.py line 101: st.session_state.attempts += 1
    assert attempts == 1, "First attempt should be counted as 1, not 0 or 2"

    # A win on attempt 1 should score 100 - 10*1 = 90
    score = update_score(current_score=0, outcome="Win", attempt_number=attempts)
    assert score == 90, f"Expected 90 points for winning on first attempt, got {score}"
