from talon.voice import Word, Context, Str

from user.utility import surround, parse_word

formatters = {
    # Smashed
    "acronym": (True, lambda i, word, _: word[0:1].upper()),
    "tree": (True, lambda i, word, _: word[0:3] if i == 0 else ""),
    "quad": (True, lambda i, word, _: word[0:4] if i == 0 else ""),
    "dunder": (
        True,
        lambda i, word, last: ("__%s" % word if i == 0 else word)
        + ("__" if last else ""),
    ),
    "camel": (True, lambda i, word, _: word if i == 0 else word.capitalize()),
    "snake": (True, lambda i, word, _: word if i == 0 else "_" + word),
    "smash": (True, lambda i, word, _: word),
    "spine": (True, lambda i, word, _: word if i == 0 else "-" + word),
    
    # Spaced
    "sentence": (False, lambda i, word, _: word.capitalize() if i == 0 else word),
    "title": (False, lambda i, word, _: word.capitalize()),
    "allcaps": (False, lambda i, word, _: word.upper()),
    "string": (False, surround("'")),
    "quoted": (False, surround('"')),
    "padded": (False, surround(" ")),
}

def FormatText(m):
    fmt = []
    for w in m._words:
        if isinstance(w, Word):
            fmt.append(w.word)
    words = [str(s).lower() for s in m.dgndictation[0]._words]

    tmp = []
    spaces = True
    for i, word in enumerate(words):
        word = parse_word(word)
        for name in reversed(fmt):
            smash, func = formatters[name]
            word = func(i, word, i == len(words) - 1)
            spaces = spaces and not smash
        tmp.append(word)
    words = tmp

    sep = " "
    if not spaces:
        sep = ""
    Str(sep.join(words))(None)


ctx = Context("formatters")
ctx.keymap(
    {
        # 'word <dgnwords>': word,
        "(%s)+ <dgndictation>"
        % (" | ".join(formatters)): FormatText
    }
)