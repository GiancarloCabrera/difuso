import tkinter as tk
from tkinter import messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def centrar_ventana(root, ancho, alto):
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    root.geometry(f'{ancho}x{alto}+{x}+{y}')

root = tk.Tk()
root.title("Comida Recomendable")
centrar_ventana(root, 400, 300)

preferencias = ctrl.Antecedent(np.arange(0, 11, 1), 'preferencias')
tipo_comida = ctrl.Antecedent(np.arange(0, 11, 1), 'tipo_comida')
hambre = ctrl.Antecedent(np.arange(0, 11, 1), 'hambre')
comida = ctrl.Consequent(np.arange(0, 11, 1), 'comida')

preferencias['salado'] = fuzz.trimf(preferencias.universe, [0, 0, 5])
preferencias['dulce'] = fuzz.trimf(preferencias.universe, [0, 5, 10])
preferencias['picante'] = fuzz.trimf(preferencias.universe, [5, 10, 10])

tipo_comida['rápida'] = fuzz.trimf(tipo_comida.universe, [0, 0, 5])
tipo_comida['casera'] = fuzz.trimf(tipo_comida.universe, [0, 5, 10])
tipo_comida['gourmet'] = fuzz.trimf(tipo_comida.universe, [5, 10, 10])

hambre['ligera'] = fuzz.trimf(hambre.universe, [0, 0, 5])
hambre['moderada'] = fuzz.trimf(hambre.universe, [0, 5, 10])
hambre['intensa'] = fuzz.trimf(hambre.universe, [5, 10, 10])

comida['snack'] = fuzz.trimf(comida.universe, [0, 0, 5])
comida['plato_principal'] = fuzz.trimf(comida.universe, [0, 5, 10])
comida['banquete'] = fuzz.trimf(comida.universe, [5, 10, 10])

rule1 = ctrl.Rule(preferencias['salado'] & tipo_comida['rápida'] & hambre['ligera'], comida['snack'])
rule2 = ctrl.Rule(preferencias['dulce'] & tipo_comida['casera'] & hambre['moderada'], comida['plato_principal'])
rule3 = ctrl.Rule(preferencias['picante'] & tipo_comida['gourmet'] & hambre['intensa'], comida['banquete'])

rule4 = ctrl.Rule(preferencias['dulce'] & tipo_comida['rápida'] & hambre['intensa'], comida['plato_principal'])
rule5 = ctrl.Rule(preferencias['salado'] & tipo_comida['casera'] & hambre['moderada'], comida['plato_principal'])
rule6 = ctrl.Rule(preferencias['picante'] & tipo_comida['rápida'] & hambre['ligera'], comida['snack'])

controlador_comida = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
simulador = ctrl.ControlSystemSimulation(controlador_comida)

def mostrar_grafica():
    comida.view(sim=simulador)
    plt.show()

def calcular_comida():
    try:
        pref = float(entry_preferencias.get())
        tipo = float(entry_tipo_comida.get())
        hambre_valor = float(entry_hambre.get())
        
        simulador.input['preferencias'] = pref
        simulador.input['tipo_comida'] = tipo
        simulador.input['hambre'] = hambre_valor
        
        simulador.compute()
        
        if 'comida' in simulador.output:
            comida_recomendada = simulador.output['comida']
        else:
            messagebox.showwarning("Advertencia", "No se pudo calcular una comida para los valores dados. Intenta con diferentes entradas.")
            return
        
        if comida_recomendada <= 3.33:
            categoria = "snack"
        elif comida_recomendada <= 6.66:
            categoria = "plato principal"
        else:
            categoria = "banquete"
        
        messagebox.showinfo("Recomendación", f"La comida recomendada tiene una puntuación de: {comida_recomendada:.2f}\nCategoría de la comida: {categoria}")
        
        mostrar_grafica()
    
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores válidos para todas las entradas.")

label_preferencias = tk.Label(root, text="¿Cuánto prefieres la comida salada? (0 = nada, 10 = mucho):")
label_preferencias.pack(pady=10)
entry_preferencias = tk.Entry(root)
entry_preferencias.pack()

label_tipo_comida = tk.Label(root, text="¿Qué tan rápido prefieres que sea tu comida? (0 = rápida, 10 = gourmet):")
label_tipo_comida.pack(pady=10)
entry_tipo_comida = tk.Entry(root)
entry_tipo_comida.pack()

label_hambre = tk.Label(root, text="Nivel de hambre (0 = ligera, 10 = intensa):")
label_hambre.pack(pady=10)
entry_hambre = tk.Entry(root)
entry_hambre.pack()

btn_calcular = tk.Button(root, text="Calcular Comida", command=calcular_comida)
btn_calcular.pack(pady=20)

root.mainloop()
