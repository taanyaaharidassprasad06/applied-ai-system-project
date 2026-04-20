#FIX: Refactored the logic functions from app.py into this file logic_utils.py using Claude Code
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    #FIX: Swap ranges for Normal and Hard difficulties to make Normal easier than Hard as intended
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        #FIXME: attempt_number is already 1-indexed in the app, so this scoring system is harsher than intended because it subtracts 10 more points than expected on each attempt
        #FIX: Adjusted scoring system to account for attempt_number being 1-indexed by removing the +1, so it subtracts the intended amount of points on each attempt
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    #FIXME: To High rewarded points on every other too high guess
    #FIX: Too High always deducts 5 points like Too Low — wrong guesses should never add score
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
