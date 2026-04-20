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
    #FIX: Change attempt limit to make Easy have the most attempts and Hard have the least attempts
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
    #FIXME: Attempts should start at 0 instead of 1 since the player has not made a guess yet
    #FIX: Changed initial value from 1 to 0 so the first guess is counted as an attempt
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "feedback" not in st.session_state:
    st.session_state.feedback = None

st.subheader("Make a guess")

st.info(
    #FIX: Use actual low / high values from get_range_for_difficulty instead of hardcoded 1 and 100
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
    # FIXME: Guess input does not reset properly on new game
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

#FIXME: New game button does not reset the game state properly
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    #FIX: Reset remaining game settings back to the initial state using Claude Code to ensure new game is started
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.feedback = None
    st.session_state.game_id = st.session_state.get("game_id", 0) + 1
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)
        
        #FIXME: The game behaves inconsistently every other attempt, sometimes treating the secret as a string and sometimes as an int which results in miscounting the attempts
        #FIX: Always pass secret as int so check_guess comparison is consistent
        outcome, message = check_guess(guess_int, st.session_state.secret)

        #FIX: Store hint messages in session state so they persist across reruns and can be displayed after the guess is processed
        st.session_state.feedback = message if show_hint else None

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
               )
    #FIX: Rerun the app after submitting a guess to ensure the number of attempts left / used is reflected correctly
    # Only rerun while playing so won/lost final messages (which include the secret) are not swallowed
    if st.session_state.status == "playing":
        st.rerun()
# FIX: Display feedback message after processing the guess so it persists across reruns and is not lost when the user submits a new guess
if st.session_state.feedback:
    st.warning(st.session_state.feedback)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
