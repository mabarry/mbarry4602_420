This program "blocksworld.py" is run and compiled with Python3 in the command line using the following format:

                    python3 blocksworld.py probs/probX##.bwp

where X = A or B and ## = the number of the problem. For example, "probs/probB03.bwp" would run the program on the
file "probB03.bwp" located within the probs directory. Additionally, there are a couple of optional flags that
can be included when typing the command line argument. These include:

    -H HX: this flag specifies the heuristic that the A* search algorithm should run with, and can be any of the
     following: H0, H1, H2. The default heuristic used if none is specified is H2, as this is my best performing.
    
    -MAX_ITERS ####..#: this flag specifies the maximum number of iterations that the blocksworld program will tolerate before terminating. In my environment, I run it with either 100000 or 1000000, depending on how intensive or complex the problem is. The default number of iterations used if none is specified for this flag is 1,000,000.

An example of both flags being used at once is shown below, but it is important to note that either can be used on its own or in addition to the other:

                    python3 blocksworld.py probs/probB07.bwp -H H1 -MAX_ITERS 100000

In the above example, the program is being run with the H1 heuristic and a max iteration count of 100,000.