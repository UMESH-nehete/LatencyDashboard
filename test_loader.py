from utils.loader import *

folder = "/home/keerthana/Desktop/serverLogs"

experiments = load_experiment(folder)

print()

print("Number of experiments")

print(len(experiments))

print()

table = experiment_table(experiments)

print(table.head())