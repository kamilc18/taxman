class TaxCalculator:

	def __init__(self, year):
		self.months = year['months']
		self.tax_free_allowance = year['tax_free_allowance']
		self.high_tax_threshold = year['high_tax_threshold']
		self.low_tax_rate = year['low_tax_rate']
		self.high_tax_rate = year['high_tax_rate']
		self.low_nic_monthly = year['low_nic_monthly']
		self.high_nic_monthly = year['high_nic_monthly']
		self.low_nic_rate = year['low_nic_rate']
		self.high_nic_rate = year['high_nic_rate']

	def round2(self, number):
		return round(number, 2)

	def getMonthlyBasis(self, referenceSalary):
		return self.round2(referenceSalary/12.0)

	def getMyMonthlyPensionContribution(self, basis, pensionRate):
		return self.round2(basis * pensionRate);

	def getMonthlyPensionMatch(self, my_pension_contrib, pension_match_rate):
		return self.round2(my_pension_contrib * pension_match_rate)

	def getNic(self, basis_nic, high_nic_monthly, low_nic_monthly, high_nic_rate, low_nic_rate):
		nic = 0;
		nic_high = basis_nic - high_nic_monthly;
		nic_low = basis_nic - low_nic_monthly;

		if nic_high > 0:
			nic_low -= nic_high;
			nic += self.round2(nic_high * high_nic_rate);

		if nic_low > 0:
			nic += self.round2(nic_low * low_nic_rate);
		nic = self.round2(nic);

		return nic

	def getMonthlyTaxFreeAllowance(self, benefitInKind):
		return self.round2((self.tax_free_allowance - benefitInKind)/12.0);

	def getMonthlyHigherTaxThreshold(self):
		return self.round2(self.high_tax_threshold/12.0);

	def getMonthlyIncomeTax(self, basis_tax, high_tax_threshold):
		tax = 0;
		tax_high = basis_tax - high_tax_threshold;
		tax_low = basis_tax;
		if tax_high > 0:
			tax += self.round2(tax_high * self.high_tax_rate);
			tax_low -= tax_high;
			
		tax += self.round2(tax_low * self.low_tax_rate);
		tax = self.round2(tax);
		return tax

	def calculateTax(self):

		self.total_gross = 0		# total gross in a year (incl. bonus)
		self.total_taxable = 0		# total taxable in a year (out of gross)
		self.total_tax_free	= 0		# total tax free in a year
		self.total_my_pension = 0	# my total pension contributions
		self.total_pension_match = 0# total pension matched by company
		self.total_pension = 0		# total pension contrib. (mine + match)
		self.total_tax = 0			# total income tax
		self.total_nic = 0			# total heath insurance contributions
		self.total_in_pocket = 0	# what's left for me
		self.tax_return = 0			# refund I should pay/get

		text = "";

		tax_free_carry_over = 0		# tax free allowance from months of no work
		higher_tax_carry_over = 0	# higher tax threshold carry over from months of no work

		for month in self.months:
			# tax free allowance for this month
			tax_free = self.getMonthlyTaxFreeAllowance(month['benefit'])
			high_tax_threshold = self.getMonthlyHigherTaxThreshold()

			if not month['worked']:
				tax_free_carry_over += tax_free
				higher_tax_carry_over += high_tax_threshold
				continue

			basic_salary = self.getMonthlyBasis(month['salary'])

			my_pension_contrib = self.getMyMonthlyPensionContribution(basic_salary, month['pension_rate'])
			pension_match = self.getMonthlyPensionMatch(my_pension_contrib, month['match_rate'])
			pension_this_month = my_pension_contrib + pension_match

			basis = basic_salary + month['bonus']
			
			basis_nic = basis - my_pension_contrib;	# basis for NIC is without pension

			nic = self.getNic(basis_nic, self.high_nic_monthly, self.low_nic_monthly, self.high_nic_rate, self.low_nic_rate)

			tax_free += tax_free_carry_over
			tax_free_carry_over = 0

			basis_tax = basis_nic - tax_free;		# basis for income tax (less tax-free allowance)
			
			high_tax_threshold += higher_tax_carry_over
			higher_tax_carry_over = 0

			tax = self.getMonthlyIncomeTax(basis_tax, high_tax_threshold)

			in_pocket = self.round2(basis_nic - nic - tax);
			
			self.total_gross += basis;
			self.total_taxable += basis_nic;
			self.total_tax_free += tax_free;
			self.total_my_pension += my_pension_contrib;
			self.total_pension_match += pension_match;
			self.total_pension += pension_this_month;
			self.total_tax += tax;
			self.total_nic += nic;
			self.total_in_pocket += in_pocket;

			text += (month['name'] + "|" +
				" b: " + str(basis) +
				" p: " + str(my_pension_contrib) +
				" p_m: " + str(pension_match) +
				" p_t: " + str(pension_this_month) +
				" tax: " + str(tax) +
				" nic: " + str(nic) +
				" in_pocket: " + str(in_pocket) +
				"\n");

		# tax return
		actual_tax = 0
		actual_taxable = self.total_taxable - self.total_tax_free
		taxable_over_threshold = actual_taxable - self.high_tax_threshold

		if taxable_over_threshold > 0:
			actual_tax += (taxable_over_threshold * self.high_tax_rate)
			actual_tax += (self.high_tax_threshold * self.low_tax_rate)
		else:
			actual_tax += (actual_taxable * self.low_tax_rate)

		self.tax_return = self.total_tax - actual_tax

		self.total_gross = self.round2(self.total_gross);
		self.total_taxable = self.round2(self.total_taxable);
		self.total_tax_free = self.round2(self.total_tax_free);
		self.total_my_pension = self.round2(self.total_my_pension);
		self.total_pension_match = self.round2(self.total_pension_match);
		self.total_pension = self.round2(self.total_pension);
		self.total_tax = self.round2(self.total_tax);
		self.total_nic = self.round2(self.total_nic);
		self.total_tax_nic = self.round2(self.total_tax + self.total_nic); # total tax money
		self.total_in_pocket = self.round2(self.total_in_pocket);
		self.tax_return = self.round2(self.tax_return);

		return text

	def getSummaryText(self):
		return ("TOTAL\n" +
				"GROSS: " + str(self.total_gross) + "  TAXABLE: " + str(self.total_taxable) + "  TAX FREE: " + str(self.total_tax_free) + "\n" +
				"PENSION: my(" + str(self.total_my_pension) + ")+match(" + str(self.total_pension_match) + ")=" + str(self.total_pension) + "\n" +
				"TAKEN: tax(" + str(self.total_tax) + ")+nic(" + str(self.total_nic) + ")=" + str(self.total_tax_nic) + "\n" +
				"IN POCKET: " + str(self.total_in_pocket) + "\n" +
				"TAX RETURN: " + str(self.tax_return) + "\n")

	def getTotalGross(self):
		return self.total_gross

	def getTotalTaxable(self):
		return self.total_taxable

	def getTotalTaxFree(self):
		return self.total_tax_free

	def getTotalMyPension(self):
		return self.total_my_pension

	def getTotalPensionMatch(self):
		return self.total_pension_match

	def getTotalPension(self):
		return self.total_pension

	def getTotalTax(self):
		return self.total_tax

	def getTotalNic(self):
		return self.total_nic

	def getTotalTaxNic(self):
		return self.total_tax_nic

	def getTotalPocket(self):
		return self.total_in_pocket

	def getTaxReturn(self):
		return self.tax_return
