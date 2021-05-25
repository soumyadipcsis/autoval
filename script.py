import os
import re
from os import listdir
from os.path import isfile, join
from posixpath import commonpath
import csv

# Get path for golden and student directories
golden_solution_path = os.getcwd() + "/golden_solution"
student_solutions_path = os.getcwd() + "/student_solutions"

# Get the golden solution filename
golden_solution_filenames = [f for f in listdir(golden_solution_path) if isfile(join(golden_solution_path, f))]
golden_solution_filenames.remove(".gitkeep")
golden_solution_filename = golden_solution_filenames[0]

# Get the student solutions filenames
student_solution_filenames = [f for f in listdir(student_solutions_path) if isfile(join(student_solutions_path, f))]
student_solution_filenames.remove(".gitkeep")

# Parse golden solution
golden_solution_file = open(golden_solution_path + "/" + golden_solution_filename,"r")
golden_code = golden_solution_file.read()

# Parse config file
config_file = open("config.txt","r")
config_file_lines = config_file.readlines()

# Build main method
main_method_file = open("main_method.c","a")
main_method_file.write("int main()\n{\n")
var_names = []
for line in config_file_lines:
    clauses = line.split(";")
    main_method_file.write("\t" + clauses[0] + ";\n")
    var_name = clauses[0].split()[1]
    var_names.append(var_name)
    main_method_file.write("\tklee_make_symbolic(&" + var_name + ",sizeof(" + var_name + "),\"" + var_name + "\");\n")
    if len(clauses) > 1:
        for i in range(1,len(clauses)):
            main_method_file.write("\tklee_assume(" + clauses[i].replace("\n","") + ");\n")


argument_list = ""
for var in var_names:
    argument_list = argument_list + var + ","
argument_list = argument_list[:-1]

main_method_file.write("\tprintf(\"%d\\n\",golden_solution(" + argument_list + ") == student_solution(" + argument_list + "));\n")
main_method_file.write("}\n")
main_method_file.close()

main_method_file = open("main_method.c","r")
main_method_code = main_method_file.read()

scores = {}

# Create the temporary combined file and execute
for x in student_solution_filenames:

    print("Running on " + x)    
    student_solution_file = open(student_solutions_path + "/" + x,"r")
    student_code = student_solution_file.read()
    
    temp_file = open("temp.c","a")
    temp_file.write("//Beginning of Golden Solution\n")
    temp_file.write(golden_code)
    temp_file.write("\n//End of Golden Solution\n")
    temp_file.write("//Beginning of Student Solution\n")
    temp_file.write(student_code)
    temp_file.write("\n//End of Student Solution\n\n\n\n\n")
    temp_file.write("//Beginning of main method\n")
    temp_file.write(main_method_code)
    temp_file.write("\n//End of main method\n\n\n\n\n")
    temp_file.close()
    
    command = "clang -emit-llvm -c temp.c"
    os.system(command)
    command = "klee --max-time=20s  --max-solver-time=20s temp.bc > temp_result.txt"
    os.system(command)
    
    file = open("temp_result.txt","r")
    contents = file.read().splitlines()
    score = 0
    for y in contents:
        if y != "":
            score = score + int(y.strip())
    if len(contents) != 0:
        score = int(score*100/len(contents))
    else:
        score = -1
    scores[x] = score
    file.close()
    
    os.system("rm temp.c\nrm temp.bc\nrm temp_result.txt\nrm -r klee-out-0")

os.system("rm main_method.c")

fields = ["Filename","Score(100)"]
rows = []
for x in scores:
    temp_row = []
    temp_row.append(str(x))
    temp_row.append(str(scores[x]))
    rows.append(temp_row)

csv_file = open("results.csv","w")
csvwriter = csv.writer(csv_file) 
csvwriter.writerow(fields) 
csvwriter.writerows(rows)
csv_file.close()