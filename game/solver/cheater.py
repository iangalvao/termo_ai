import string
from game.solver.solver_tools import WordFilter
from game.model.attempt import Attempt
from game.model.hint import Hint
from game.solver.tree import init_game


def find_all_word_differences(letter_count, words, target=2.5):
    # Convert the letter count values to floats
    letter_count = {k: float(v) for k, v in letter_count.items()}

    word_differences = []

    for word in words:
        # Calculate the sum of the letter counts for the word
        total = sum(letter_count.get(char, 1) for char in set(word))
        word_differences.append((word, total))

    return word_differences


def get_good_guesses(letter_count, words):
    letter_count = {k: float(v) for k, v in letter_count.items()}

    word_differences = []

    for word in words:
        # Calculate the sum of the letter counts for the word
        if any([c for c in word if c not in letter_count.keys()]):
            continue
        if any([c for c in word if word.count(c) > 1]):
            continue
        total = sum(letter_count.get(char, 1) for char in set(word))
        word_differences.append((word, total))

    return word_differences


if __name__ == "__main__":
    n_desafios, lim_chutes, palavras_restantes, palavras, solver, palavras_possiveis = (
        init_game()
    )
    palavras_restantes = palavras_possiveis
    wf = WordFilter()
    # word, mean = solver.select_word_from_mean_filter_size(palavras_restantes)
    # print(word, mean)
    while len(palavras_restantes) > 0:
        guess = input("guess: ")
        if guess == "":
            word, mean = solver.select_word_from_mean_filter_size(palavras_restantes)
            print(word, mean)
            continue
        feedbacks = input("feedbacks: ")
        feedbacks = [Hint(int(l)) for l in feedbacks]
        palavras_restantes = wf.filter_from_feedback(
            guess, feedbacks, palavras_restantes
        )
        contagem_letras = {
            c: (
                len([w for w in palavras_restantes if c in w]) / len(palavras_restantes)
            )
            for c in string.ascii_lowercase
        }

        formatted_data = {key: f"{value:.2f}" for key, value in contagem_letras.items()}
        print(formatted_data)

        good_guesses = get_good_guesses(
            {k: v for k, v in contagem_letras.items() if v != 0 and v != 1},
            palavras_possiveis,
        )

        good_guesses = sorted(good_guesses, key=lambda item: -abs(item[1] - 2.5))[0:40]
        formatted_data = {key: f"{value:.2f}" for key, value in good_guesses}

        print("Good Guesses:\n", formatted_data)
        print(f"Up to 80 remainig words of a total of: {len(palavras_restantes)}")
        print(palavras_restantes[0:80])
        if len(palavras_restantes) < 20:
            word, mean = solver.select_word_from_mean_filter_size(palavras_restantes)
            print(word, mean)
