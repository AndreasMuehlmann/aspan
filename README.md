#Cospa

creator: Andreas Mühlmann
License: MIT
Github: https://github.com/AndreasMuehlmann/cospa

wavelength_to_RGB: http://www.noah.org/wiki/Wavelength_to_RGB_in_Python

Quickstart:

    To enter a spectrum:
        - make a new text file
        - write your upper limit for the y axis into the first line

        To enter the points:
            - one point is on one line
            - x and y koordinates are separated by a comma
            - x is first y is second
            - when entering floating pont numbers use a dot (example: 2.5)
            - the first point has to have the x value 380 and the last x value has to be 780

            it should look like this:
            faktor
            x1, y1
            x2, y2
            x3, y3
            x4, y4
            x5, y5
            x6, y6

            example:
            2.5
            380.0, 1.0556
            420.0, 1.9167
            460.0, 0.2778
            640.0, 0.3333
            675.0, 1.5278
            700.0, 0.4167
            780.0, 0.2778

    after finishing:
    Run the programm by typing:
    ".\aspan [filename] (the one you just created)"
    into a terminal (you have to be in the directory of the executable and the spectrum)