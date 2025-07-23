# import librairies and packages
import os
from copy import deepcopy
import pandas as pd
import numpy as np
import random
from copy import deepcopy
from classes import Student
from classes import Teacher
from classes import Schedule
from classes import gene


def charge_data(teacher_directory,student_directory ):
    
    
    
    # charger les fichiers du dossier Profs
    student_files =  os.listdir(student_directory)
    # charger les fichiers du dossier Students
    teacher_files = os.listdir(teacher_directory)
    global no_days # Le nombre de jours
    global days_list # La liste des jours
    global teacher_list # La liste des profs
    global student_list # La liste des étudiants
    # Charger les données des profs 
    teacher_list= []
    teacher_time = pd.DataFrame() # Un dataFrame pour la disponibilité d'un prof
    dicto = {}
    index1 = 0
    while index1 < len(teacher_files):
        filename = teacher_files[index1] # nom du fichier contenant les données d'un professeur
        with open(os.path.join(teacher_directory, filename),encoding='utf-8') as f: # Ouvrir le fichier du prof
            
            teacher_name = os.path.splitext(os.path.basename(filename))[0] # Extraire le nom du prof
            lines = f.read().splitlines()
            lines = list(filter(None, lines))
            no_days = sum(c.isdigit() for c in lines[-1]) # extraction du nombre de jours 
            days_list = ['day'+str(i) for i in range(1, no_days+1) ] # Creation d'une liste de jours
            
            
            cc = (list(filter(lambda x:  all(i.isalpha() or i.isspace() for i in x), lines))) # extraction des cours dont le prof est responsable
            
            dicto[teacher_name] = [[int(num) for num in lines[-2].split()], [int(num) for num in lines[-1].split()]] 
            teacher_time = pd.DataFrame(dicto[teacher_name], index=['morning', 'noon'], columns = days_list )    # Ajouter la disponibilité du prof dans la Dataframe 0 : No Dispo et 0 : Dispo   
            new_teacher = Teacher(teacher_name, cc, teacher_time) # creation d'un objet de la classe Teacher
            teacher_list.append(new_teacher) # ajouter l'instance crée de la classe Teacher à la liste des profs
        index1+=1
        
    # Charger les données des étudiants
    student_list = [] # La liste des étudiants
    index2 = 0
    while index2 < len(student_files):
        filename = student_files[index2] # nom du fichier contenant les données d'un étudiant
        with open(os.path.join(student_directory, filename),encoding='utf-8') as f: # Ouvrir le fichier de l'étudiant
            
            student_name = os.path.splitext(os.path.basename(filename))[0] # extraire le nom de l'étudiant
           
            lines = f.read().splitlines()
            lines = list(filter(None, lines))
            
            cc = (list(filter(lambda x:  all(i.isalpha() or i.isspace() for i in x), lines))) # La liste des cours suivies par l'étudiant
            
            new_student = Student(student_name, cc) # Création d'une instance de la classe étudiant
            student_list.append(new_student) # Liste des étudiants
        index2+=1
    
    
        
    
    
    
    return student_list, teacher_list

# Charger tous les cours
def charge_courses(teacher_list):
    courses = [] 
    for teacher in teacher_list:
        courses.extend(teacher.courses)
    return courses
# Charger une Dataframe qui permet de donner les étudiants suivant un cours spécifique 
def charge_df_student(student_list):
    courses = charge_courses(teacher_list)
    data = [ [  [] for i in range(len(courses)) ] ]
    df_student = pd.DataFrame(data, columns = courses, index = ['Student'])
    for course in courses:
       for student in student_list:
          if course in student.courses:
            df_student[course]['Student'].append(student)
    return df_student
# Charger une Dataframe qui permet de donner les profs responsables d'un cours spécifique 
def charge_df_teacher(teacher_list):
    courses = charge_courses(teacher_list)
    df = pd.DataFrame(columns = courses, index = ['Teacher'])
    for teacher in teacher_list:
       for course in teacher.courses:
          df[course]['Teacher'] = teacher
    return df
