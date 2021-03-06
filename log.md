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

# Day 08

20211208
start: 17:10
stop: 17:54

20211209
start: 18:46
stop: 20:39

This one was a slog. I didn't think it was especially challenging--though the amount of time I took may suggest otherwise--but it required much more time than I expected. A small part of that was that most of the work I did on 20211208 was not helpful--I was more focused on my engagement at 18:00 than on understanding the problem domain. I solved the example "on paper" first. Generally, I think paper's the preferred tool for determining an algorithm to solve a logic puzzle, but since my initial paper solution worked, I'm wondering if, in this case, it was worth the extra time.

# Day 09

2021212
start: 9:15
stop: 10:31

The solution to part two could be improved a fair bit. Since every point on the heightmap that has a value less than 9 is in exactly one basin, it's not essential to find the minima first.

# Day 10

20211213
start 07:45
stop: 08:35

My initial implementation for part one tracked state using counters for each of the bracket pairs instead of a stack of opening brackets. That implementation did not work on the first attempt, so I immediately pivoted to the implementation that I knew would work. After further consideration, I do not think that counters alone can replace a stack as the order of opening brackets matters.

# Day 11

20211213
start: 12:28
stop: 13:46

The `OctopusMap` was a little clumsy to work with. An improvement would be to return `list[Octopus]` from the function that converts a `Grid` to `Octopus`es. It's also not necessary for `Octopus` to have access to a map--neighbors did not need to be a property. The converter could have determined each `Octopus`'s neighbors and set them. `Octopus` itself, is of course, unnecessary, but I found it easier to mentally model the solution as operating on octopuses instead of points on a plane.

# Day 12

20211213
start: 15:00
stop: 16:25

# Day 13

20211214
start 17:35
stop: 18:18

# Day 14

20211214
start: 18:22
stop: 19:39

An idea for improving performance enough to solve part two is to dynamically add insertion rules for sequences of elements longer than two as they appear.

20211215
start: 16:47
stop: 17:47

I first tried divide and concur, which was a slight improvement, but was still way too slow and, if storing intermediate steps, ran out of memory. After looking at the size of expected outcomes ("...the most common element is B (occurring 2192039569602 times)..."), I realized that maintaining any sort of contiguous representation in memory would be impossible. I next tried tracking counts of pairs. This seems to work, in so far as it completes in a reasonable amount of time, but the final counts are off due to double counting of characters that appear in two pairs, but only appear once in the polymer. E.g. in `NBN`, there are two pairs, `NB` and `BN`, with a total of two `B`s, but there's only one `B` in the final polymer. Simply halving the count seems wrong and produces the wrong answer. Despite that, I'm certain that representing the polymer as a map of pairs to counts is the correct approach. Maybe in addition to pairs, we need to track the counts of individual elements as the insertion occurs.

20211216
start: 16:24
stop: 16:31

Counting the letters as they were inserted was the key.

20211219
start: 09:09
stop: 09:32

Improved readability.

# Day 15

20211219
start: 10:12
stop: 11:52

20211219
start: 13:00
answer to part one: 13:15

My initial approach was to use Dijkstra's algorithm for finding the shortest path between two nodes. This worked correctly, but did not complete for the full problem size. This was a bit surprising because, from memory and from analyzing the algorithm, I thought the running time was bounded by `O(n^2)` where `n` is the number of nodes. I was fairly confident I had the algorithm correct, which turned out to be a mistake, so I moved on. My next approach was to iteratively generate a map of cumulative risk by adding the risk of the current coordinate to the minimum cumulative risk of its neighbors above and to the left. This completes and provides the correct answer for the 10 by 10 test, but currently provided an answer that was too high for the 100 by 100 problem. This is due to the incorrect assumption that the shortest path always advances by one step to the left or the right. While away from the problem, I was not able to think of a way to generate a cumulative risk map without constraints on the direction of dependence--after seeing that the second part of the problem increases the number of points 25 times, I suspect this may be possible and a way to solve part two with a reasonable amount of computation--and I suspected that I was correct about the running time of Dijkstra's algorithm and wrong about my implementation. I compared my implementation and the one on Wikipedia and discovered my error. My implementation was adding the neighbor node to the `queue.PriorityQueue` even if the projected cumulative risk for the current path through the neighbor was higher than a previously discovered path through that neighbor.

20211220
start: 17:39
stop: 18:47

Figuring out how to extend the risk map took way more time than it "should" have. I still think there's likely a linear algorithm to generate a minimum cumulative risk map, but I wasn't able to come up with it. The formatting of in `test_extend_map()` seems like a good reason to not use Black for formatting.

# Day 16

20211221
start: 19:08
stop: 19:12

20211222
start: 16:42
stop: 17:38

20211223
start: 09:40
stop: 10:45

20211224
start: 09:08
stop: 10:23

I found the problem description to be misleading. Left padding the binary representation with zeroes was mentioned in the context of literal value packets, "Literal value packets encode a single binary number. To do this, the binary number is padded with leading zeroes until its length is a multiple of four bits..." This lead me to attempt to left pad just the encoded literal value, i.e. the portion of a packet between the type id and the start of the next packet. Fortunately, I noticed one of the examples left padded the entire packet and not just the value portion of a literal value. Unfortunately, I did not notice that until after spending a lot of time trying to understand why my implementation did not work.

Similarly, one of the examples for solving part two, "04005AC33890 finds the product of 6 and 9, resulting in the value 54," appears to be wrong. `0x04005AC33890` is `0b1000000000001011010110000110011100010010000`, which has an outermost operator of sum, not product. Furthermore, attempting to interpret the parsed packet causes `max()` to throw a `ValueError` because the corresponding operator packet does not have children. My implementation returned the correct answer for part two, so I believe this is an issue with the example.
