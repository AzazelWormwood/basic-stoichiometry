import time
from selenium import webdriver
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
    result = browser.find_element('css selector', '#featured-results > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > span:nth-child(1) > span:nth-child(2) > span:nth-child(1)')
    result = float(result.text)
except:
    print('Data not found')
    quit()

browser.quit()

choices = ['mols', 'mass', 'volume', 'molarity', 'molality']

#conversion functions
def what_mass(mols, molar_mass):
    mass_needed = mols * molar_mass
    print('You need ' + str(mass_needed) + " grams.")

def what_mols(mass, molar_mass):
    mols_needed = mass/molar_mass
    print('You need ' + str(mols_needed) + " moles.")

def molarity_from_mass(molarity, volume, molar_mass):
    mols_needed = molarity * (volume/1000)
    mass_needed = mols_needed * molar_mass
    print('You need ' + str(mass_needed) + " grams.")



which1 = input('What would you like to solve for? ')
which2 = input('What are you solving from? ')

#if/else statements to decide the correct conversion function to use
if which1.lower() == 'mols' and which2.lower() == 'mass':
    what_mass(float(input('How many moles do you want? ')), result)

elif which1.lower() == 'mass' and  which2.lower() == 'mols':
    what_mols(float(input('How much mass do you want in grams? ')),result)

elif which1.lower() == 'mass' and which2.lower() == 'molarity':
    molarity = float(input('What molarity do you want? '))
    volume = float(input('What volume will be used in mL? '))
    molarity_from_mass(molarity, volume, result)
 
else:
    print('Currently not supported')



