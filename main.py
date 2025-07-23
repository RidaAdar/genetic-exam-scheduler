# importer les librairies et packages nécessaires
import os
from copy import deepcopy
import pandas as pd
import random
from copy import deepcopy
# importer les classes et les fonctions
from classes import Student
from classes import Teacher
from classes import Schedule
from classes import gene
from functions import Algorithm









def main():
    
    teacher_directory = r"C:\Users\Nesrine\Downloads\Data Cluster Projet Math-app\Profs"# Emplacement du Dossier Profs
    student_directory = r"C:\Users\Nesrine\Downloads\Data Cluster Projet Math-app\Students" # Emplacement du Dossier Students
    pop_size = random.randint(50,75)  # la taille de la population initiale
    stop_generation = random.randint(100,200)  # Condition d'arret: Le nombre di'itérations de notre algorithme génétique
    student_coeff = 1# Pénalité des faibles contraintes
    teacher_coeff = random.randint(10,100) # Pénalité des fortes contraintes
    crossover_rate = 1 #Taux de Croisement
    mutation_rate = random.uniform(0.2,0.5) #Taux de Mutation
    print("Les paramètres de l'algorithme")
    print('Taille de la population: {}'.format(pop_size))
    print('Maximum de générations: {}'.format(stop_generation))
    print('Taux de Croisement: {}'.format(crossover_rate))
    print('Taux de mutation {}'.format(mutation_rate))
    print('Pénalité des fortes contraintes: {}'.format(teacher_coeff))
    print('Pénalité des faibles contraintes: {}'.format(student_coeff))
    # éxécution de l'algorithme génétique
    res = Algorithm(pop_size, stop_generation, crossover_rate, mutation_rate,teacher_directory,student_directory,student_coeff,teacher_coeff) # La meilleure solution trouvée
    print(res)
   

   
if __name__ == "__main__":
         main()
            





            







