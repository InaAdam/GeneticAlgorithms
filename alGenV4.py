import numpy as np
from numpy import random as rnd, exp, e, sqrt, cos, pi
from binary_fractions import Binary
import copy
import sys

class Cromozom:
    def __init__(self, dp, lc, pc, pm):
        self.dimensiune_populatie = dp
        self.lungime_cromozom = lc
        self.lungime_gena = 15
        self.pc = pc
        self.pm = pm
        self.xMax = 5.14*2
        self.xMin = -5.14*2
        self.w = 10**(-3)
        return
    
    def populatie_initiala(self, codificare):
        eroare = 1
        if codificare == "codificare binara":
            eroare = 0
            self.populatie = np.empty((self.dimensiune_populatie, 
                                       self.lungime_cromozom),
                                      dtype='U%d' %(self.lungime_gena))
            for i in range(self.dimensiune_populatie):
                for j in range(self.lungime_cromozom):
                    individ = np.random.choice([0, 1],
                                               size = (self.lungime_gena,))
                    individ = ''.join((element) for 
                                    element in individ.astype(str))
                    self.populatie[i,j] = individ
        if codificare == "codificare reala":
            eroare = 0
            self.populatie = np.random.uniform(self.xMin,self.xMax,
                                               (self.dimensiune_populatie,
                                                self.lungime_cromozom))
        if eroare == 1:
            print("Codificare invalida")
            sys.exit()
    
    def realInBinar(self):
        self.populatie = (self.populatie - self.xMin)/(self.xMax - self.xMin)
        self.populatie = self.populatie.astype('U%d' %(self.lungime_gena+2))
        for i in range(self.dimensiune_populatie):
            for j in range(self.lungime_cromozom):
                temp = str(Binary(float(self.populatie[i,j])))
                temp = str(temp[0:self.lungime_gena+4]).replace("0b0.", "")
                self.populatie[i,j] = temp
        return self
    
    def BinarInReal(self):
        for i in range(self.dimensiune_populatie):
            for j in range(self.lungime_cromozom):
                suma = 0
                temp = self.populatie[i,j]
                for z in range(self.lungime_gena):
                   suma = suma + (int(temp[z])*2**(-(z+1)))
                self.populatie[i,j] = suma
        self.populatie = self.populatie.astype(float, casting='unsafe')
        self.populatie = self.populatie * (self.xMax - self.xMin) + self.xMin
        return self
    
    def spherFunction(self,X):
        return sum([x**2 for x in X])
    
    def rastriginFunction(self,X):
        return 10*self.lungime_cromozom+sum([(x**2-10*cos(2*pi*x)) for x in X])
    
    def ackleyFunction(self,X):
        for i in range(0,self.lungime_cromozom,2):
            p1 = -20*exp(-0.2*sqrt(0.5*(X[i]**2+X[i+1]**2)))
            p2 = exp(0.5*(cos(2*pi*X[i])+cos(2*pi*X[i+1])))
        return p1-p2+e+20
    
    def functia_de_evaluare(self, codificare, functie):
        eroare = 1
        self.fit = np.empty(self.dimensiune_populatie)
        if codificare == "codificare binara":
            temp_pop = copy.deepcopy(self)
            temp_pop = Cromozom.BinarInReal(temp_pop)
        else:
            temp_pop = copy.deepcopy(self)
        if functie == "sfera":
            eroare = 0
            for i in range(self.dimensiune_populatie):
                self.fit[i] = self.spherFunction(temp_pop.populatie[i])
        if functie == "rastrigin":
            eroare = 0
            for i in range(self.dimensiune_populatie):
                self.fit[i] = self.rastriginFunction(temp_pop.populatie[i])
        if functie == "ackley":
            eroare = 0
            for i in range(self.dimensiune_populatie):
                self.fit[i] = self.ackleyFunction(temp_pop.populatie[i])
        if eroare == 1:
            print("Functie de evaluare invalida")
            sys.exit()
    
    def sortare_populatie(self):
        #sortare cromozomi in functie de scor
        sort_idx = np.argsort(self.fit)
        self.fit = self.fit[sort_idx]
        self.populatie = self.populatie[sort_idx]
    
    def selectie(self, metoda):
        eroare = 1
        populatie_noua = copy.deepcopy(self.populatie)
        if metoda == "selectie proportionala":
            eroare = 0
            scor_temporar = np.max(self.fit) - self.fit
            index = np.arange(self.dimensiune_populatie)
            if sum(scor_temporar) == 0:
                probabilitate_selectie = self.fit/sum(self.fit)
            else:
                probabilitate_selectie = scor_temporar/sum(scor_temporar)
            for i in range(self.dimensiune_populatie):   
                idx = np.random.choice(index,p = probabilitate_selectie)
                populatie_noua[i] = self.populatie[idx]
        if metoda == "selectie prin concurs":
            eroare = 0
            for i in range(self.dimensiune_populatie):
                idx = [rnd.randint(0, self.dimensiune_populatie-1) 
                       for i in range(2)]
                if self.fit[idx[0]] < self.fit[idx[1]]:
                    populatie_noua[i] = self.populatie[idx[0]]
                else:
                    populatie_noua[i] = self.populatie[idx[1]]
        if metoda == "selectie prin etichetare":
            eroare = 0
            index = np.arange(self.dimensiune_populatie)
            sort_idx = np.argsort(self.fit)[::-1]
            temp_pop = self.populatie[sort_idx]
            total = sum(index)
            probabilitate_selectie = index/total
            for i in range(self.dimensiune_populatie):   
                idx = np.random.choice(index,p = probabilitate_selectie)
                populatie_noua[i] = temp_pop[idx]
        self.populatie = populatie_noua
        if eroare == 1:
            print("Operator de selectie invalid")
            sys.exit()
    
    def incrucisare(self, metoda):
        eroare = 1
        populatie_noua = copy.deepcopy(self.populatie)
        '''codificare binara'''
        if metoda == "incrucisare cu m taieturi":
            eroare = 0
            for i in range(0,self.dimensiune_populatie-1,2):
                idx = np.random.choice(range(self.dimensiune_populatie), 2)
                rata = rnd.random()
                if rata<self.pc:
                    for j in range(self.lungime_cromozom):
                        gp1 = self.populatie[idx[0],j]
                        gp2 = self.populatie[idx[1],j]
                        nr_taieturi = rnd.randint(0,self.lungime_gena-1)
                        taieturi = np.random.choice(range(self.lungime_gena),
                                                    nr_taieturi, False)
                        taieturi = np.sort(taieturi)
                        taieturi = np.append(taieturi,self.lungime_gena)
                        gd1, gd2 = '',''
                        if nr_taieturi == 0:
                            gd1, gd2 = gp1, gp2
                        else:
                            for z in range(nr_taieturi+1):
                                if z%2 == 0:
                                    gd1 += gp1[len(gd1):taieturi[z]]
                                    gd2 += gp2[len(gd2):taieturi[z]]
                                else:
                                    gd1 += gp2[len(gd1):taieturi[z]]
                                    gd2 += gp1[len(gd2):taieturi[z]]
                        populatie_noua[i,j] = gd1
                        populatie_noua[i+1,j] = gd2
                else:
                    populatie_noua[i] = self.populatie[idx[0]]
                    populatie_noua[i+1] = self.populatie[idx[1]] 
        if metoda == "incrucisare uniforma":
            eroare = 0
            for i in range(0,self.dimensiune_populatie-1,2):
                idx = np.random.choice(range(self.dimensiune_populatie), 2)
                rata = rnd.random()
                if rata<self.pc:
                    for j in range(self.lungime_cromozom):
                        gp1 = self.populatie[idx[0],j] 
                        gp2 = self.populatie[idx[1],j]
                        gd1, gd2 = '',''
                        for z in range(self.lungime_gena):
                            rata = rnd.random()
                            if rata > 0.5:
                                gd1 += gp1[z]
                            else:
                                gd1 += gp2[z]
                        for z in range(self.lungime_gena):
                            rata = rnd.random()
                            if rata > 0.5:
                                gd2 += gp1[z]
                            else:
                                gd2 += gp2[z]
                        populatie_noua[i,j] = gd1
                        populatie_noua[i+1,j] = gd2
                else:
                    populatie_noua[i] = self.populatie[idx[0]]
                    populatie_noua[i+1] = self.populatie[idx[1]]     
        if metoda == "incrucisare cu 2 taieturi":
            eroare = 0
            for i in range(0,self.dimensiune_populatie-1,2):
                idx = np.random.choice(range(self.dimensiune_populatie), 2)
                rata = rnd.random()
                if rata<self.pc:
                    for j in range(self.lungime_cromozom):
                        gp1 = self.populatie[idx[0],j] 
                        gp2 = self.populatie[idx[1],j]
                        gd1, gd2 = '',''
                        gd1 = gp1[0:6]+gp2[6:11]+gp1[11:15]
                        gd2 = gp2[0:6]+gp1[6:11]+gp2[11:15]
                    populatie_noua[i,j] = gd1
                    populatie_noua[i+1,j] = gd2
        '''codificare reala'''
        if metoda == "incrucisare discreta":
            eroare = 0
            for i in range(0,self.dimensiune_populatie-1,2):
                idx = [rnd.randint(0, self.dimensiune_populatie-1) 
                       for i in range(2)]
                for j in range(self.lungime_cromozom):
                    rata = rnd.random()
                    if rata>0.5:
                        populatie_noua[i,j] = self.populatie[idx[0],j]
                        populatie_noua[i+1,j] = self.populatie[idx[1],j]
                    else:
                        populatie_noua[i,j] = self.populatie[idx[1],j]
                        populatie_noua[i+1,j] = self.populatie[idx[0],j]
        if metoda == "incrucisare continua":
            eroare = 0
            for i in range(0,self.dimensiune_populatie-1,2):
                idx = [rnd.randint(0, self.dimensiune_populatie-1) 
                       for i in range(2)]
                rata = rnd.random()
                if rata<self.pc:
                    for j in range(self.lungime_cromozom):
                        rata = rnd.random()
                        if rata>0.5:
                            populatie_noua[i,j]=(self.populatie[idx[0],j]+
                                                 self.populatie[idx[1],j])/2
                            populatie_noua[i+1,j]=(self.populatie[idx[0],j]+
                                                   self.populatie[idx[1],j])/2
                        else:
                            populatie_noua[i,j] = self.populatie[idx[0],j]
                            populatie_noua[i+1,j] = self.populatie[idx[1],j]
                else:
                    populatie_noua[i] = self.populatie[idx[0]]
                    populatie_noua[i+1] = self.populatie[idx[1]]
        if metoda == "incrucisare convexa":
            eroare = 0
            alpha = 0.5
            for i in range(0,self.dimensiune_populatie-1,2):
                idx = [rnd.randint(0, self.dimensiune_populatie-1) 
                       for i in range(2)]
                rata = rnd.random()
                if rata<self.pc:
                    p1, p2 = self.populatie[idx[0]], self.populatie[idx[1]]
                    populatie_noua[i] = alpha*p1+(1-alpha)*p2
                    populatie_noua[i+1] = alpha*p2+(1-alpha)*p1
                else:
                    populatie_noua[i] = self.populatie[idx[0]]
                    populatie_noua[i+1] = self.populatie[idx[1]]
        self.populatie = populatie_noua
        if eroare == 1:
            print("Operator de incrucisare invalid")
            sys.exit()
    
    def mutatie(self, metoda, T,t):
        eroare = 1
        '''codificare binara'''
        if metoda == "mutatie uniforma puternica cb":
            eroare = 0
            for i in range(self.dimensiune_populatie):
                for j in range(self.lungime_cromozom):
                    gena_parinte = self.populatie[i,j]
                    gena_desc = ''
                    for z in range(self.lungime_gena):
                        rata = rnd.random()
                        if rata < self.pm:
                            gena_desc += str(1 - int(gena_parinte[z]))
                        else:
                            gena_desc += gena_parinte[z]
                    self.populatie[i,j] = gena_desc
        if metoda == "mutatie uniforma slaba cb":
            eroare = 0
            for i in range(self.dimensiune_populatie):
                for j in range(self.lungime_cromozom):
                    gena_parinte = self.populatie[i,j]
                    gena_desc = ''
                    for z in range(self.lungime_gena):
                        rata = rnd.random()
                        if rata < self.pm:
                            s = np.random.choice([0,1])
                            if s > 0.5:
                                gena_desc += '1'
                            else:
                                gena_desc += '0'
                        else:
                            gena_desc += gena_parinte[z]
                    self.populatie[i,j] = gena_desc
        if metoda == "mutatie neuniforma cb":
            eroare = 0
            self.pm = 1/(2+(self.lungime_cromozom-2)/T*t)
            for i in range(self.dimensiune_populatie):
                for j in range(self.lungime_cromozom):
                    gena_parinte = self.populatie[i,j]
                    gena_desc = ''
                    for z in range(self.lungime_gena):
                        rata = rnd.random()
                        if rata < self.pm:
                            gena_desc += str(1 - int(gena_parinte[z]))
                        else:
                            gena_desc += gena_parinte[z]
                    self.populatie[i,j] = gena_desc
        '''codificare reala'''
        if metoda == "mutatie uniforma cr":
            eroare = 0
            for i in range(self.dimensiune_populatie):
                rata = rnd.random()
                if rata < self.pm:
                    idx = np.random.choice(range(self.lungime_cromozom))
                    self.populatie[i,idx] = rnd.uniform(self.xMin,self.xMax)
        if metoda == "mutatie neuniforma cr":
            eroare = 0
            for i in range(self.dimensiune_populatie):
                rata = rnd.random()
                if rata < self.pm:
                    idx = np.random.choice(range(self.lungime_cromozom))
                    p = rnd.choice([-1,1])
                    temp = self.populatie[i,idx]
                    if p > 0:
                        temp += (self.xMax-temp)*(1-pow(self.pm,1-t/T))
                    else:
                        temp -= (temp-self.xMin)*(1-pow(self.pm,1-t/T))
                    self.populatie[i,idx] = temp
        if eroare == 1:
            print("Operator de muatatie invalid")
            sys.exit()
    
    def elitism(self):
        idx = np.argmin(self.fit)
        self.elita = self.populatie[idx]
        self.elita_fit = self.fit[idx]
    
    def adauga_elita(self):
        self.populatie[0] = self.elita
        self.fit[0] = self.elita_fit



#-------------testing-----------#

dp = 6
lc = 4
pc =0.8
pm=0.2
t=20
T=100
#pop = Cromozom(dp, lc, pc, pm)
codificare = "codificare reala"

#Cromozom.populatie_initiala(pop, codificare)
#print("populatia initiala\n", pop.populatie)
#Cromozom.functia_de_evaluare(pop,codificare,"rastrigin")
#print("scor: ",pop.fit)
#Cromozom.selectie(pop, "selectie prin concurs")
#print("populatia dupa selectie: \n",pop.populatie)
#Cromozom.functia_fitness(pop,"real")
#print("scor: ",pop.fit)

#Cromozom.incrucisare(pop, "Incrucisare cu m taieturi")
#print("populatia initiala\n", pop.populatie)

#Cromozom.mutatie(pop, 'Mutatie binara neuniforma',T,t)
#print('populatia dupa mutatie\n',pop.populatie)