# Génération d'un emploi du temps aléatoire
def random_schedule(teacher_list,student_coeff,teacher_coeff):
        df_teacher = pd.DataFrame(columns = courses, index = ['Teacher'])
        for teacher in teacher_list:
            for course in teacher.courses:
               df_teacher[course]['Teacher'] = teacher
        
        s = Schedule() # initialisation d'un emploi du temps vide
        exam_times = ['morning', 'noon'] # Les heures des examens morning = matin et noon = après-midi
        data = [ [ [] for i in range(len(exam_times))] for j in range(len(days_list)) ] # Une matrice de taille "nombre de jours * nombre de créneaux"
       
        schedule = pd.DataFrame(data) # transformer la matrice en dataframe qui sera notre tableau pour l'emploi du temps aléatoire
        schedule.index = days_list # les indices de la dataframe sont les jours(day1, day2 .....)
        schedule.columns = exam_times # les colonnes de l'emploi du temps sont les heures d'examen(morning ou noon)
        
        
        
        
        
        for course in courses:
            index1 = random.randint(0, len(days_list)-1)
            index2 = random.randint(0, 1)
            teacher = df_teacher[course]['Teacher']
            day = days_list[index1] # tirer un jour aléatoirement parmi la liste des jours
            time = exam_times[index2] # tirer une heure ou un créneau aléatoirement parmi les heures(morning ou noon)
            
            
            
                
            
            
            schedule[time][day].append(gene(course,day,time)) # création d'une instance gene(equivalent d'un examen) et l'ajouter à l'emploi du temps aux coordoonées (time, day)
        schedule['fitness']=0 # initialisert le fitness de l'emploi du temps
        
            
        s = Schedule( 0, schedule) # Créer une instance de la classe Schedule et ajouter le tableau qu'on a crée avant
        #s = evaluate_population(s,student_coeff,teacher_coeff)
                
        
        
        return s
def empty_schedule():
        s = Schedule()
        exam_times = ['morning', 'noon']
        data = [ [ [] for i in range(len(exam_times))] for j in range(len(days_list)) ]
       
        schedule = pd.DataFrame(data)
        schedule.index = days_list
        schedule.columns = exam_times
        schedule['fitness']=0
        s.sc=schedule
        
        
    
        return s
# Un prof ne doit pas avoir plus d'un examen en meme temps
def calculate_high_constraints1(schedule): 
    score = 0
    df_student = charge_df_student(student_list)
     
   # parcourir tous les créneaux horaires
    for day in days_list:
        
        for time in exam_times:
            
            list_profs = [] # liste des profs visitées 
            exams = schedule.sc[time][day] # extraire les examens programmées dans ce créneau horaire
            for course in exams:
                teacher = df_teacher[course.exam]['Teacher'] # identifier le prof responsable de ce cours
                if teacher not in list_profs:    # verifier si le prof n'existait pas dans la liste des profs déja visitées
                        list_profs.append(teacher)
                else: # le prof a un conflit deux cours en meme temps
                        
                        schedule.sc.at[day,'fitness']+= 1 # on compte un conflit de plus
                        score+=1        
    return score
# un prof ne doit pas avoir un examen programmée dans un créneau où il n'est pas disponible
def calculate_high_constraints2(schedule):
    score = 0
    df_student = charge_df_student(student_list)
    
       # parcourir tous les créneaux horaires
    for day in days_list:
        
        for time in exam_times:
            
            exams = schedule.sc[time][day]
            for course in exams:
                teacher = df_teacher[course.exam]['Teacher'] # identifier le prof responsable de ce cours
                if teacher.avl[day][time] == 0:  # valeur 0 signfie que le prof est absent pendant le créneau où l'examen a été programmée
                    score+=1 # on compte un conflit de plus
                    schedule.sc.at[day,'fitness'] += 1
    return score

# un étudiant ne dit pas avoir plus d'un examen en meme temps
def calculate_low_constraints(schedule): 
    score = 0
    df_student = charge_df_student(student_list)
    for day in days_list:
        
        for time in exam_times:

            list_students = []
            exams = schedule.sc[time][day]
            for course in exams:
                students = df_student[course.exam]['Student']
                for student in students:
                    if student not in list_students:
                        list_students.append(student)
                    else:
                        score += 1
               
    return score            


        
    
def generate_population(n, teacher_list,student_coeff,teacher_coeff):
    pop = []
    for i in range(n):
        sc = random_schedule(teacher_list,student_coeff,teacher_coeff)
        pop.append(sc)
    return pop

