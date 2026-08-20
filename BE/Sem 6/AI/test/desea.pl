symptom(fever).
symptom(cough).
symptom(headache).

disease(flu):-
    symptom(fever),
    symptom(cough).

disease(migraine):-
    symptom(headache).

diagnosis :-
    disease(X),
    write('Disease is '),
    write(X).