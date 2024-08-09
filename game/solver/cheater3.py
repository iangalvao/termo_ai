import csv
import string
from typing import List

from unidecode import unidecode


def get_words_with_letters(letters: List[str], words: List[str]):
    for letter in letters:
        words = [w for w in words if letter in w]
    return words


def init_game():
    # Check if an argument is passed
    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras_originais = next(myreader)
    palavras_unidecode = {}
    lista_unidecode = []
    for palavra in palavras_originais:
        palavras_unidecode[unidecode(palavra)] = palavra
        lista_unidecode.append(unidecode(palavra))
    lista_unidecode = list(palavras_unidecode.keys())
    palavra_possiveis = list(palavras_unidecode.keys())[9147:]

    return (
        lista_unidecode,
        palavra_possiveis,
    )


def word_have_n_of_selected_chars(word, n, chars):
    if len([l for l in chars if l in word]) >= n:
        return True
    return False


def palavras_de_tres_consoantes_nao_r_nao_s_nao_l_nao_m_nao_n(palavras):
    letters_not = ["l", "m", "n", "r", "s"]
    letters_have = ["t", "p", "d", "f", "g", "c", "v", "b"]
    palavras = [w for w in palavras if len([l for l in letters_not if l in w]) == 0]
    palavras = [w for w in palavras if len([l for l in letters_have if l in w]) >= 3]
    return palavras


if __name__ == "__main__":
    palavras_unidecode, palavras_possiveis = init_game()
    palavras = palavras_possiveis
    contagem_letras = {
        c: (len([w for w in palavras if c in w]) / len(palavras))
        for c in string.ascii_lowercase
    }

    formatted_data = {key: f"{value:.2f}" for key, value in contagem_letras.items()}
    print(formatted_data)
    print(palavras_de_tres_consoantes_nao_r_nao_s_nao_l_nao_m_nao_n(palavras_unidecode))
    for l in "aeiourtsl":
        for i in range(5):
            print(
                l,
                i + 1,
                (
                    (
                        len([w for w in palavras if l == w[i]])
                        / len([w for w in palavras if l in w])
                    )
                    * contagem_letras[l]
                ),
            )
        print("\n")

    prob_dica = {}
    for l in string.ascii_lowercase:
        prob_dica[l] = []
        for i in range(5):
            prob_dica[l].append(
                (
                    len([w for w in palavras if l == w[i]])
                    / max(len([w for w in palavras if l in w]), 0.1)
                )
                * contagem_letras[l]
            )
    for key, item in prob_dica.items():
        print(key, "".join(f"{value:.2f}, " for value in item))

    prob_words = {}
    for word in palavras:
        p = 1
        for i, l in enumerate(word):
            p *= 1 - prob_dica[l][i]
        prob_words[word] = 1 - p
        if any([l for l in word if len([c for c in word if c == l]) > 1]):
            prob_words[word] = 0
    # print(prob_words)
    best_words = list(prob_words.keys())
    best_words.sort(key=lambda x: prob_words[x])
    best_words = [(w, prob_words[w]) for w in best_words[-20:]]
    print(best_words)
    letters = input("letters: ").strip()
    print(get_words_with_letters(letters, palavras_unidecode))
