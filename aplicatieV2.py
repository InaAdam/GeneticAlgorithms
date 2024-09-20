import tkinter as tk
from alGenV4 import Cromozom
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

#declaram fereastra aplicatie
frame = tk.Tk(className=(" Algoritm Genetic"))
frame_width = 1000
frame_height = 510

#determinam valorile de pozitionare a ferestrei pe ecran
x_left = int(frame.winfo_screenwidth()/2 - frame_width/2)
y_top = int(frame.winfo_screenheight()/2 - frame_height/1.7)

#setam dimensiunile si pozitia ferestrei
frame.geometry("{}x{}+{}+{}".format(frame_width, frame_height,x_left, y_top))
frame.configure(background = 'white')
frame.resizable(False,False)

dd = tk.Frame(frame, width=200, height=400, bg='white')
dd.pack(side='left', fill='both', expand=True)

#setam partea stanga unde vor fi plasate variabelele
lf_color = 'pink'
lf_font = ("Ariel", 9)
left_frame = tk.Frame(dd, width=200, height=400, bg=lf_color)
left_frame.pack(side='left', fill='both', expand=True)
left_frame.pack_propagate(False)

#setama partea unde va fi afisat graficul 
right_frame = tk.Frame(dd, width=600, height=400, bg='white')
right_frame.pack(side='right', fill='both', expand=True)


comp_frame = tk.Frame(frame, width=200, height=400, bg='pink')
comp_frame.pack(side='right', fill='both', expand=True)


####dimensiunie populatie####
#mesaj
dim_pop_msg = tk.Label(left_frame, text="Dimensiune populatie",width = '200', 
                       bg= lf_color, font=lf_font)
dim_pop_msg.pack()
#valoare
dim_pop_val = tk.IntVar()
dim_pop_btn = tk.Scale(left_frame, variable = dim_pop_val, from_=5, to=200, 
                       orient='horizontal', length = '200',resolution=5)
dim_pop_btn.set(35)
dim_pop_btn.pack()

####numarul de generatii####
#mesaj
nr_gen_msg = tk.Label(left_frame, text="Numar generatii",width = '200', 
                       bg= lf_color, font=lf_font)
nr_gen_msg.pack()
#valoare
nr_gen_val = tk.IntVar()
nr_gen_btn = tk.Scale(left_frame, variable = nr_gen_val, from_=10, to=1000, 
                       orient='horizontal', length = '200',resolution=10)
nr_gen_btn.set(250)
nr_gen_btn.pack()

#generatia curenta
gen_cur = tk.Label(left_frame, text="Generatia curenta: 0",width = '200', 
                       bg= lf_color, font=lf_font)
gen_cur.pack()

####lungime cromozom###
#mesaj
lg_crom_msg = tk.Label(left_frame, text="Lungime cromozom",width = '200', 
                       bg= lf_color, font=lf_font)
lg_crom_msg.pack()
#valoare
lg_crom_val = tk.IntVar()
lg_crom_btn = tk.Scale(left_frame, variable = lg_crom_val, from_=2, to=20,
                       resolution=2,orient='horizontal', length = '200')
lg_crom_btn.pack()

lista_incrucisare = ['incrucisare cu m taieturi', 'incrucisare uniforma']
lista_mutatie = ['mutatie uniforma puternica cb', 'mutatie uniforma slaba cb',
                 'mutatie neuniforma cb']
def changeOpVar(val):
    global lista_incrucisare, lista_mutatie
    if val == 'codificare binara':
        lista_incrucisare = ['incrucisare cu m taieturi', 'incrucisare uniforma']
        lista_mutatie = ['mutatie uniforma puternica cb', 
                         'mutatie uniforma slaba cb', 'mutatie neuniforma cb']
        menu = incrucisare["menu"]
        menu.delete(0, "end")
        for string in lista_incrucisare:
            menu.add_command(label=string, 
                             command=lambda value=string:
                                  tip_incrucisare.set(value))
        tip_incrucisare.set(lista_incrucisare[0])
        menu = mutatie["menu"]
        menu.delete(0, "end")
        for string in lista_mutatie:
            menu.add_command(label=string, 
                             command=lambda value=string:
                                  tip_mutatie.set(value))
        tip_mutatie.set(lista_mutatie[0])
    if val == 'codificare reala':
        lista_incrucisare = ['incrucisare discreta', 'incrucisare continua',
                             'incrucisare convexa']
        menu = incrucisare["menu"]
        menu.delete(0, "end")
        for string in lista_incrucisare:
            menu.add_command(label=string, 
                             command=lambda value=string:
                                  tip_incrucisare.set(value))
        tip_incrucisare.set(lista_incrucisare[0])
        lista_mutatie = ['mutatie uniforma cr', 'mutatie neuniforma cr']
        menu = mutatie["menu"]
        menu.delete(0, "end")
        for string in lista_mutatie:
            menu.add_command(label=string, 
                             command=lambda value=string:
                                  tip_mutatie.set(value))
        tip_mutatie.set(lista_mutatie[0])

