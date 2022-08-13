# compr - flexible comparing and matching


## Rationale
_compr_ is a collection of wrappers (comparators) that enable flexible and complex comparing scenarios via simple code.

Comparators bind value(s) AND compare logic into single object.
Quite similar to what _pytest.approx(...)_ does.

Comparators redefine `__eq__`. The goal: exploit `==` to simplify underlying code (mainly by getting rid of extra if-else's later). Works well with assertions, filters, dispatchers etc.

Human readable `__repr__` is also available!


## Installation
```
pip install compr
```


## List available comparator functions
```
>>> import compr
>>> list(compr._COMPARATORS)
```


## Usage
We create comparators via functions in compr module:
```
>>> import copmr
>>> all_fives = compr.all_eq(5)  # all_fives matches any iteable filled with fives
>>> [5, 5, 6,] == all_fives
False
>>> (5 for _ in range(10)) == all_fives
True
```

The real profit comes by using comparators as arguments.
So underlying handlers can stay simple (check only `==`). While flexibility is achieved by providing different comparators when needed.

Please see examples (also the one with `kwargs2compr` demonstrates in-depth usage scenario).

> NOTE: These examples are intentionally synthetic for better illustration.

### Example 0. Basic assert (note the assert message):
```
# Assert actual value is greater than 5
>>> import compr
>>> expected = compr.gt(5)  # gt stands for greater than as in __gt__
>>> actual = 3
>>> assert expected == actual, f'{actual=} does not match {expected=}'
...
AssertionError: actual=3 does not match expected=gt(5)
```

### Example 1. Searhing list by condition:
```
# Find index of the first word starting with 't'
>>> from compr import startswith
>>> words = 'one', 'two', 'three', 'four'
>>> words.index(startswith('t'))
1
```

### Example 2: Validate HTTP response object attributes

Imagine requests-like `response` object:
```
>>> dir(response)
['status', 'headers', 'body', 'body_len'] # int, dict, str, int respectively
```

Without compr validator with parateters may look like:
```
>>> def validate(response, **kwargs):
>>>     """
>>>     Check if all given kwargs equal to response attributes
>>>     """
>>>     for k, v in kwargs.items():
>>>         if getattr(response, k) == v:
>>>             continue
>>>         else:
>>>             raise AssertionError(k, v)
```

Usage (check if status is 200 and body is 'asdf'):
```
>>> validate(response, status=200, body='asdf')
```

Now let's expand our requirements. We need to check if:
* body_len is between 300 and 400 bytes (inclusive)
* status code is < 206.

Pushing compare logic into validator above will eventually overwhelm it with complex
code, extra arguments or even magic.

Instead we may keep method above unchanged and use comparators:
```
>>> from compr import lt, within  # less-than, fits-range
>>> validate(response, status=lt(206), body_len=within(300, 400))
```

Now when `validate` tries to `==` status, it will actually check if its less-than 206.
Similarly with `==` body_len, it will check if it fits into range [300..400].

Profit!

Few more steps can make things prettier (introducing kwargs2compr):
```
>>> from compr import kwargs2compr
>>>
>>> def validate(response, **kwargs):
>>>     for k, v in kwargs2compr(kwargs):  # arg name parsing kicks in here
>>>     # allow kwargs to be interpreted as
>>>     # <attribute-name>_<comparator-func-name>=<comparator-func-argument>
>>>         if getattr(response, k) == v:
>>>             continue
>>>         else:
>>>             raise AssertionError(k, v)
```

And usage becomes:
```
>>> validate(response, status_lt=206, body_len_within=[300, 400])
```

After more refactoring (see `all_attrs` docstring for help):
```
>>> from compr import all_attrs
>>>
>>> def validate(response, **kwargs):
>>>         if not all_attrs(response, kwargs2compr(kwargs)):
>>>             raise AssertionError(response, kwargs)
```


## Creating Your own comparator object:
```
@compr.comparator
def almost_equal(actual, expected):
    return 0.9 * expected < actual < 1.1 * expected
```
