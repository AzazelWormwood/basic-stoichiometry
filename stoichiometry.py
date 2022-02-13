import time
from selenium import webdriver
nums = ['0', '1', '2', '3', '4', '5', '6','7', '8', '9', '.']
molecule = input('What is the molecule in question? ')

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
    mw = float(mw.text)
except:
    print('Molar mass not found')
    
#searches wikipedia for density of molecule; currently not foolproof and can find the wrong value
try:
    density = browser.get('https://en.wikipedia.org/wiki/' + molecule)
    time.sleep(1)
    density = browser.find_element('css selector','.infobox > tbody:nth-child(2) > tr:nth-child(29) > td:nth-child(2)' )
    denresult = str(density.text)
    
    
except:
    print('Density not found')

browser.quit()

choices = ['mols', 'mass', 'volume', 'molarity', 'molality']

#conversion functions
def mass_for_x_mols(mols, molar_mass):
    mass_needed = mols * molar_mass
    print('You need ' + str(mass_needed) + " grams.")

def mols_for_x_mass(mass, molar_mass):
    mols_needed = mass/molar_mass
    print('You need ' + str(mols_needed) + " moles.")

def mass_for_x_molarity(molarity, volume, molar_mass):
    mols_needed = molarity * (volume/1000)
    mass_needed = mols_needed * molar_mass
    print('You need ' + str(mass_needed) + " grams.")

def molarity_for_x_mass(mass, volume, molar_mass):
    mols_needed = mass/molar_mass
    molarity = mols_needed / (volume/1000)
    print('The molarity is ' + str(molarity) + ' M')

#prints the fetched values so they can be verified
print('Molar mass = ' + mmresult + ' g/mol')

#try/except so bad density fetch doesn't break the program
try:
    print('Density = ' + denresult)
except:
    print('No density value')


print('Mass(g), Moles, Volume (mL), Molarity, Molar Mass (g/mol)')
which1 = input('What would you like to solve for? ')
which2 = input('What are you solving from? ')

#if/else statements to decide the correct conversion function to use
if which1.lower() == 'mols' or which1.lower() == 'moles' and which2.lower() == 'mass':
   mass_for_x_mols(float(input('How many moles do you want? ')), mw)

elif which1.lower() == 'mass' and  which2.lower() == 'mols' or which2.lower() == 'moles':
    mols_for_x_mass(float(input('How much mass do you want in grams? ')),mw)

elif which1.lower() == 'mass' and which2.lower() == 'molarity':
    molarity = float(input('What molarity do you want? '))
    volume = float(input('What volume will be used in mL? '))
    mass_for_x_molarity(molarity, volume, mw)
 
elif which1.lower() == 'molarity' and which2.lower() == 'mass':
    mass = float(input('How much mass will be used in grams? '))
    volume = float(input('What volume will be used in mL? '))
    molarity_for_x_mass(mass, volume, mw)
else:
    print('Currently not supported')



