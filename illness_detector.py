from pyswip import Prolog
import tkinter as tk
import re

################################################################################################
# STEP1: Define the knowledge base of illnesses and their symptoms

prolog = Prolog()

# TODO: read illnesses descriptions from illnesses.txt and add them to the prolog knowledge base

with open('illnesses.txt', 'r') as illness_file:
    for line in illness_file:
        data = re.split(' symptoms are |, and |, |\.', line)[:-1]
        illness, symptoms = data[0].lower(), data[1:]

        prolog.assertz(f"illness({illness})")
        for symp in symptoms:
            prolog.assertz(f"symptom({illness}, {symp.lower()})")

################################################################################################
# STEP2: Define a function to diagnose illnesses based on symptoms


def diagnose(symptoms):
    # TODO: Define this function to diagnose illnesses based on symptoms

    query = "illness(X), {}.".format(", ".join([f"symptom(X, {symp})" for symp in symptoms]))
    query = list(prolog.query(query))
    if len(query) == 0:
        return ['Unknown illness']
    if len(query) == 1:
        return [query[0]['X']]
    return query



################################################################################################
# STEP3: Define a function to ask yes/no questions about the remaining symptoms to decide on the illness

def ask_question(illnesses):
    # Enabling YES and NO Button
    yes_button.config(state=tk.NORMAL)
    no_button.config(state=tk.NORMAL)
    
    # TODO: Define a function to diagnose illnesses based on user answers to yes/no questions

    #example of working with buttons
    # if remaining_symptoms:
    #     question_symptom = remaining_symptoms.pop(0)
    #     question_label.config(text="Do you have {}?".format(question_symptom))
    #     yes_button.config(command=lambda: on_question_answer(question_symptom, True, illnesses))
    #     no_button.config(command=lambda: on_question_answer(question_symptom, False, illnesses))
    # else:
    #     with open("diagnosed_illness.txt", "w") as f:
    #         f.write(", ".join(illnesses))
    #     root.destroy()

    pass


def on_question_answer(symptom, answer, illnesses):
    # TODO: Define a function to handle the answer to yes/no question and
    #       to diagnose illnesses based on user answers to yes/no questions
    pass

################################################################################################
# The code is for GUI creation and functionality
# You don't need to directly change it


# "Next" button click event
def on_next_click():
    symptom = symptom_entry.get()
    if symptom:
        symptoms.append(symptom)
        symptom_entry.delete(0, tk.END)


# "Finish" button click event
def on_finish_click():
    illnesses = diagnose(symptoms)
    if len(illnesses) == 1:
        with open("diagnosed_illness.txt", "w") as f:
            f.write(illnesses[0])
        root.destroy()
    else:
        ask_question(illnesses)

# Create the GUI
root = tk.Tk()
root.title("Illness Diagnosis System")

# Create the symptom entry field
symptom_label = tk.Label(root, text="Enter a symptom:")
symptom_label.grid(row=0, column=0, padx=5, pady=5)
symptom_entry = tk.Entry(root)
symptom_entry.grid(row=0, column=1, padx=5, pady=5)

# Create the "Next" button
next_button = tk.Button(root, text="Next", command=on_next_click)
next_button.grid(row=1, column=0, padx=5, pady=5)

# Create the "Finish" button
finish_button = tk.Button(root, text="Finish", command=on_finish_click)
finish_button.grid(row=1, column=1, padx=5, pady=5)

# Create the question label
question_label = tk.Label(root, text="")
question_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Create the "Yes" button
yes_button = tk.Button(root, text="Yes")
yes_button.grid(row=3, column=0, padx=5, pady=5)

# Create the "No" button
no_button = tk.Button(root, text="No")
no_button.grid(row=3, column=1, padx=5, pady=5)

# Buttons are disabled at first
yes_button.config(state=tk.DISABLED)
no_button.config(state=tk.DISABLED)

# Initialize the symptoms list
symptoms = []

# Start the GUI
root.mainloop()
