import re
from collections import defaultdict

class Design:
    '''Required design of a bouquet'''
    
    def __init__(self, design):

        self.design = design
        self.design_name = None
        self.total_quantity = 0
        self.total_species = 0
        self.design_bouquet = defaultdict(lambda: defaultdict(int))
        
        # Parse and validate the design
        self._parse_design()

    def _parse_design(self):
        '''
        Parameters: 
            self: design object

        Functionality: validating designs entered by user
            1. Check if design of the bouquet is following the expected pattern
                <design name as A-Z><flower size as L | S>
                <flower1 max quantity as number><flower1 species as a-z>...<flowerN max quantity as number><flowerN species as a-z>
                <total quantity as number>
            2. Check if duplicate entry of the same flower species found
            3. Check if the flower species are alphabetically sorted
            4. Check total quantity of flowers should be less than or sum of all flower species max quantity.

        Return: None
        '''

        total = 0

        # 1. 
        if not re.findall(r'^[A-Z]{2}(\d+[a-z])+\d+$', self.design):
            raise ValueError("Error: Design name incorrect, valid syntax" 
                             "<design name as A-Z><flower size as L | S>"
                             "<flower1 max quantity as number><flower1 species as a-z>...<flowerN max quantity as number><flowerN species as a-z>"
                             "<total quantity as number>")
        
        # get design name & size
        self.design_name = re.findall(r'^([A-Z]{2})', self.design)
        self.design_bouquet["Design"][self.design_name[-1][-1]]= self.design_name[0][0]                                      
        self.design_bouquet["Bouquet"][self.design_name[-1][-1]] = self.design_name[0][0]

        # get flower species
        species_match = re.findall(r'(\d+[a-z])', self.design)

        # 2.
        for flower in species_match:
            if flower[-1] in self.design_bouquet["Design"]:
                raise ValueError("Duplicate entry of the same species found")
            else:
                self.design_bouquet["Design"][flower[-1]] = flower[0:-1]
                self.design_bouquet["Bouquet"][flower[-1]] = 0
                total += int(flower[0:-1])
                self.total_species += 1
        # 3.
        for i in range(len(species_match) - 1):
            if species_match[i][-1] > species_match[i + 1][-1]:
                raise ValueError("The flowers are not sorted alphabetically.")                          # Raise error if not sorted
            
        # get total quantity
        self.total_quantity = int(re.findall(r'.*[a-z](\d+)$', self.design)[0])

        # 4.
        if self.total_quantity > total:
            raise ValueError("Total quantity is greater then the sum of all max quantity in flowers")
        elif self.total_quantity < self.total_species:
            raise ValueError("Total quantity is smaller then the number of flower species")
        
        self.design_bouquet["Design"]['TQ'] = self.total_quantity
        print(self.design_bouquet)


class Flower:
    '''Flowers arriving at the facility'''
    
    def __init__(self, flower):
        self.flower = flower
        self.species = None
        self.size = None
        self._parse_input()

    def _parse_input(self):
        '''
        Parameters: 
            self: flower object

        Functionality: validating flowers arriving at facility
            1. Check if flower and flower size is following the expected pattern
                <flower species as a-z><flower size as L | S>

        Return: None
        '''

        # 1.
        match = re.match(r'^[a-z](L|S)$', self.flower)
        if not match:
            raise ValueError(f"Invalid input: {self.flower}. It must be a lowercase letter followed by 'L' or 'S'.")

        self.species = self.flower[0]
        self.size = self.flower[1]


    def flower_callback(self, designs):
        '''
        Parameters: 
            self: flower object
            designs: designs objects array

        Functionality: Checking if the flower species and size satisfying any design 

        Return: None
        '''
        
        for design in designs:

            design_element = design.design_bouquet
            
            if self.size in design_element['Design'] and self.species in design_element['Design']:
                if design_element['Bouquet'][self.species] < int(design_element['Design'][self.species]):
                    # Corner case - AS2a1b1c3
                    if design.total_species == design_element['Design']['TQ'] and design_element['Bouquet'][self.species] == 0:
                        design_element['Bouquet'][self.species] += 1
                    elif design.total_species != design_element['Design']['TQ']:
                        design_element['Bouquet'][self.species] += 1
                    break
                else:
                    continue

    def check_bouquet(self, designs):

        for design in designs:

            design_element = design.design_bouquet
            bouquet = ""
            total = 0
            species_quantity = list(design_element['Bouquet'].values())[1:]

            for quantity in species_quantity:
                if quantity < 1:
                    no_add = False
                    break
                no_add = True
                total += quantity

            if total == design_element['Design']['TQ'] and no_add == True:
                for species in design_element['Bouquet']:
                    bouquet += str(design_element['Bouquet'][species])
                    bouquet += species
                    if isinstance(design_element['Bouquet'][species], int):
                        design_element['Bouquet'][species] = 0
                print(bouquet)


def main():
    
    # Work for a total of 5 wrong inputs
    incorrect_inputs = 0
    designs = []

    print("Enter the design(s) (one per line, empty line to finish):")
    while True:
        design_input = input().strip()
        if design_input == '':
            break
        try:
            design = Design(design_input)
            designs.append(design)                                                          # get all designs
        except ValueError as e:
            print(f"Invalid design: {e}")
            incorrect_inputs += 1

        if incorrect_inputs >= 5:
            print("Too many incorrect inputs. Exiting...")
            return

    # Accept flower species and size inputs
    print("\nEnter flower species and size (e.g., tL) or type 'exit' to quit:")

    while incorrect_inputs < 5:
        flower_input = input().strip()

        if flower_input == '':
            print("No input detected. Please try again.")
            continue

        if flower_input.lower() == 'exit':
            print("Exiting...")
            break

        try:
            flower = Flower(flower_input)                                           
            flower.flower_callback(designs)
            flower.check_bouquet(designs)
        except ValueError as e:
            incorrect_inputs += 1
            print(f"Invalid input: {e}. You have {5 - incorrect_inputs} attempts left.")

        if incorrect_inputs >= 5:
            print("Too many incorrect inputs. Exiting...")
            break


if __name__ == "__main__":
    main()