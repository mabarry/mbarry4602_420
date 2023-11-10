This program uses the Davis-Putnam (DPLL) procedure to do logical inference on a few notable SAT problems.

To run this program, intall Python 3 and have a Linux environment ready on your computer. Then, open a terminal and type:

                    python3 DPLL.py <filename> <literal> [--UCH]

Here, <filename> represents the knowledge base (kb) converted to a file in Conjunctive Normal Form (cnf file) that DPLL.py will read in and perform operations with. <literal> is the optional literal that you can add to the command line, i.e "WAR", that will be appended to the read-in contents of the cnf file. Finally, the [--UCH] flag is an optional flag that determines whether or not the DPLL algorithm with use the Unit Clause Heuristic (UCH) when doing logical inferences and determining satisifiablity. By default, it is disabled. Do not include brackets around this flag when adding it via command-line. 