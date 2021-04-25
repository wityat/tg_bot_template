from ...db.models import AutopostingFunction
from ...modules.keyboard import KeyboardInline
from itertools import islice


def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k: data[k] for k in islice(it, SIZE)}


def checkbox(flag: bool):
    if flag:
        return "✅"
    return "🚫"

