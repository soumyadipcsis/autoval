## Project Autoval
A CLI Tool for automatically evaluating student code submissions

# Dependencies

## Docker:

Check out the following guides on for installation instructions on Ubuntu, MacOS and Windows:

Ubuntu: https://docs.docker.com/engine/install/ubuntu/

MacOS: https://docs.docker.com/docker-for-mac/

Windows: https://docs.docker.com/docker-for-windows/


## KLEE:

KLEE can be installed by many ways. For an extensive guide visit https://klee.github.io/getting-started/

We recommend using the KLEE images for Docker. For more info visit https://klee.github.io/docker/


## Python3:

Installing Python3 on your system is easy. For instructions visit https://www.python.org/downloads/ and choose your respective OS for a detailed guide


# Execution Instructions

1. Add the golden solution to the "golden_solution" directory
2. Add the student solutions to the "student_solutions" directory
3. In the "config.txt" file add input configurations. See below for details.
4. Give execute permission to "execute.sh". Run the following command: chmod +x execute.sh
5. Run "execute.sh" using the following command: ./execute.sh
6. Once the batch process finishes, hurrah! Now you can check the results compiled in the generated results.csv file.


# Input Configuration

Each line in the config.txt contains information about each input parameter (in strict order as per the order of functional arguments in the golden solution)

Each line starts with the parameter datatype, followed by a space and then the variable name followed by a semicolon.

Any input restrictions can be added following that, each separated by a semicolon.

For example,

If the variable name is "var" and the datatype in integer, and it should be in the range (0,100], then the corresponding line in the config.txt file should be the following:

int var;var>0;var<=100
