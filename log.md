# Day 01

20211201
start: 20:24
stop: 21:06

Some of that time was spent setting up the project and thinking about ways to improve organization over previous years. I also spent some time looking for a builtin window function--I would have bet and lost money that itertools had one. I was likely thinking about [more-itertools](https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.chunked).

# Day 02

20211202
start: 18:32
stop: 18:55

I started by adding types and a parser for the instructions, but decided that it made the solution overly verbose.

# Day 03

20211203
start: 17:03
stop: 18:11

I misunderstood part two, which cost me a lot of time. Initially, I missed the step in the algorithm that recalculated the bit criteria after each filtering pass. This lead me to use the gamma and epsilon rating in an attempt to avoid recalculating the most and least common bits. This caused the oxygen generator rating to be off by one for test input, which lead me to search for a slight implementation error instead of an egregious one.

Moral of the story: Eat before, not after.
