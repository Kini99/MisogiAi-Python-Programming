from datetime import datetime, timedelta
import re

class Employee:
    company_name = "GlobalTech Solutions"
    total_employees = 0
    departments = {"Engineering": 0, "Sales": 0, "HR": 0, "Marketing": 0}
    tax_rates = {"USA": 0.22, "India": 0.18, "UK": 0.25}
    next_employee_id = 1

    def __init__(self, name, department, base_salary, country, email):
        self.employee_id = Employee.generate_employee_id()
        self.name = name
        self.department = department
        self.base_salary = base_salary
        self.country = country
        self.email = email
        self.hire_date = datetime.now()
        self.performance_ratings = []

        Employee.total_employees += 1
        if department in Employee.departments:
            Employee.departments[department] += 1

    # --------- Static Methods ----------
    @staticmethod
    def validate_email(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def calculate_tax(salary, country):
        rate = Employee.tax_rates.get(country, 0)
        return salary * rate

    @staticmethod
    def is_valid_department(dept):
        return dept in Employee.departments

    @staticmethod
    def generate_employee_id():
        year = datetime.now().year
        emp_id = f"EMP-{year}-{Employee.next_employee_id:04d}"
        Employee.next_employee_id += 1
        return emp_id

    # --------- Class Methods ----------
    @classmethod
    def from_csv_data(cls, csv_line):
        name, dept, salary, country, email = csv_line.split(",")
        return cls(name.strip(), dept.strip(), float(salary.strip()), country.strip(), email.strip())

    @classmethod
    def get_department_stats(cls):
        return {dept: {"count": count} for dept, count in cls.departments.items() if count > 0}

    @classmethod
    def set_tax_rate(cls, country, rate):
        cls.tax_rates[country] = rate

    @classmethod
    def hire_bulk_employees(cls, employee_list):
        for line in employee_list:
            emp = cls.from_csv_data(line)

    # --------- Instance Methods ----------
    def add_performance_rating(self, rating):
        if 1 <= rating <= 5:
            self.performance_ratings.append(rating)

    def get_average_performance(self):
        if not self.performance_ratings:
            return 0
        return sum(self.performance_ratings) / len(self.performance_ratings)

    def calculate_net_salary(self):
        tax = Employee.calculate_tax(self.base_salary, self.country)
        return self.base_salary - tax

    def get_years_of_service(self):
        return (datetime.now() - self.hire_date).days / 365

    def is_eligible_for_bonus(self):
        return self.get_average_performance() > 3.5 and self.get_years_of_service() > 1


# Test Case 1: Class setup and basic functionality
Employee.company_name = "GlobalTech Solutions"
Employee.tax_rates = {"USA": 0.22, "India": 0.18, "UK": 0.25}
Employee.departments = {"Engineering": 0, "Sales": 0, "HR": 0, "Marketing": 0}

emp1 = Employee("John Smith", "Engineering", 85000, "USA", "john.smith@globaltech.com")
assert emp1.employee_id.startswith("EMP-2025")
assert Employee.total_employees == 1
assert Employee.departments["Engineering"] == 1

# Test Case 2: Static method validations
assert Employee.validate_email("test@company.com") == True
assert Employee.validate_email("invalid-email") == False
assert Employee.is_valid_department("Engineering") == True
assert Employee.is_valid_department("InvalidDept") == False
assert abs(Employee.calculate_tax(100000, "USA") - 22000) < 0.01

# Test Case 3: Class methods and bulk operations
emp2 = Employee.from_csv_data("Sarah Johnson,Sales,75000,UK,sarah.j@globaltech.com")
assert emp2.name == "Sarah Johnson"
assert emp2.department == "Sales"

bulk_data = [
    "Mike Wilson,Marketing,65000,India,mike.w@globaltech.com",
    "Lisa Chen,HR,70000,USA,lisa.chen@globaltech.com"
]

Employee.hire_bulk_employees(bulk_data)
assert Employee.total_employees == 4

stats = Employee.get_department_stats()
assert stats["Engineering"]["count"] == 1
assert stats["Sales"]["count"] == 1

# Test Case 4: Performance and bonus calculations
emp1.add_performance_rating(4.2)
emp1.add_performance_rating(4.5)
emp1.add_performance_rating(3.8)
assert abs(emp1.get_average_performance() - 4.17) < 0.01

emp1.hire_date = datetime.now() - timedelta(days=800)
assert emp1.get_years_of_service() > 2
assert emp1.is_eligible_for_bonus() == True

# Test Case 5: Salary calculations
net_salary = emp1.calculate_net_salary()
expected_net = 85000 - (85000 * 0.22)
assert abs(net_salary - expected_net) < 0.01

print("✅ All tests passed!")