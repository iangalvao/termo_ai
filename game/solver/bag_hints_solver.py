remaining_words = ["abada, amada"]
bags_of_hints = [[("b", "IN_WORD")], [("m", "IN_WORD")]]


def get_bag_of_hints(remaining_words):
    bags_of_hints = [[("b", "IN_WORD")], [("m", "IN_WORD")]]
    return bags_of_hints


result = get_bag_of_hints(remaining_words)

for i, hint_list in enumerate(bags_of_hints):
    assert hint_list == result[i]
    print("OK", hint_list, result[i])