####codificare####
lista_codificare = ['codificare binara', 'codificare reala']
tip_codificare = tk.StringVar(left_frame,lista_codificare[0])
select = tk.OptionMenu(left_frame, tip_codificare, *lista_codificare,
                       command = changeOpVar)
select.config(width = '200')
select.pack()

####selectie####
lista_selectie = ['selectie proportionala', 'selectie prin concurs',
                  'selectie prin etichetare']
tip_selectie = tk.StringVar(left_frame, lista_selectie[0])
selectie = tk.OptionMenu(left_frame, tip_selectie, *lista_selectie)
selectie.config(width = '200')
selectie.pack()

####operatorii de variatie####
#incrucisare
tip_incrucisare = tk.StringVar(left_frame, lista_incrucisare[0])
incrucisare = tk.OptionMenu(left_frame, tip_incrucisare, *lista_incrucisare)
incrucisare.config(width = '200')
incrucisare.pack()

pc = tk.StringVar()
pc_btn = tk.Scale(left_frame, variable = pc, from_=0, to=1, resolution = 0.05,
                       orient='horizontal', length = '200')
pc_btn.set(1)
pc_btn.pack()

#mutatie
tip_mutatie = tk.StringVar(left_frame, lista_mutatie[0])
mutatie = tk.OptionMenu(left_frame, tip_mutatie, *lista_mutatie)
mutatie.config(width = '200')
mutatie.pack()

pm = tk.StringVar()
pm_btn = tk.Scale(left_frame, variable = pm, from_=0, to=1, resolution = 0.01,
                       orient='horizontal', length = '200')
pm_btn.set(0.2)
pm_btn.pack()

#functie
#mesaj
fct_msg = tk.Label(left_frame, text="Functie",width = '200', 
                       bg= lf_color, font=lf_font)
fct_msg.pack()
#valoare
lista_functii = ["rastrigin","ackley","sfera"]
tip_functie = tk.StringVar(left_frame, lista_functii[0])
functie = tk.OptionMenu(left_frame, tip_functie, *lista_functii)
functie.config(width = '200')
functie.pack()

def spher(*X):
    return sum([(x**2) for x in X])

def rastrigin(*X):
    return 10 + sum([(x**2 - 10 * np.cos(2 * np.pi * x)) for x in X])

def ackley(x,y):
    return -20.0*np.exp(-0.2*np.sqrt(0.5 * (x**2 + y**2))
                        )-np.exp(0.5 * (np.cos(2*np.pi*x)+np.cos(
                            2 * np.pi * y))) + np.e + 20
                     


def enable_cl():
    if comp_status.get():
        select_comp.config(state='active')
        iter_btn.config(state='active')
    else:
        select_comp.config(state='disabled')
        iter_btn.config(state='disabled')

comp_status = tk.IntVar()
comp = tk.Checkbutton(comp_frame, text='Comparare', width=200,
                      variable=comp_status, onvalue=1, offvalue=0, command=enable_cl)
comp.pack(pady=(10,0))

lista_comparare = ['operatorul de selectie', 'operatorul de incrucisare',
                  'operatorul de mutatie', 'presiunea de incrucisare',
                  'presiunea de mutatie']
tip_comp = tk.StringVar(comp_frame, lista_comparare[0])
select_comp = tk.OptionMenu(comp_frame, tip_comp, *lista_comparare)
select_comp.config(width = '200',state='disabled')
select_comp.pack()


####numarul de iteratii####
#mesaj
iter_msg = tk.Label(comp_frame, text="Numar iteratii",width = '200', 
                       bg= lf_color, font=lf_font)
iter_msg.pack()
#valoare
iter_val = tk.IntVar()
iter_btn = tk.Scale(comp_frame, variable = iter_val, from_=0, to=50, 
                       orient='horizontal', length = '200')
iter_btn.set(5)
iter_btn.config(state='disabled')

iter_btn.pack()

tip_comp_msg = tk.Label(comp_frame, text="",width = '200', 
                       bg= lf_color, font=lf_font)
tip_comp_msg.pack()

iter_cur_msg = tk.Label(comp_frame, text="Iteratia: 0",width = '200', 
                       bg= lf_color, font=lf_font)
iter_cur_msg.pack()


