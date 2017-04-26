import sys
import json

from taxCalculator import TaxCalculator

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Please provide imput file name!"
        exit()
    
    with open(str(sys.argv[1])) as data_file:    
        data = json.load(data_file)

    taxCalculator = TaxCalculator(data)
    print taxCalculator.calculateTax()
    print taxCalculator.getSummaryText()
    