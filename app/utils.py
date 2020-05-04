from typing import Optional


def get_sentence_lemmas(sentence, categories=None):
    if sentence.terminals:
        return (t.lemma for t in sentence.terminals
               if t.category != 'grm' and (categories is None or t.category in categories))

    elif sentence.tokens:
        def get_first_relevant_variation(token) -> Optional[str]:
            val = token.val
            if not val:
                return None
            if not isinstance(val, list):
                val = [val]
            for v in val:
                cat = getattr(v, 'ordfl', None)
                if cat != 'grm' and (categories is None or cat in categories):
                    return v.stofn

        lst = (get_first_relevant_variation(t) for t in sentence.tokens)
        return (i for i in lst if i)

    else:
        return iter([])
