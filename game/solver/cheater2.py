from game.model.hint import Hint
from game.solver.solver_tools import WordFilter
from game.solver.tree import init_game
from game.solver.word_checker import WordChecker


word_filter = WordFilter()


# apply a filter based on guess considering each possible word being the correct one.
# return the distribution of remaining lenght of possible words after the filter.


# apply a filter based on guess considering each possible word being the correct one.
# return the distribution of remaining lenght of possible words after the filter.
def filter_size_distribution(word, possible_words, word_checker: WordChecker):
    results = []
    if len(possible_words) > 200:
        for i in range(243):
            f4 = i % 3
            f3 = i % 9 // 3
            f2 = i % 27 // 9
            f1 = i % 81 // 27
            f0 = i // 81

            feedback = [f0, f1, f2, f3, f4]
            # print(feedback)
            for i, f in enumerate(feedback):
                if f == 0:
                    feedback[i] = Hint.WRONG_LETTER
                elif f == 1:
                    feedback[i] = Hint.WRONG_POS
                elif f == 2:
                    feedback[i] = Hint.RIGHT_POS

            initial_len = len(possible_words)
            possible_words = word_filter.negative_filter_from_feedback(
                word,
                feedback,
                possible_words,
            )
            # print(word, feedback, filter)
            remaining_words_size = initial_len - len(possible_words)
            if remaining_words_size > 0:
                results.append(remaining_words_size)
                print(word, feedback, remaining_words_size)

        return results


word_checker = WordChecker()


def f(possible_words, word_list):
    for guess in word_list:
        filter_sizes = filter_size_distribution(guess, possible_words, word_checker)

        if len(filter_sizes) == 0:
            continue
        mean = sum(filter_sizes) / len(filter_sizes)
        max_value = max(filter_sizes)
        if max_value == 1:
            return guess, mean
        if max_value <= best_max_value:
            if mean < best_mean or max_value < best_max_value:
                best_max_value = max_value
                best_mean = mean
                best_word = guess

    return best_word, best_mean


if __name__ == "__main__":
    n_desafios, lim_chutes, palavras_restantes, palavras, solver, palavras_possiveis = (
        init_game()
    )

    for palavra in palavras_restantes[0:10]:
        print(filter_size_distribution(palavra, palavras_possiveis, word_checker))
