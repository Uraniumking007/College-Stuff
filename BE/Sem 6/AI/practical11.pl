% दूरी (Distance between cities)
distance(a, b, 10).
distance(a, c, 15).
distance(a, d, 20).
distance(b, c, 35).
distance(b, d, 25).
distance(c, d, 30).

% Since graph is undirected
dist(X, Y, D) :- distance(X, Y, D).
dist(X, Y, D) :- distance(Y, X, D).

% Find all cities
cities([a, b, c, d]).

% Route cost calculation
path_cost([_], 0).
path_cost([City1, City2 | Rest], Cost) :-
    dist(City1, City2, C),
    path_cost([City2 | Rest], RestCost),
    Cost is C + RestCost.

% Add return to starting city
cycle_cost([Start | Rest], Cost) :-
    append([Start | Rest], [Start], Cycle),
    path_cost(Cycle, Cost).

% TSP Solution
tsp(BestPath, MinCost) :-
    cities(Cities),
    permutation(Cities, [Start | Rest]),
    cycle_cost([Start | Rest], _),
    findall(C-P,
        (
            permutation(Cities, P),
            P = [Start | _],
            cycle_cost(P, C)
        ),
        Results),
    min_member(MinCost-BestPath, Results).