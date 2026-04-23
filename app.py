import subprocess
import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    # FIX: Change attempt limit to make Easy have the most attempts and Hard have the least attempts
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # TO FIX: Attempts should start at 0 instead of 1 since the player has not made a guess yet
    # FIX: Changed initial value from 1 to 0 so the first guess is counted as an attempt
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "feedback" not in st.session_state:
    st.session_state.feedback = None

if "error_message" not in st.session_state:
    st.session_state.error_message = None

# FIX: Added final_message to session state so the secret is revealed after the game ends
if "final_message" not in st.session_state:
    st.session_state.final_message = None

# FIX: Added win_message to session state so the score shows when game won
if "win_message" not in st.session_state:
    st.session_state.win_message = None

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False


st.subheader("Make a guess")

st.info(
    # FIX: Use actual low / high values from get_range_for_difficulty instead of hardcoded 1 and 100
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    # TO FIX: Guess input does not reset properly on new game
    # FIX: Added game_id to the key to ensure it resets properly when a new game is started
    key=f"guess_input_{difficulty}_{st.session_state.get('game_id', 0)}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# TO FIX: New game button does not reset the game state properly
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    # FIX: Reset remaining game settings back to the initial state using Claude Code to ensure new game is started
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.feedback = None
    st.session_state.game_id = st.session_state.get("game_id", 0) + 1
    st.session_state.error_message = None
    st.session_state.final_message = None
    st.session_state.win_message = None
    st.session_state.show_balloons = False
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        if st.session_state.show_balloons:
            st.balloons()
            st.session_state.show_balloons = False
        # FIX: Show win_message with the score if won
        if st.session_state.win_message:
            st.success(st.session_state.win_message)
        else:
            st.success("You already won. Start a new game to play again.")
        if st.session_state.feedback:
            st.warning(st.session_state.feedback)
    else:
        # FIX: Show final_message with the secret number and generic game over message together
        st.error(st.session_state.final_message)
        st.error("Game over. Start a new game to try again.")

    st.divider()
    st.subheader("🧪 Reliability Tester")

    if st.button("Run Reliability Tests"):
        with st.spinner("Running tests..."):
            result = subprocess.run(
                ["python", "reliability_test.py"],
                capture_output=True,
                text=True
            )
        st.markdown(result.stdout)

    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.error_message = err
    else:
        st.session_state.attempts += 1
        st.session_state.error_message = None
        st.session_state.history.append(guess_int)
        
        # TO FIX: The game behaves inconsistently every other attempt, sometimes treating the secret as a string and sometimes as an int which results in miscounting the attempts
        # FIX: Always pass secret as int so check_guess comparison is consistent
        outcome, message = check_guess(guess_int, st.session_state.secret)

        # FIX: Store hint messages in session state so they persist across reruns and can be displayed after the guess is processed
        st.session_state.feedback = message if show_hint else None

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.show_balloons = True
            # FIX: Store win message in session state instead of displaying directly so it persists across the rerun
            st.session_state.win_message = (
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                # FIX: Store final message in session state instead of displaying directly so it persists across the rerun
                st.session_state.final_message = (
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
    # FIX: Rerun after every guess so the attempts left counter and game state update immediately
    # without st.rerun() attempts is incremented but the info bar shows the old value (before incrementing) since Streamlit renders top to bottom so the attempts incrementing is not rendered in UI
    # with st.rerun() attempts is incremented when submit is pressed and the script restarts from the top to correctly render to accurate attempts left count
    st.rerun()
# FIX: Display feedback message after processing the guess so it persists across reruns and is not lost when the user submits a new guess
if st.session_state.feedback:
    st.warning(st.session_state.feedback)

if st.session_state.error_message:
    st.error(st.session_state.error_message)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")

st.divider()
st.subheader("🧪 Reliability Tester")

if st.button("Run Reliability Tests"):
    with st.spinner("Running tests..."):
        result = subprocess.run(
            ["python", "reliability_test.py"], # start new python process and run reliability_test.py
            capture_output=True, # capture everything it prints and store in results
            text=True # output is received as a normal string
        )

    st.markdown(result.stdout)