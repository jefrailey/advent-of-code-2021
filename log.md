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

# Day 05

20211205
start: 10:00
stop: 11:13

It took me an embarrassing amount of time to correctly produce points on the diagonal. I made a sequence of simple and avoidable errors, such as swapping the `+` and `*`, and I held onto a conceptual error, that the slope could be used to determine the sign of both the change in x and the change in y, for far too long. Had I slowed down and sketched some diagonal lines I suspect I would have caught these errors much sooner and cut my time in half.

# Day 06

20211206
start: 18:08
stop: 18:45

I used a Counter to map days to birth to a count of fish that will give birth in that many days, but a list would have worked as well. My initial implementation of the `advance_time()`, which iterated over the items in the school, that caused the test to fail at day 16. It was off by one, `20` instead of the expected `21`. I couldn't see the error in the amount of time I wanted to spend looking for it, so I re-wrote the implementation to iterate over a set range of days. That version passed. I have since tried to replicate my failing implementation and haven't been able to.

# Day 07

20211207
start: 17:45
submitted: 18:24
stopped: 18:39

My initial implementation relied on summing to get the fuel cost in part two. I'm surprised it solved part two within a "reasonable" amount of time (~15 seconds). At first, I thought the performance issue was in the `O(n^2)`, where `n` is the number of positions, used to determine which position minimized total fuel cost. I was not able to think of another model or a mathematical formula that would obviate checking every ending position. It took me several minutes after submitting the solution to remember that sums of a range could be calculated in constant time. That change reduced the running time to around 370ms.
