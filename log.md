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

# Day 04

20211204
start: 15:47
stop: 16:58

Representing the Bingo boards as a class with methods for marking drawn numbers and determining if they had won, was a gamble that paid off this time, but could have cost a lot (more) time if part two was wildly different. My primary mistakes were in the construction of columns--I unintentionally wrote `number % size` instead of `idx % size`, which made rearranged the column members and made the size of the columns inconsistent--and in parsing the input file--the parser added an empty board due to a missing conditional. Despite those mistakes, I think this should have taken much less than an hour. I'm not sure exactly where else the time went.

After review, there's a couple inefficiencies in this implementation. First, each board does not need to keep the draw history, it just needs to track the last number drawn. Second, the `has_won` property is unnecessary. `has_won` could have been an attribute that was set to `True` by `mark()` if a row or column was empty after removing the drawn number from it.
