% Simpsons Facts
parent(bart, homer).
parent(bart, marge).
parent(lisa, homer).
parent(lisa, marge).
parent(maggie, homer).
parent(maggie, marge).
parent(homer, abraham).
parent(herb, abraham).
parent(todd, ned).
parent(rod, ned).
parent(marge, jackie).
parent(patty, jackie).
parent(selma, jackie).

female(maggie).
female(lisa).
female(marge).
female(patty).
female(selma).
female(jackie).

male(bart).
male(homer).
male(herb).
male(burns).
male(smithers).
male(todd).
male(rod).
male(ned).
male(abraham).

% Occupation Facts
state(houston, texas).
state(pittsburgh, pennsylvania).
state(dallas, texas).
state(omaha, nebraska).
state(chicago, illinois).
state(college_station, texas).
state(los_angeles, california).
state(san_antonio, texas).

occupation(joe,oral_surgeon).
occupation(sam,patent_lawyer).
occupation(bill,trial_lawyer).
occupation(cindy,investment_banker).
occupation(joan,civil_lawyer).
occupation(len,plastic_surgeon).
occupation(lance,heart_surgeon).
occupation(frank,brain_surgeon).
occupation(charlie,plastic_surgeon).
occupation(lisa,oral_surgeon).

address(joe,houston).
address(sam,pittsburgh).
address(bill,dallas).
address(cindy,omaha).
address(joan,chicago).
address(len,college_station).
address(lance,los_angeles).
address(frank,dallas).
address(charlie,houston).
address(lisa,san_antonio).

salary(joe,50000).
salary(sam,150000).
salary(bill,200000).
salary(cindy,140000).
salary(joan,80000).
salary(len,70000).
salary(lance,650000).
salary(frank,85000).
salary(charlie,120000).
salary(lisa,190000).

% Teacher Facts
subject(algebra, math).
subject(calculus, math).
subject(dynamics, physics).
subject(electromagnetism, physics).
subject(nuclear, physics).
subject(organic, chemistry).
subject(inorganic, chemistry).

degree(bill, phd, chemistry).
degree(john, bs, math).
degree(chuck, ms, physics).
degree(susan, phd, math).

retired(bill).

% Octal Facts
bit(0).
bit(1).

% Map-coloring Facts
color(red).
color(green).
color(blue).

% Define the constraints
constraint(X, Y) :- color(X), color(Y), X \= Y.

% Rules
mapcolor(WA, NT, SA, Q, NSW, V, T) :-
    color(WA), color(NT), color(SA),
    color(Q), color(NSW), color(V),
    color(T),
    constraint(SA, WA),
    constraint(SA, NT),
    constraint(SA, Q),
    constraint(SA, NSW),
    constraint(SA, V),
    constraint(WA, NT),
    constraint(NT, Q),
    constraint(Q, NSW),
    constraint(NSW, V),
    format('WA = ~w, NT = ~w, SA = ~w, Q = ~w, NSW = ~w, V = ~w, T = ~w~n',
           [WA, NT, SA, Q, NSW, V, T]).

% ---------------

surgeon(X) :- occupation(X, oral_surgeon).
surgeon(X) :- occupation(X, plastic_surgeon).
surgeon(X) :- occupation(X, heart_surgeon).
surgeon(X) :- occupation(X, brain_surgeon).

lawyer(X) :- occupation(X, patent_lawyer).
lawyer(X) :- occupation(X, trial_lawyer).
lawyer(X) :- occupation(X, civil_lawyer).

lives_in_state(X, State) :- address(X, City), state(City, State).

earns_over(X, Amount) :- salary(X, Salary), Salary > Amount.

% ------------------

brother(X, Y) :- male(X), parent(X, P), parent(Y, P), X \= Y.
sister(X, Y) :- female(X), parent(X, P), parent(Y, P), X \= Y.

aunt(X, Y) :- female(Y), parent(X, P), sister(Y, P).
uncle(X, Y) :- male(Y), parent(X, P), brother(Y, P).

grandfather(X, Y) :- male(Y), parent(P, Y), parent(X, P).
granddaughter(X, Y) :- female(Y), parent(Y, P), parent(P, X).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

% -------------------

canTeach(X, Y) :- degree(X, phd, Z), subject(Y, Z).
canTeach2(X, Y) :- canTeach(X, Y), \+ retired(X).
canTeach3(X, Y) :- (degree(X, phd, Z) ; degree(X, ms, Z)), subject(Y, Z), \+ retired(X).

% -------------------

octal_code(A, B, C) :- bit(A), bit(B), bit(C), format('~w~w~w~n', [A, B, C]).

% -------------------

% Queries for 2
query2a(X) :- lawyer(X).
query2b(X) :- surgeon(X), lives_in_state(X, california).
query2c(X) :- surgeon(X), lives_in_state(X, texas), earns_over(X, 100000).