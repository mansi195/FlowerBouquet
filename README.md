This script is a Python-based script designed to create bouquets from flower designs. 

Run Script Command: python createBouquet.php

Inputs:
    - Designs: The design specifications entered by the user.
    - Flowers: The available flowers, with their sizes and quantities, arriving at the facility.
Output:
    - Bouquets: The bouquets are created based on the flower designs as soon as the required flowers arrive.

Steps Taken:
1. Created Two Classes: Design and Flower:
    - Design Class: Handles the logic for parsing and validating flower design input.
    - Flower Class: Handles the arrival of flowers and checks if they match the designs.

2. Implemented the Design Class:
    - Input Parsing and Validation:
        - The design entered by the user is parsed and validated.
        <design name as A-Z> followed by <flower size as L | S>.
        Then, for each flower: <flower max quantity as number><flower species as a-z>.
        Finally, the total quantity of flowers in the design: <total quantity as number>.
    - Validation:
        - The design is validated to ensure it follows the correct format and contains all necessary information.

3. Implemented the Flower Class:
    - Flower Shipments:
        - The flowers arrive at the facility, and their size and quantity are tracked.
    - Design Matching:
        - As flowers arrive, the script checks if they match the design requirements (size and species).
        - Once all flowers for a design are available, a bouquet is created.

Conditions:
1. The input values are provided by the user through the command-line interface.
2. Designs are entered first, followed by an empty line, and then the flower shipments are entered.
3. Bouquets are created in the sequential order of the designs entered by the user, as soon as all the required flowers for a particular design are available.