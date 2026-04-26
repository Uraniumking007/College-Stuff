% AIM: Develop an expert system for medical diagnosis of childhood diseases using Prolog.

:- dynamic yes/1, no/1.

% Entry point
start :-
    nl,
    write('--- Childhood Disease Expert System ---'), nl,
    write('Answer each question with y. or n.'), nl, nl,
    diagnose(Disease),
    nl,
    write('Possible diagnosis: '), write(Disease), nl,
    write('Note: This is a learning model, not medical advice.'), nl,
    undo.

% Disease diagnosis rules
diagnose(measles) :-
    symptom(fever),
    symptom(rash),
    symptom(runny_nose),
    symptom(red_eyes),
    symptom(cough), !.

diagnose(chickenpox) :-
    symptom(fever),
    symptom(itchy_rash),
    symptom(blisters),
    symptom(tiredness), !.

diagnose(mumps) :-
    symptom(fever),
    symptom(swollen_glands),
    symptom(headache),
    symptom(pain_while_swallowing), !.

diagnose(whooping_cough) :-
    symptom(severe_cough),
    symptom(whoop_sound),
    symptom(runny_nose),
    symptom(vomiting_after_cough), !.

diagnose(influenza) :-
    symptom(fever),
    symptom(cough),
    symptom(sore_throat),
    symptom(body_ache),
    symptom(tiredness), !.

diagnose(common_cold) :-
    symptom(runny_nose),
    symptom(sneezing),
    symptom(sore_throat),
    symptom(mild_fever), !.

diagnose(unknown_condition).

% Symptom checker with memory
symptom(Symptom) :-
    yes(Symptom), !.
symptom(Symptom) :-
    no(Symptom), !, fail.
symptom(Symptom) :-
    ask(Symptom).

ask(Symptom) :-
    write('Does the child have '),
    write(Symptom),
    write('? (y/n): '),
    read(Response),
    nl,
    (
        Response == y
        ->
        assertz(yes(Symptom))
        ;
        assertz(no(Symptom)),
        fail
    ).

% Clear stored answers after every run
undo :-
    retract(yes(_)),
    fail.
undo :-
    retract(no(_)),
    fail.
undo.
