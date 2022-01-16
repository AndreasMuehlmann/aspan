#Cospa

creator: Andreas Mühlmann
License: MIT
Github: https://github.com/AndreasMuehlmann/cospa

wavelength_to_RGB: http://www.noah.org/wiki/Wavelength_to_RGB_in_Python

#Quickstart:

    To enter a spectrum make a new text file and enter the points of the curve.
        - one point is on one line
        - x and y koordinates are separated by a comma
        - x is first y is second
        - when entering floating pont numbers use a dot (example: 2.5)
        - the absorption (the y) has to be measured from 0 to 2.5
            (
                If yours is measured diffenrently use the convert.py.
                For that enter "python convert.py [faktor] (to multiply your y so its from 0 to 2.5)"
                (you have to be in the directory of the  convert.py and the spectrum)
            )

        #it should look like this:
        x1, y1
        x2, y2
        x3, y3
        x4, y4
        x5, y5
        x6, y6

        #example
        400, 0.65
        425, 0.80
        460, 0.60
        480, 0.60
        525, 0.15
        650, 0.30
        675, 0.60
        710, 0.05
        800, 0.01

    #after finishing:

    Run the programm by typing:
    "python (a python interpreter has to be installed) main.py [filename] (the one you just created)"
    into a terminal (you have to be in the directory of the main.py and the spectrum)