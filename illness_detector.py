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

    for i in range(len(symptoms)):
        symptoms[i] = symptoms[i].lower()

    query = list(prolog.query(f"illness(X), findall(S, symptom(X, S), L), intersection(L, {symptoms}, R),"
                              f" length(R, N)"))

    max_N = max([q['N'] for q in query])
    query = [illness for illness in query if illness['N'] == max_N]

    # query = "illness(X), {}.".format(", ".join([f"symptom(X, {symp.lower()})" for symp in symptoms]))
    # query = list(prolog.query(query))

    if len(query) == 0:
        return ['Unknown illness']
    if len(query) == 1:
        return [query[0]['X']]
    return [i['X'] for i in query]


################################################################################################
# STEP3: Define a function to ask yes/no questions about the remaining symptoms to decide on the illness

def ask_question(illnesses, symptoms):
    # Enabling YES and NO Button
    yes_button.config(state=tk.NORMAL)
    no_button.config(state=tk.NORMAL)
    
    # TODO: Define a function to diagnose illnesses based on user answers to yes/no questions

    remaining_symptoms = []

    if len(illnesses) == 0:
        illnesses = "Unknown illness"
    elif len(illnesses) != 1:
        for illness in illnesses:
            new_symptoms = list(prolog.query(f"findall(S, (symptom({illness}, S), not(member(S, {symptoms})),"
                                             f" not(member(S, {remaining_symptoms}))), L)"))
            for sym in new_symptoms[0]['L']:
                remaining_symptoms.append(str(sym))

    # if len(illnesses) == 0:
    #     illnesses = "Unknown illness"
    # elif len(illnesses) != 1:
    #   for illness in illnesses:
    #       new_symptoms = list(prolog.query(f"findall(S, symptom({illness}, S), L)"))
    #       for sym in new_symptoms[0]['L']:
    #           all_symptoms.add(str(sym))
    #
    #   remaining_symptoms = list(all_symptoms.difference(symptoms))

    # example of working with buttons
    if remaining_symptoms:
        question_symptom = remaining_symptoms.pop(0)
        question_label.config(text="Do you have {}?".format(question_symptom))
        yes_button.config(command=lambda: on_question_answer(question_symptom, True, illnesses, symptoms))
        no_button.config(command=lambda: on_question_answer(question_symptom, False, illnesses, symptoms))
    else:
        with open("diagnosed_illness.txt", "w") as f:
            f.write(", ".join(illnesses))
        root.destroy()


def on_question_answer(symptom, answer, illnesses, symptoms):
    # TODO: Define a function to handle the answer to yes/no question and
    #       to diagnose illnesses based on user answers to yes/no questions

    if answer:
        symptoms.append(symptom)
        illnesses = diagnose(symptoms)
        ask_question(illnesses, symptoms)
    else:
        illnesses = list(prolog.query("findall(X, symptom(X, {}), L), findall(Y, ({}), T), subtract(T, L, R)".format(
            symptom, ", ".join([f"symptom(Y, {symp.lower()})" for symp in symptoms]))))
        illnesses = [str(illness) for illness in illnesses[0]['R']]

        # # ANOTHER WAY
        # remove_illnesses = diagnose([symptom])
        # for illness in remove_illnesses:
        #     if illness in illnesses:
        #         illnesses.remove(illness)
        # # OR EVEN THIS WAY WE CAN SAY
        # # ---------------------------------------------
        # remove_illnesses = diagnose([symptom])
        # illnesses = list(prolog.query(f"subtract({illnesses}, {remove_illnesses}, L)"))
        # illnesses = [str(illness) for illness in illnesses[0]['L']]
        # # ---------------------------------------------

        ask_question(illnesses, symptoms)

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
        ask_question(illnesses, symptoms)


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
