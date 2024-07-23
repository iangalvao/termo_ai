import pytest
from game.solver.solver_tools import VocabularyAnalyser


@pytest.fixture
def vocabulary_english():
    return [
        "perform",
        "warm",
        "swift",
        "aggressive",
        "defective",
        "boot",
        "consist",
        "narrow",
        "yak",
        "lush",
        "venomous",
        "flat",
        "elated",
        "ski",
        "corn",
        "curvy",
        "boring",
        "trousers",
        "hair",
        "material",
        "lewd",
        "rock",
        "skinny",
        "fast",
        "ready",
        "trucks",
        "bead",
        "bury",
        "cemetery",
        "ignore",
        "fold",
        "battle",
        "festive",
        "cheat",
        "lie",
        "tight",
        "workable",
        "brother",
        "spiritual",
        "throne",
        "reminiscent",
        "join",
        "annoy",
        "unsuitable",
        "obedient",
        "easy",
        "flavor",
        "organic",
        "bite-sized",
        "fade",
        "liquid",
        "same",
        "hang",
        "silk",
        "railway",
        "calendar",
        "political",
        "giants",
        "hospitable",
        "obscene",
        "eminent",
        "frogs",
        "useful",
        "natural",
        "harmony",
        "outgoing",
        "gather",
        "round",
        "sign",
        "extra-large",
        "monkey",
        "food",
        "hurt",
        "fretful",
        "kneel",
        "geese",
        "hum",
        "necessary",
        "flowery",
        "dull",
        "curtain",
    ]


@pytest.fixture
def vocabulary_simple():
    return ["aba", "omo", "ele", "ixi", "ugu", "ada", "oto", "erre", "idi", "uju"]


def test_cluster_letters_by_occurrence_from_english_dict(vocabulary_english):
    analyser = VocabularyAnalyser(vocabulary_english)
    result = analyser.cluster_letter_by_occurrence()

    expected_result = {"a", "o", "e", "u", "i"}

    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_cluster_letters_by_occurrence_from_short_dict(vocabulary_simple):
    analyser = VocabularyAnalyser(vocabulary_simple)
    result = analyser.cluster_letter_by_occurrence()

    expected_result = {"a", "o", "e", "u", "i"}

    assert result == expected_result, f"Expected {expected_result}, but got {result}"


from game.solver.tree import init_game


@pytest.fixture
def palavras_pt():
    n_desafios, lim_chutes, palavras_unidecode, palavras, solver, palavras_possiveis = (
        init_game()
    )
    return palavras_unidecode


def test_cluster_letters_by_occurrence_from_all_pt_words(palavras_pt):
    analyser = VocabularyAnalyser(palavras_pt)
    result = analyser.cluster_letter_by_occurrence()

    expected_result = {"a", "o", "e", "u", "i"}

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
