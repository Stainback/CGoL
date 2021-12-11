from main import *
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm


def update_graphic_field(w, h):
    global graphic_field
    global field_width
    global field_height
    graphic_field.destroy()
    field_width = min(1768, 30*w)
    field_height = min(992, 30*h)
    graphic_field = tk.Canvas(root, width=field_width, height=field_height, bg='white')
    graphic_field.grid(row=2, column=0, columnspan=7)
    graphic_field.bind("<Button-1>", change_cell_click)


def graphic_result_output(field):
    global cell_size
    graphic_field.delete('all')
    cell_size = min(field_width / len(field[0]), field_height / len(field))
    for row in range(len(field)):
        for col in range(len(field[0])):
            if field[row][col] == 0:
                graphic_field.create_rectangle(col * cell_size, row * cell_size,
                                               (col + 1) * cell_size, (row + 1) * cell_size,
                                               fill='white', outline='black', width=1)
            else:
                graphic_field.create_rectangle(col * cell_size, row * cell_size,
                                               (col + 1) * cell_size, (row + 1) * cell_size,
                                               fill='black', outline='black', width=3)


def gen_un():
    global universe
    if hUn.get() == 0 or wUn.get() == 0:
        tkm.showinfo("Error!", "None of universe sizes must be equal to zero")
    else:
        universe = generate_universe(hUn.get(), wUn.get())
    update_graphic_field(len(universe[0]), len(universe))
    graphic_result_output(universe)
    # "Save", "Change State" and "Next Gen" buttons must be disabled until universe generated
    button_CSCell['state'] = tk.NORMAL
    button_NextStep['state'] = tk.NORMAL
    button_Save['state'] = tk.NORMAL


def load_universe():
    global universe
    uf = tkf.askopenfilename()
    u_file = open(uf)
    u_data = u_file.read().split('-')
    if int(u_data[0]) == 0 or int(u_data[1]) == 0:
        tkm.showinfo("Error!", "None of universe sizes must be equal to zero")
    else:
        universe = generate_universe(int(u_data[0]), int(u_data[1]))
    update_graphic_field(len(universe[0]), len(universe))
    for row in range(len(universe)):
        for col in range(len(universe)):
            universe[row][col] = int(u_data[2][row*int(u_data[0])+col])
    graphic_result_output(universe)
    # "Save", "Change State" and "Next Gen" buttons must be disabled until universe generated
    button_CSCell['state'] = tk.NORMAL
    button_NextStep['state'] = tk.NORMAL
    button_Save['state'] = tk.NORMAL


def save_universe():
    sf = tkf.asksaveasfilename()
    u_file = open(sf, "w")
    # Save universe dimensions
    u_file.write(str(len(universe))+'-'+str(len(universe[0]))+'-')
    # Save cells state
    for row in range(len(universe)):
        for col in range(len(universe)):
            u_file.write(str(universe[row][col]))
    u_file.close()


def quit_app():
    save_universe()
    root.destroy()


def change_cell():
    if xC.get() == 0 or yC.get() == 0 or xC.get() > len(universe[0]) or yC.get() > len(universe):
        tkm.showinfo("Error!", "None of cell coordinates must be equal to zero")
    else:
        change_cell_state(universe, xC.get(), yC.get())
        graphic_result_output(universe)


def change_cell_click(event):
    change_cell_state(universe, int((event.x // cell_size)+1), int((event.y // cell_size)+1))
    graphic_result_output(universe)


def next_gen():
    field = calculate_new_gen(universe, calculate_cell_index(universe))
    for row in range(len(universe)):
        for col in range(len(universe[0])):
            universe[row][col] = field[row][col]
    graphic_result_output(universe)


# App interface
root = tk.Tk()
root.title("Conway's Game of Life")

graphic_field = tk.Canvas(root, width=600, height=600, bg='white')
graphic_field.grid(row=2, column=0, columnspan=7)

# Variables
hUn = tk.IntVar()
wUn = tk.IntVar()
xC = tk.IntVar()
yC = tk.IntVar()

# Spinboxes
hUniverse = tk.Spinbox(root, from_=0, textvariable=hUn, width=10)
hUniverse.grid(row=1, column=0)
wUniverse = tk.Spinbox(root, from_=0, textvariable=wUn, width=10)
wUniverse.grid(row=1, column=1)
xCell = tk.Spinbox(root, from_=0, textvariable=xC, width=10)
xCell.grid(row=1, column=3)
yCell = tk.Spinbox(root, from_=0, textvariable=yC, width=10)
yCell.grid(row=1, column=4)

# Buttons
button_GenUniverse = tk.Button(root, text="Generate Universe", command=gen_un)
button_GenUniverse.grid(row=0, column=0, columnspan=2)
button_Load = tk.Button(root, text="Load Universe", command=load_universe)
button_Load.grid(row=0, column=2)
button_Save = tk.Button(root, text="Save Universe", command=save_universe, state=tk.DISABLED)
button_Save.grid(row=1, column=2)
button_CSCell = tk.Button(root, text="Change state of a Cell", command=change_cell, state=tk.DISABLED)
button_CSCell.grid(row=0, column=3, columnspan=2)
button_NextStep = tk.Button(root, text="Calculate next step", command=next_gen, state=tk.DISABLED)
button_NextStep.grid(row=0, column=5)
button_Quit = tk.Button(root, text="Save and Quit", command=quit_app)
button_Quit.grid(row=0, column=6, rowspan=2)

root.mainloop()







