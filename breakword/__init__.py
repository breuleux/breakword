import colorsys
import hashlib
import os
import pdb
import random

from .common_words import common_words, common_words_source


_acquired = {}
_log = print


def set_default_logger(logger):
    """Set the default logger used by log."""
    global _log
    _log = logger


def file_source(filename, exclude=set()):
    """Return a list of words picked from the given file.

    One word per line. Words in the exclude set are removed from the list.
    """

    def make():
        if filename not in _acquired:
            if not os.path.exists(filename):
                return []
            words = {word.lower() for word in open(filename).read().split("\n")}
            words -= set(exclude)
            _acquired[filename] = list(sorted(words))
        return list(_acquired[filename])

    return make


class WordGroup:
    """Deterministic word generator.

    Generates a sequence of words from common_words, and then from
    /usr/share/dict/words, if it exists. The sequence deterministically depends
    on the name of the group.
    """

    def __init__(self, name, sources):
        self.name = name
        self.hash = int(hashlib.md5(self.name.encode()).hexdigest(), base=16)
        self.words = []
        self.sources = list(reversed(sources))
        self.random = random.Random(self.hash)
        self.index = 0
        self.current = None

    def gen(self):
        """Generate the next word."""
        if not self.words:
            if not self.sources:
                self.words = []
            else:
                next_source = self.sources.pop()
                self.words = next_source()
                self.random.shuffle(self.words)
        if self.words:
            self.current = self.words.pop()
        else:
            self.index += 1
            self.current = str(self.index)
        return self.current

    def rgb(self):
        """Generate an RGB color string for this group."""
        # We generate the color in the YIQ space first because the Y component,
        # corresponding to brightness, is fairly accurate, so we can easily
        # restrict it to a range that looks decent on a white background, and
        # then convert to RGB with the standard colorsys package. The IQ
        # components control hue and have bizarre valid ranges.
        h = self.hash
        # 0.3 <= Y <= 0.6
        y = 0.3 + ((h & 0xFF) / 0xFF) * 0.4
        h >>= 16
        i = (((h & 0xFF) - 0x80) / 0x80) * 0.5957
        h >>= 16
        q = (((h & 0xFF) - 0x80) / 0x80) * 0.5226
        r, g, b = colorsys.yiq_to_rgb(y, i, q)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        return f"rgb({r}, {g}, {b})"


class Logword:
    """Tool to track progress through a program on stdout."""

    _groups = {}

    def __init__(
        self,
        watch=None,
        gen=True,
        nowatch_log=False,
        print_word=True,
        group="",
        logger=None,
        data=[],
    ):
        self.data = data if isinstance(data, (list, tuple)) else [data]
        if group not in Logword._groups:
            Logword._groups[group] = WordGroup(
                name=group,
                sources=[
                    common_words_source,
                    file_source("/usr/share/dict/words", exclude=common_words),
                ],
            )
        self.group = Logword._groups[group]
        self.watch = watch
        self.word = self.group.gen() if gen else self.group.current
        self.match = self.word is not None and self.watch == self.word
        self.active = self.match or (nowatch_log and self.watch is None)
        self.logger = logger
        if print_word:
            self.log(self, *self.data, force=self.watch is None)

    def breakpoint(self):
        if self.active:
            pdb.Pdb(skip=["breakword"]).set_trace()

    def log(self, *objs, force=False):
        if force or self.active:
            (self.logger or _log)(*objs)

    def __bool__(self):
        return self.active

    def __str__(self):
        gname = f"{self.group.name}:" if self.group.name else ""
        color = 30 + (self.group.hash % 8)
        return f"\033[1;{color};40m⏎ {gname}{self.word}\033[0m"

    def __hrepr__(self, H, hrepr):
        return H.div(
            f"⏎ {self.group.name}:{self.word}",
            style=f"color:{self.group.rgb()};font-weight:bold;",
        )

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass


def word(**kw):
    """Return the next word as a string."""
    return str(Logword(print_word=False, **kw))


def log(*data, **kw):
    """Prints out a word along with the given data."""
    return Logword(data=data, **kw)


def after(word=None, **kw):
    """True after log prints out the given word."""
    if word is None:
        word = os.environ.get("BREAKWORD")
    if word is not None and ":" in word:
        group, word = word.split(":")
        kw["group"] = group
    return Logword(watch=word, gen=False, print_word=False, **kw)


def brk(word=None, **kw):
    """Activate a breakpoint after log prints out the given word."""
    after(word, **kw).breakpoint()


def wordbrk(*args, **kwargs):
    """Generate word, brk, return word."""
    w = word(*args, **kwargs)
    brk(**kwargs)
    return w


def logbrk(*args, **kwargs):
    """Log and then brk."""
    log(*args, **kwargs)
    brk(**kwargs)
