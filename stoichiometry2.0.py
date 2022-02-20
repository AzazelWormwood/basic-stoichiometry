from tkinter import *
from tkinter.ttk import Combobox
import time
from selenium import webdriver

#conversion functions
def mass_for_x_mols(mols, molar_mass):
    mass_needed = mols * molar_mass
    answer.set('You need ' + str(round(mass_needed, 7)) + " grams.")

def mols_for_x_mass(mass, molar_mass):
    mols_needed = mass/molar_mass
    answer.set('You need ' + str(round(mols_needed,7)) + " moles.")

def mass_for_x_molarity(molarity, volume, molar_mass):
    mols_needed = molarity * (volume/1000)
    mass_needed = mols_needed * molar_mass
    answer.set('You need ' + str(round(mass_needed,7)) + " grams.")

def molarity_for_x_mass(mass, volume, molar_mass):
    mols_needed = mass/molar_mass
    molarity = mols_needed / (volume/1000)
    answer.set('The molarity is ' + str(round(molarity,7)) + ' M')

def volume_for_x_mass(volume, density):
    mass = volume * density
    answer.set('The mass is ' +str(round(mass,7))+ ' grams.')

def mass_for_x_volume(mass, density):
    volume = mass / density
    answer.set('The volume is ' +str(round(volume,7))+ ' mL.')

#dictionaries to organize functions
mass_functions = {'Moles(mols)': mass_for_x_mols, 'Molarity(M)': mass_for_x_molarity, 'Volume(mL)': mass_for_x_volume}
mols_functions = {'Mass(g)': mols_for_x_mass}
molarity_functions = {'Mass(g)': molarity_for_x_mass}
volume_functions = {'Mass(g)': volume_for_x_mass}



x = 0
stored_molecule = ''
MW = 0
def solve(self):
    #all this mucking about with global variables and stored molecules is so the program checks if it already has the values for the input molecule stored
    #if it does it doesn't open a browser session which drastically cuts runtime
    #probably a more efficient way of doing this but I don't know it right now
    global MW
    global x
    global stored_molecule
    x += 1

    if x == 1:
        stored_molecule = txtfld.get()
        
    if stored_molecule != txtfld.get():
        x = 0

    which1 = cb1.get()
    which2 = cb2.get()
    molecule = txtfld.get()
    value = txtfld1.get()
    answer.set('')

    #stops execution if no molecule is entered
    if molecule == '':
            answer.set('Please enter a molecule')
            return

    #stops execution if number is invalid
    try:
        value = float(value)
    except:
        answer.set('Please enter a valid number')
        return
        

    #stops execution if process is invalid
    if which1 == 'Unit you have' or which2 == 'Unit you want' or which1 == which2:
        answer.set('Please enter a valid conversion')
        return

    if stored_molecule != txtfld.get() or x == 1:
        
        

        #creates an invisible browser session that runs in the background
        options = webdriver.FirefoxOptions()
        options.headless = True
        browser = webdriver.Firefox(options=options)

        
        

        #searches pubchem for the given molecule
        browser.get('https://pubchem.ncbi.nlm.nih.gov/#query=' + molecule)

        #this is here to let the page fully load before searching it, might need to be longer on slower connections
        time.sleep(1.5)
        #gets the molar mass of the first search result; will break if pubchem changes their html, look at better options
        try:
            mw = browser.find_element('css selector', '#featured-results > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > span:nth-child(1) > span:nth-child(2) > span:nth-child(1)')
            mmresult = str(mw.text)
            MW = float(mw.text)
        except:
            pass
        

        
        #searches wikipedia for density of molecule; currently not foolproof and can find the wrong value
        try:
            density = browser.get('https://en.wikipedia.org/wiki/' + molecule)
            time.sleep(1)
            density = browser.find_element('css selector','.infobox > tbody:nth-child(2) > tr:nth-child(29) > td:nth-child(2)' )
            denresult = str(density.text)
        except:
            pass

        browser.quit()

        #prints the fetched values to the UI so they can be verified
        try:
            fetched_mm.set('MW:' + mmresult + ' g/mol')
        except:
            fetched_mm.set('Molar mass not found')
        #try/except so bad density fetch doesn't break the program
        try:
            fetched_den.set('Density = ' + denresult)
        except:
            fetched_den.set('Density not found')

    else:
        pass

    #if/else decides what function dictionary to pull from
    if which2 == 'Mass(g)':
        choice = mass_functions
    elif which2 == 'Moles(mols)':
        choice = mols_functions
    elif which2 == 'Molarity(M)':
        choice = molarity_functions
    elif which2 == 'Volume(mL)':
        choice = volume_functions

    #executes function at the input key, find better way to feed arguments to function
    for key in choice:
        if which1 == key:
            choice[key](value, MW)

    
    


window=Tk()


options1 = ('Unit you have', 'Mass(g)', 'Volume(mL)', 'Moles(mols)', 'Molarity(M)', 'Molality(m)')
options2 = ('Unit you want', 'Mass(g)', 'Volume(mL)', 'Moles(mols)', 'Molarity(M)', 'Molality(m)')



#creates output variables
fetched_mm = StringVar()
fetched_mm.set('')

fetched_den = StringVar()
fetched_den.set('')

answer = StringVar()
answer.set('')



lbl1=Label(window, text="Known Value:", fg='black', font=("Arial", 10))
lbl1.place(x=45, y=170)

#entry field for value you have
txtfld1=Entry(window, bd=5, width=8)
txtfld1.place(x=50, y=190)

# creates the dropdown menus
cb1=Combobox(window, values=options1)
cb1.place(x=50, y=225)
cb1.current(0)


cb2=Combobox(window, values=options2)
cb2.place(x=50, y=255)
cb2.current(0)


#creates the button
btn=Button(window, text="Solve", fg='black')
btn.place(x=210, y=250)

lbl=Label(window, text="Enter the name of the molecule in question", fg='black', font=("Arial", 10))
lbl.place(x=47, y=25)

#entry field for molecule
txtfld=Entry(window, bd=5)
txtfld.place(x=50, y=50)

#output fields
output1 = Label(window, textvariable=fetched_mm)
output1.place(x=300,y=210)
output2 = Label(window, textvariable=fetched_den)
output2.place(x=300,y=235)
output3 = Label(window, textvariable=answer)
output3.place(x=300,y=260)


#binds button to solve function
btn.bind('<Button-1>', solve)

#initialises the window
window.title('Stoichiometry')
window.geometry("500x300+10+20")
window.mainloop()