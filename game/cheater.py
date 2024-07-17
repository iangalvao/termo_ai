import string
from game.solver_tools import WordFilter
from game.attempt import Attempt
from game.hint import Hint
from game.tree import init_game

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
        print(palavras_restantes[0:20])
        if len(palavras_restantes) < 16:
            word, mean = solver.select_word_from_mean_filter_size(palavras_restantes)
            print(word, mean)