graf_msg = tk.Label(comp_frame, text="Salveaza grafic",width = '200', 
                       bg= lf_color, font=lf_font)
graf_msg.pack()

nume_imagine = tk.Entry(comp_frame,width=30)
nume_imagine.pack()

ruleaza = 1

def parcurge_generatii(populatia_curenta, crit):
    y_fit = []
    indx = 0
    if comp_status.get() == 0:
        for i in range(nr_gen_val.get()):
            if ruleaza == 0:
                break
            gen_cur.config(text = "Generatia curenta %d"%(i+1))
            gen_cur.update()
            Cromozom.elitism(populatia_curenta)
            Cromozom.selectie(populatia_curenta, tip_selectie.get())
            Cromozom.incrucisare(populatia_curenta, tip_incrucisare.get())
            Cromozom.mutatie(populatia_curenta, tip_mutatie.get(), 
                             nr_gen_val.get(),i)
            Cromozom.functia_de_evaluare(populatia_curenta,tip_codificare.get(),
                                         tip_functie.get())
            Cromozom.adauga_elita(populatia_curenta)
            y_fit.append(populatia_curenta.fit.min())
            indx = np.argmin(populatia_curenta.fit)
    else:
        for i in range(nr_gen_val.get()):
            if ruleaza == 0:
                break
            gen_cur.config(text = "Generatia curenta %d"%(i+1))
            gen_cur.update()
            Cromozom.elitism(populatia_curenta)
            if tip_comp == lista_comparare[0]:
                Cromozom.selectie(populatia_curenta, crit)
            else:
                Cromozom.selectie(populatia_curenta, tip_selectie.get())
            if tip_comp == lista_comparare[1]:
                Cromozom.incrucisare(populatia_curenta, crit)
            else:
                Cromozom.incrucisare(populatia_curenta, tip_incrucisare.get())
            if tip_comp == lista_comparare[2]:
                Cromozom.mutatie(populatia_curenta, crit, nr_gen_val.get(),i)
            else:
                Cromozom.mutatie(populatia_curenta, tip_mutatie.get(), 
                                 nr_gen_val.get(),i)
            Cromozom.functia_de_evaluare(populatia_curenta,tip_codificare.get(),
                                        tip_functie.get())
            Cromozom.adauga_elita(populatia_curenta)
            indx = np.argmin(populatia_curenta.fit)
            y_fit.append(populatia_curenta.fit[indx])
    return indx,y_fit

lista_pc = np.arange(0,1.01,0.05)
lista_pm = np.arange(0,1.01,0.05)


