% AIM:
% Write a Prolog program to count even and odd elements from list and
% count elements up to specific index in list.

% count_even_odd(+List, -EvenCount, -OddCount)
count_even_odd([], 0, 0).
count_even_odd([H | T], EvenCount, OddCount) :-
    count_even_odd(T, E1, O1),
    (   0 is H mod 2
    ->  EvenCount is E1 + 1,
        OddCount is O1
    ;   EvenCount is E1,
        OddCount is O1 + 1
    ).

% count_upto_index(+List, +Index, -Count)
% Counts elements from start up to Index (1-based, inclusive).
count_upto_index(_, Index, 0) :-
    Index =< 0, !.
count_upto_index([], _, 0).
count_upto_index([_ | T], Index, Count) :-
    Index > 0,
    NextIndex is Index - 1,
    count_upto_index(T, NextIndex, RestCount),
    Count is RestCount + 1.

/*
Example Queries:

?- count_even_odd([1,2,3,4,5,6,7,8], E, O).
E = 4,
O = 4.

?- count_upto_index([10,20,30,40,50], 3, C).
C = 3.

?- count_upto_index([10,20,30,40,50], 10, C).
C = 5.
*/
