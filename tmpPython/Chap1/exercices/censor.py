def censor (text, word):
    new_line = []
    asterisks = '*' * len(word)
    for wds in text.split():
        if wds == word:
            new_line.append(asterisks)
        else:
            new_line.append(wds)
    return " ".join(new_line)