def main():
    global ruleaza
    ruleaza = 1
    for widget in right_frame.winfo_children():
        widget.destroy()
    if comp_status.get()==0:
        populatia_curenta = Cromozom(dim_pop_val.get(), lg_crom_val.get(),
                                     float(pc.get()),float(pm.get()))
        Cromozom.populatie_initiala(populatia_curenta, tip_codificare.get())
        Cromozom.functia_de_evaluare(populatia_curenta,tip_codificare.get(),
                                     tip_functie.get())
        idx_sol, fit_array = parcurge_generatii(populatia_curenta,0)
        
        if tip_codificare.get() == "codificare binara":
            populatia_curenta.BinarInReal()
        
        print(populatia_curenta.populatie[idx_sol])
        #definirea graficelor
        fig = Figure(figsize=(6, 6), dpi = 100)
        canvas = FigureCanvasTkAgg(fig, right_frame)  
        canvas.draw()
        
        ax = fig.subplots(2,1,gridspec_kw={'height_ratios': [2, 1]})
        x = np.linspace(-10.14, 10.14, 300)    
        y = np.linspace(-10.14, 10.14, 300)    
        X, Y = np.meshgrid(x, y)
        if tip_functie.get() == "rastrigin":
            Z = rastrigin(X, Y)
        if tip_functie.get() == "ackley":
            Z = ackley(X, Y)
        if tip_functie.get() == "sfera":
            Z = spher(X, Y)   
        ax[0].contourf(X,Y,Z,cmap="rainbow")
        xsol,ysol=[],[]
        for i in range(lg_crom_val.get()):
            if i%2 == 0:
                xsol.append(populatia_curenta.populatie[idx_sol,i])
            else:
                ysol.append(populatia_curenta.populatie[idx_sol,i])
        ax[0].scatter(xsol,ysol,color='red')
        ax[0].set_aspect(1)
        ax[0].plot(0,0,marker='+',color='black')
        
        ax[1].plot(fit_array, color = lf_color)
        ax[1].text(0.5,-0.4, str(populatia_curenta.fit[idx_sol]), 
                   size=8, ha="center", transform=ax[1].transAxes)
        
        canvas.get_tk_widget().pack()
    else:
        scor = []
        med = []
        iteratii = iter_val.get()
        tip = 0
        if tip_comp.get() == 'operatorul de selectie':
            criteriu = lista_selectie
        if tip_comp.get() == 'operatorul de incrucisare':
            criteriu = lista_incrucisare
        if tip_comp.get() == 'operatorul de mutatie':
            criteriu = lista_mutatie
        if tip_comp.get() == 'presiunea de incrucisare':
            criteriu = lista_pc
            tip=1
        if tip_comp.get() == 'presiunea de mutatie':
            criteriu = lista_pm
            tip=1
        if tip==1:
            for cc in criteriu:
                tip_comp_msg.config(text = cc)
                tip_comp_msg.update()
                for i in range(iteratii):
                    iter_cur_msg.config(text = 'iteratia %d'%(i+1))
                    iter_cur_msg.update()
                    if tip_comp.get() == 'presiunea de incrucisare':
                        populatia_curenta = Cromozom(dim_pop_val.get(), lg_crom_val.get(),
                                                 cc,float(pm.get()))
                    if tip_comp.get() == 'presiunea de mutatie':
                        populatia_curenta = Cromozom(dim_pop_val.get(), lg_crom_val.get(),
                                                 float(pc.get()),cc)
                    Cromozom.populatie_initiala(populatia_curenta, tip_codificare.get())
                    Cromozom.functia_de_evaluare(populatia_curenta,tip_codificare.get(),
                                                 tip_functie.get())
                    idx_sol, fit_array = parcurge_generatii(populatia_curenta,cc)
                    scor.append(populatia_curenta.fit[idx_sol])
                med.append(np.mean(scor))
            
            #plt.savefig('pm%s'%codf,dpi=200)
            
            #definirea graficelor
            fig = Figure(figsize=(6, 6), dpi = 100)
            canvas = FigureCanvasTkAgg(fig, right_frame)  
            canvas.draw()
            ax = fig.subplots()
            ax.plot(criteriu,med)
            ax.set(xlabel = tip_comp.get(),ylabel = "Scor")
            #ax.xaxis.set_ticks(criteriu)
            ax.set_title("Impactul presiunii de mutatie asupra scorului(%s)"
                         % tip_codificare.get(),
                      fontsize = 10)    
            canvas.get_tk_widget().pack()
        else:
            fig = Figure(figsize=(6, 6), dpi = 100)
            canvas = FigureCanvasTkAgg(fig, right_frame)  
            canvas.draw()
            ax = fig.subplots()
            textcc = 'Scor final:'
            med = {}
            for cc in criteriu:
                tip_comp_msg.config(text = cc)
                tip_comp_msg.update()
                scor=[]
                med[cc]=[]
                for i in range(iteratii):
                    iter_cur_msg.config(text = 'iteratia %d'%(i+1))
                    iter_cur_msg.update()
                    populatia_curenta = Cromozom(dim_pop_val.get(), lg_crom_val.get(),
                                                 float(pc.get()),float(pm.get()))
                    Cromozom.populatie_initiala(populatia_curenta, tip_codificare.get())
                    Cromozom.functia_de_evaluare(populatia_curenta,tip_codificare.get(),
                                                 tip_functie.get())
                    idx_sol, fit_array = parcurge_generatii(populatia_curenta,cc)
                    scor.append(fit_array)
                med[cc].append(np.mean(scor,axis=0))
                ax.plot(med[cc][-1], label = cc)
                textcc+='\n'+cc+": "+("{:.8f}".format(list(med.values())[-1][-1][-1]))
            ax.legend(loc = 'upper right')
            ax.set(xlabel = "Generatia",ylabel = "Scor")
            ax.set_title("Comparare %s(%s, functia %s)"%
                         (tip_comp.get(),tip_codificare.get(),tip_functie.get()),
                      fontsize = 10)
            ax.text(0.3,0.6,textcc,horizontalalignment='left',verticalalignment='center',
                     transform = ax.transAxes)
            if nume_imagine.get():
                fig.savefig('grafice\\'+nume_imagine.get()+".png",dpi=200)
            
            canvas.get_tk_widget().pack()
            #plt.savefig('incrucisaretestFunctia%s'%fun,dpi=200)



#buton afisare grafic
plot_button = tk.Button(comp_frame, width = 20,text = "Ruleaza",
                        command = main)
plot_button.pack(pady=15)

def stoploop():
    global ruleaza
    ruleaza = 0

stop_button = tk.Button(comp_frame, width = 20,text = "Stop",
                        command = stoploop)
stop_button.pack()
frame.mainloop()