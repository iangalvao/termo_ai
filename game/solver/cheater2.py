from game.solver.solver_tools import WordFilter
from game.solver.word_checker import WordChecker


word_filter = WordFilter()


# apply a filter based on guess considering each possible word being the correct one.
# return the distribution of remaining lenght of possible words after the filter.
def filter_size_distribution(self, word, possible_words, word_checker: WordChecker):
    results = []
    for pw in possible_words:
        feedback = word_checker.get_feedback_from_guess(word, pw)

        remaining_words_size = len(
            word_filter.filter_from_feedback(
                word,
                feedback,
                possible_words,
            )
        )
        results.append(remaining_words_size)

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
