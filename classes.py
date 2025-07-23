# importer les librairies et packagfes nécessaires
import os
from copy import deepcopy
import pandas as pd
import numpy as np
import random
from copy import deepcopy
# Définition de la classe Student/Etudiant
class Student:
    def __init__(self, name, courses):
        self.name = name  # le nom de l'étudiant
        self.courses = []
        self.courses.extend(courses) # liste des cours suivies par l'étudiant
        
    def __repr__(self):
        output =  self.name 
        return output
# Définition de la classe Teacher/Prof
class Teacher:
    def __init__(self, name, courses, avl):
        self.name = name  # le nom du prof
        self.courses = []
        self.courses.extend(courses) # liste des cours dont le prof est responsable
        self.avl = avl  # le tableau DataFrame contenant la disponibilité du prof
        
    def __repr__(self):
            output = "Name: " + self.name + "\t" + "Courses: " + str(self.courses)  + "\n"
            return output
# Définition de la classe Schedule/Emploi du temps


class Schedule:
    def __init__(self,fitness=0, sc = pd.DataFrame()):
       
        self.fitness=fitness # le fitness/score de l'emploi du temps
        self.sc = sc # le tableau DataFrame de l'emploi du temps
    
   
# Définition de la classe gene


class gene:
    def __init__(self,exam, day , time ):
       
        self.exam = exam  # le nom de l'examen
        self.day = day   # le jour de l'examen
        self.time = time  # l'heure de l'examen
    def __repr__(self):
        output =  self.exam
        return output
    def __eq__(self, other): 
        return self.exam == other.exam
    