def evaluate_population(population,student_coeff,teacher_coeff): # evaluation de chaque individu de la population
    for schedule in population:
        schedule.sc['fitness'] = 0
        no_lc= calculate_low_constraints(schedule) #faibles contraintes 
        no_hc1= calculate_high_constraints2(schedule) # fortes contraintes
        no_hc2= calculate_high_constraints1(schedule)
        fitness = teacher_coeff*(no_hc1 + no_hc2) + student_coeff*no_lc # evaluation de l'individu en utilsant les pénalités 
        schedule.fitness = fitness
    return population

def selection(population):                                # la selection par roulette

    new_pop = []
    total_fitness = 0

    for schedule in population:
        total_fitness += schedule.fitness

    best1, best2 = get_best(population)  # ajouter les deux meilleurs solutions pour ne pas les perdre 
    new_pop.append(best1)
    new_pop.append(best2)
    fitness_sum = 0

    while len(new_pop) < len(population): # pour garder la meme taille de la population initiale

        index = random.randint(0, len(population)-1)   # choisir aléatoirement un individu dans la population
        fitness_sum += population[index].fitness
        if fitness_sum >= total_fitness:             # la probabilité selon lmaquelle un individu peut etre choisie            
            if population[index] not in new_pop:  # verifier si l'emploi du temps n'existait pas déja dans la population(éviter la repetition)
                new_pop.append(deepcopy(population[index]))

    return new_pop
def get_fitness(schedule): # obtenir le fitness d'un individu
    return schedule.fitness
def get_best(population): 
    copy_pop = deepcopy(population)
    copy_pop.sort(key=get_fitness, reverse=False)                      # ordonner dans l'ordre descendant
    return copy_pop[0], copy_pop[1]                                 #tirer les deux meilleurs elements qui ont un fitness minimal 
def selection_1(population): # algorithm_size < generation_size
    #Tournament pool
    fittest1, _ = get_best(population) # tirer le meilleur parent
    random_id =  random.randint(0, len(population)-1)
    fittest2 = population[random_id]

    
    return fittest1, fittest2

def generate_genes(sched):#generer des genes/exams d'un emploi du temps
        genes = [] # la liste des genes que contient cet individu
        # parcourir toutes les demies-journées
        for day in days_list:
            for time in exam_times:
                sched_sc = sched.sc[time][day]  # une demi-journée
                for i in range(0, len(sched_sc)):
                     #un module
                    new_gene = gene(sched_sc[i].exam,day, time)  # le gène i
                    #new_gene = gene[i]
                
                    genes.append(new_gene)
            
           
        return genes

# transformer une liste de gènes en un amploi du temps
def genes_to_schedule(genes): 
    sch = empty_schedule() # initialiser un emploi du temps vide pour le remplir avec les gènes de la liste
    for g in genes:
        sch.sc[g.time][g.day].append(g)  # utiliser les attrributes day et time pour savoir l'emplacement du gène dans l'emploi du temps
    sch.fitness = 0
    return sch
# le croisement uniforme
def crossover(sch1,sch2,student_coeff,teacher_coeff):
    genes1 = generate_genes(sch1) # generer  les genes du premier parent
    genes2 = generate_genes(sch2) # generer  les genes du deuxième parent
    
    
    new_genes1=[] # initialiser la liste où on va mettre les gènes des enfants crées par le croisement
    new_genes2=[]# initialiser la liste où on va mettre les gènes des enfants crées par le croisement
    uniform_rate = 0.5 # taux de croisement unifome est 0.5
    for i in range(len(genes1)):
       id = random.uniform(0,1) # generer un nombre décimal entre 0 et 1
       index = genes2.index(genes1[i]) # l'indice du gene qui été choisi pour l'echange
       if id < uniform_rate:  # echange du gene choisi entre les parents 1 et 2
         
            
             
            new_genes1.append(genes2[index]) # enfant1 prend le gène du parent2
            new_genes2.append(genes1[i]) # enfant2 prend le gène du parent
       else: # pâs d'échange de gènes
           new_genes2.append(genes2[index]) # enfant2 prend le gène du parent2
           new_genes1.append(genes1[i]) # enfant1 prend le gène du parent1
           
                 
               
                
              
              
            
    
    new_sch1 = genes_to_schedule(new_genes1) # transformer la liste de genes en un emploi du temps
    new_sch2 = genes_to_schedule(new_genes2) # transformer la liste de genes en un emploi du temps
    #new_sch1 = evaluate_population(new_sch1,student_coeff,teacher_coeff)
    #new_sch2 = evaluate_population(new_sch2,student_coeff,teacher_coeff)
    return new_sch1, new_sch2

