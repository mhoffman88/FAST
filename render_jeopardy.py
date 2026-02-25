import re
import streamlit as st

from render_jeopardy_questions import get_randomized_jeopardy_board


def _normalize(text: str) -> str:
    """Normalize answers for forgiving comparisons."""
    lowered = text.strip().lower()
    stripped = re.sub(r"^(what|who)\s+is\s+", "", lowered)
    stripped = re.sub(r"^what\s+are\s+", "", stripped)
    return re.sub(r"[^a-z0-9]+", "", stripped)


def _initialize_state() -> None:
    if "jeopardy_board" not in st.session_state:
        st.session_state.jeopardy_board = get_randomized_jeopardy_board()

    if "jeopardy_revealed" not in st.session_state:
        st.session_state.jeopardy_revealed = {
            (cat_i, clue_i): False
            for cat_i, category in enumerate(st.session_state.jeopardy_board)
            for clue_i, _ in enumerate(category["clues"])
        }
    if "jeopardy_score" not in st.session_state:
        st.session_state.jeopardy_score = 0
    if "jeopardy_active" not in st.session_state:
        st.session_state.jeopardy_active = None


def _reset_game() -> None:
    st.session_state.jeopardy_board = get_randomized_jeopardy_board()
    st.session_state.jeopardy_revealed = {
        (cat_i, clue_i): False
        for cat_i, category in enumerate(st.session_state.jeopardy_board)
        for clue_i, _ in enumerate(category["clues"])
    }
    st.session_state.jeopardy_score = 0
    st.session_state.jeopardy_active = None


def run_jeopardy_game() -> None:
    st.title("FAST Jeopardy: Steward Edition")
    st.caption("Pick a clue value, answer it, and build your score. Board resets with random categories and random clues each game.")

    _initialize_state()
    board = st.session_state.jeopardy_board

    top_left, top_right = st.columns([2, 1])
    with top_left:
        st.subheader(f"Score: {st.session_state.jeopardy_score}")
    with top_right:
        if st.button("New Random Game"):
            _reset_game()
            st.rerun()

    board_cols = st.columns(len(board))
    for cat_i, category in enumerate(board):
        with board_cols[cat_i]:
            st.markdown(f"**{category['category']}**")
            for clue_i, clue in enumerate(category["clues"]):
                clue_key = (cat_i, clue_i)
                already_used = st.session_state.jeopardy_revealed[clue_key]
                label = "—" if already_used else f"${clue['value']}"
                if st.button(
                    label,
                    key=f"clue_{cat_i}_{clue_i}",
                    disabled=already_used,
                    use_container_width=True,
                ):
                    st.session_state.jeopardy_active = (cat_i, clue_i)

    active = st.session_state.jeopardy_active
    if active is None:
        return

    cat_i, clue_i = active
    clue = board[cat_i]["clues"][clue_i]

    st.divider()
    st.subheader(f"For ${clue['value']}: {board[cat_i]['category']}")
    st.write(clue["question"])

    response = st.text_input("Your answer", key=f"response_{cat_i}_{clue_i}")

    check_col, reveal_col = st.columns(2)
    with check_col:
        if st.button("Check Answer", key=f"check_{cat_i}_{clue_i}"):
            is_correct = _normalize(response) == _normalize(clue["answer"])
            if is_correct:
                st.success(f"Correct! +{clue['value']} points")
                st.session_state.jeopardy_score += clue["value"]
            else:
                st.error(f"Not quite. Correct answer: {clue['answer']}")
                st.session_state.jeopardy_score -= clue["value"]

            st.session_state.jeopardy_revealed[(cat_i, clue_i)] = True
            st.session_state.jeopardy_active = None
            st.rerun()

    with reveal_col:
        if st.button("Reveal Answer", key=f"reveal_{cat_i}_{clue_i}"):
            st.info(f"Answer: {clue['answer']}")
