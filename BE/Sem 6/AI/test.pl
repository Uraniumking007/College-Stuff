likes(bhavesh, pizza).
likes(bhavesh, coding).
likes(rahul, cricket).

friend(X, Y) :- likes(X, Z), likes(Y, Z).