def mutation(sched, mutation_rate,student_coeff,teacher_coeff):
    
    genes1 = []
    genes1 = generate_genes(sched) # generer les genes de l'individu qui  
    if random.uniform(0, 1) <= mutation_rate: # taux de mutation à respecter si oui on va muter l'individu sinon on le retourne sans mutation
        
        for g in genes1: # parcourir toues gènes de l'individu
          if random.randint(0, 100) <= 1/3 * 100: # pour éviter d'altèrer les bonnes solutions on va muter que le tiers des gènes de l'individu
            idx = genes1.index(g) # recuperer l'indice de ce gène dans la liste 
          
            
            
            exam  = g.exam # extraire le nom de l'examen
            
            index = random.randint(0,len(days_list)-1) # choisir aléatoirment un jour
            day  = days_list[index]
            index = random.randint(0,len(exam_times)-1) # choisir aléatoirment une demi-journée
            time  = exam_times[index]
            
            del genes1[idx] # supprimer l'ancien gene 
            genes1.append(gene(exam,day,time)) # ajouter le nouveau gene
            
        sched_result = genes_to_schedule(genes1) #  enfin apres l'ajout de tous les nouveaux genes on cree notre schedule
        #sched_result = evaluate_population(sched_result,student_coeff,teacher_coeff)
        return sched_result # retourner l'individu muté
    return sched    


def crossovering_population(population, crossover_rate,student_coeff,teacher_coeff):
        crossovered_population = []
        while len(crossovered_population) < len(population):
         
           parent_a, parent_b = selection_1(population)
           if random.uniform(0, 1) <= crossover_rate:
            
           
             child1, child2 = crossover(parent_a, parent_b,student_coeff,teacher_coeff)
          
             crossovered_population.append(deepcopy(child1))
             crossovered_population.append(deepcopy(child2)) 
           else:
             crossovered_population.append(parent_a)
             crossovered_population.append(parent_b)

        
         
         
           
          
        return crossovered_population
        
def mutating_population(population, mutation_rate,student_coeff,teacher_coeff):
    mutated_population = []
    for schedule in population:
        s = mutation(schedule, mutation_rate,student_coeff,teacher_coeff)
        mutated_population.append(s)
    return mutated_population


def Algorithm(generation_size, stop_generation,crossover_rate,mutation_rate,teacher_directory,student_directory,student_coeff,teacher_coeff):
    global courses
    global df_teacher
    global df_student
    global data
    global exam_times
    exam_times = ['morning', 'noon']
    student_list, teacher_list= charge_data(teacher_directory,student_directory)
    df_teacher = charge_df_teacher(teacher_list)
    df_student = charge_df_student(student_list)
    courses = charge_courses(teacher_list)
    data = [ [ [] for i in range(len(exam_times))] for j in range(len(days_list)) ] 
    population = [generate_population(generation_size,teacher_list,student_coeff,teacher_coeff)]
    evaluate_population(population[0],student_coeff,teacher_coeff)
   
    initial_solution, _ = get_best(population[0])
   

    for i in range(stop_generation):
        popu = population[0]
        parents = selection(deepcopy(popu))
        evaluate_population(parents,student_coeff,teacher_coeff)
        
        crossover_population = crossovering_population(parents, crossover_rate,student_coeff,teacher_coeff)
        evaluate_population(crossover_population,student_coeff,teacher_coeff)
        
        mutation_population = mutating_population(crossover_population, mutation_rate,student_coeff,teacher_coeff)
        evaluate_population(mutation_population,student_coeff,teacher_coeff)
        
        
        
        
        
        new_solution, _ = get_best(mutation_population)
        last_solution = deepcopy(new_solution)
        
        population.clear()

        population.append(mutation_population)

        
            
            

        print(i, "Le fitness de la solution initiale:", initial_solution.fitness, "\t le fitness de la nouelle solution: ",
              new_solution.fitness)

    return new_solution.sc

