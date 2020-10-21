
# breakword

`breakword` is a small debugging utility that combines print debugging with breakpoint debugging. It aims to facilitate debugging the kind of problem where you might use print statements to quickly spot where something seems to be off, and then switch to a step by step debugger.

`breakword` normally requires running your program twice and will only work properly if it is deterministic.


## How to use

1. Set the `PYTHONBREAKPOINT` environment variable to `breakword.breakpoint`.

2. Use `breakpoint` like a `print` statement:

```python
for i in range(10):
    breakpoint(i)
```

This will print out something like this:

```
$ python example.py
⏎ standard 0
⏎ sound 1
⏎ character 2
⏎ thank 3
⏎ play 4
⏎ however 5
⏎ fish 6
⏎ cultural 7
⏎ either 8
⏎ and 9
```

3. Use the `BREAKWORD` environment variable to set a breakpoint to what you want to investigate further. For instance, if you want to stop when `i == 6` in the above program, you can run the following command:


```
$ env BREAKWORD=fish python example.py
⏎ standard 0
⏎ sound 1
⏎ character 2
⏎ thank 3
⏎ play 4
⏎ however 5
⏎ fish 6
> example.py(2)<module>()
-> for i in range(10):
(Pdb) i
6
```

You can also give a comma-separated list of words, e.g. `BREAKWORD=sound,fish`.

**Note:** `breakpoint()` with no arguments retains the normal behavior.

![demo](https://raw.githubusercontent.com/breuleux/breakword/master/media/demo.png)


## More functions

* `breakword.log(*things, **config)`: Print a word and optionally other things after it.

* `breakword.brk(watch=None, **config)`: Sets a breakpoint to trigger after `log` printed out the given word. If `watch` is `None` or not given, the `BREAKWORD` environment variable is consulted. If the variable is not set, nothing will happen.
  * This is equivalent to `breakword.after(word).breakpoint()`.

* `breakword.after(watch=None, **config)`: Returns an object that evaluates to `True` right after `log` printed out the given watch word. As with `brk`, if `watch` is `None` or not given, the `BREAKWORD` environment variable is consulted.

* `breakword.word(**config)`: Returns the next word as a string. You can print it yourself, in which case it's basically like `log`, or you can store it in an object.

* `breakword.logbrk(**config)`: Calls `log` and then `brk`.

* `breakword.wordbrk(**config)`: Calls `word` and then `brk`. The word is returned.

* `breakword.set_default_logger(logger)`: Set the logging function to use (defaults to `print`)


## Tracking objects

* `breakword.track(obj, all=False)` will set the `breakword` attribute in the object to the next word in the list. By setting the `BREAKWORD` environment variable, you will set a breakpoint to the corresponding call to `track`. Set the `all` argument to `True` and the attribute will contain a list. Note: this will not work if `obj` is an integer or string, in those cases track will print a warning.

* `breakword.track_creation(*classes)` will set the `breakword` attribute on all instances of the given classes, when they are created. That way, you can set a breakpoint back to the creation of some object of interest.


## Groups

Use `breakword.groups.<name>` to get a "word group" with the given name. Each group generates words independently and will therefore not interfere with each other. They have `log`, `brk`, `after`, `word`, etc. as methods. The default group is `groups[""]`.


```python
from breakword import groups

assert groups.aardvark == groups["aardvark"]

# Log "a" in the aardvark group
groups.aardvark.log("a")

# Log "b" in the pelican group
groups.pelican.log("b")

# Get the next word in the pelican group
word = groups.pelican.word()

# Conditional behavior to perform only after the word "cherry"
if groups.pelican.after("cherry"):
    print("blah")
```
