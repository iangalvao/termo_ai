import string
from game.solver_tools import WordFilter
from game.attempt import Attempt
from game.hint import Hint
from game.tree import init_game


def find_all_word_differences(letter_count, words, target=2.5):
    # Convert the letter count values to floats
    letter_count = {k: float(v) for k, v in letter_count.items()}

    word_differences = []

    for word in words:
        # Calculate the sum of the letter counts for the word
        total = sum(
            letter_count.get(char, 0)
            for char in set(word)
            if letter_count[char] not in [0, 1]
        )

        # Calculate the difference from the target
        difference = abs(total - target)

        # Append the word and its difference to the list
        word_differences.append((word, difference))

    return word_differences


if __name__ == "__main__":
    n_desafios, lim_chutes, palavras_restantes, palavras, solver, palavras_possiveis = (
        init_game()
    )
    palavras_restantes = palavras_possiveis
    wf = WordFilter()
    while len(palavras_restantes) > 0:
        guess = input("guess: ")
        feedbacks = input("feedbacks: ")
        feedbacks = [Hint(int(l)) for l in feedbacks]
        palavras_restantes = wf.filter_from_feedback(
            guess, feedbacks, palavras_restantes
        )
        contagem_letras = {
            c: len([w for w in palavras_restantes if c in w]) / len(palavras_restantes)
            for c in string.ascii_lowercase
        }

        formatted_data = {
            key: f"{value:.2f}" for key, value in contagem_letras.items() if value != 0
        }
        print(formatted_data)
        good_guesses = find_all_word_differences(contagem_letras, palavras_possiveis)

        good_guesses = sorted(good_guesses, key=lambda item: item[1])[0:10]
        formatted_data = {key: f"{value:.2f}" for key, value in good_guesses}

        print("Good Guesses:\n", formatted_data)
        print("Up to twenty remainig words:")
        print(palavras_restantes[0:20])
        if len(palavras_restantes) < 16:
            word, mean = solver.select_word_from_mean_filter_size(palavras_restantes)
            print(word, mean)
