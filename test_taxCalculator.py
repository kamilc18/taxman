import unittest

from taxCalculator import TaxCalculator

class TestTaxCalculator(unittest.TestCase):

    def setUp(self):

        year = {
            "low_nic_monthly": 680,
            "tax_free_allowance": 11500,
            "high_tax_threshold": 33500,
            "high_nic_monthly": 3750,
            "high_nic_rate": 0.02,
            "date": 1950,
            "low_tax_rate": 0.2,
            "low_nic_rate": 0.12,
            "months": [
                {"salary": 0,      "match_rate": 0.0,  "name": "APR", "pension_rate": 0.0, "bonus": 0,    "benefit": 0,    "worked": False},
                {"salary": 100000, "match_rate": 0.66, "name": "MAY", "pension_rate": 0.1, "bonus": 1000, "benefit": 0,    "worked": True},
                {"salary": 100000, "match_rate": 0.66, "name": "JUN", "pension_rate": 0.1, "bonus": 0,    "benefit": 1000, "worked": True},
                {"salary": 100000, "match_rate": 0.66, "name": "JUL", "pension_rate": 0.1, "bonus": 2000, "benefit": 1000, "worked": True},
                {"salary": 100000, "match_rate": 0.66, "name": "AUG", "pension_rate": 0.1, "bonus": 0,    "benefit": 1000, "worked": True},
                {"salary": 100000, "match_rate": 0.66, "name": "SEP", "pension_rate": 0.1, "bonus": 3000, "benefit": 1000, "worked": True},
                {"salary": 100000, "match_rate": 0.66, "name": "OCT", "pension_rate": 0.1, "bonus": 0,    "benefit": 1000, "worked": True},
                {"salary": 100000, "match_rate": 0.66, "name": "NOV", "pension_rate": 0.1, "bonus": 0,    "benefit": 1000, "worked": True},
                {"salary": 100000, "match_rate": 0.66, "name": "DEC", "pension_rate": 0.1, "bonus": 0,    "benefit": 1000, "worked": True},
                {"salary": 100000, "match_rate": 0.66, "name": "JAN", "pension_rate": 0.1, "bonus": 0,    "benefit": 1000, "worked": True},
                {"salary": 100000, "match_rate": 0.66, "name": "FEB", "pension_rate": 0.1, "bonus": 5000, "benefit": 1000, "worked": True},
                {"salary": 100000, "match_rate": 0.66, "name": "MAR", "pension_rate": 0.1, "bonus": 0,    "benefit": 1000, "worked": True}
            ],
            "high_tax_rate": 0.4
        }

        self.taxCalculator = TaxCalculator(year)

    def test_round2(self):
        self.assertEqual(self.taxCalculator.round2(1.244), 1.24)
        self.assertEqual(self.taxCalculator.round2(1.245), 1.25)
        self.assertEqual(self.taxCalculator.round2(1.246), 1.25)

    def test_getMonthlyBasis(self):
        monthly_basis = self.taxCalculator.getMonthlyBasis(120.0)
        self.assertEqual(monthly_basis, 10.0)

    def test_getMyMonthlyPensionContribution(self):
        monthly_contrib = self.taxCalculator.getMyMonthlyPensionContribution(120.0, 0.5)
        self.assertEqual(monthly_contrib, 60.0)

    def test_getMonthlyPensionMatch(self):
        monthly_match = self.taxCalculator.getMonthlyPensionMatch(120.0, 0.5)
        self.assertEqual(monthly_match, 60.0)

    def test_getNic(self):
        nic = self.taxCalculator.getNic(8333.33, 3750, 680, 0.02, 0.12)
        self.assertEqual(nic, 460.07)

    def test_calculateTax(self):
        self.taxCalculator.calculateTax()

        total_gross = self.taxCalculator.getTotalGross();
        total_taxable = self.taxCalculator.getTotalTaxable();
        total_tax_free = self.taxCalculator.getTotalTaxFree();
        total_my_pension = self.taxCalculator.getTotalMyPension()
        total_pension_match = self.taxCalculator.getTotalPensionMatch();
        total_pension = self.taxCalculator.getTotalPension();
        total_tax = self.taxCalculator.getTotalTax();
        total_nic = self.taxCalculator.getTotalNic();
        total_tax_nic = self.taxCalculator.getTotalTaxNic();
        total_in_pocket = self.taxCalculator.getTotalPocket();
        tax_return = self.taxCalculator.getTaxReturn();

        self.assertEqual(total_gross, 102666.63)
        self.assertEqual(total_taxable, 93500.0)
        self.assertEqual(total_tax_free, 10666.66)
        self.assertEqual(total_my_pension, 9166.63)
        self.assertEqual(total_pension_match, 6050.0)
        self.assertEqual(total_pension, 15216.63)
        self.assertEqual(total_tax, 26433.27)
        self.assertEqual(total_nic, 5097.4)
        self.assertEqual(total_tax_nic, 31530.67)
        self.assertEqual(total_in_pocket, 61969.33)
        self.assertEqual(tax_return, -0.07)

if __name__ == '__main__':
    unittest.main()
