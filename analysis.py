import os
from datetime import datetime

# ============= STEP 1: STANDALONE FUNCTIONS FOR CALCULATIONS =============

def calculate_total(data):
    """Calculate the sum of all values in the dataset."""
    total = 0
    for value in data:
        total += value
    return total


def calculate_average(data):
    """Calculate the average of all values in the dataset."""
    if len(data) == 0:
        return 0
    total = calculate_total(data)
    average = total / len(data)
    return average


def find_minimum(data):
    """Find the minimum value in the dataset."""
    if len(data) == 0:
        return None
    min_value = data[0]
    for value in data:
        if value < min_value:
            min_value = value
    return min_value


def find_maximum(data):
    """Find the maximum value in the dataset."""
    if len(data) == 0:
        return None
    max_value = data[0]
    for value in data:
        if value > max_value:
            max_value = value
    return max_value


def extract_unique_categories(category_file):
    """Extract unique values from a categorical data file."""
    try:
        with open(category_file, 'r') as file:
            categories = set()
            for line in file:
                line = line.strip()
                if line:
                    categories.add(line)
            return categories
    except FileNotFoundError:
        print(f"Error: Category file '{category_file}' not found.")
        return set()


# ============= STEP 2: OOP - DataSet CLASS =============

class DataSet:
    """A class to manage dataset operations and statistical analysis."""
    
    def __init__(self, data_file, category_file=None, threshold=75):
        """Initialize the DataSet object."""
        self.data_file = data_file
        self.category_file = category_file
        self.threshold = threshold
        self.data = []
        self.categories = set()
        self.statistics = {}
    
    def load_data(self):
        """Load numerical data from a file."""
        # Check if file exists
        if not os.path.exists(self.data_file):
            print(f"Error: File '{self.data_file}' does not exist.")
            return False
        
        # Check if file is empty and load data
        try:
            with open(self.data_file, 'r') as file:
                lines = file.readlines()
                
                if len(lines) == 0:
                    print("Error: The data file is empty.")
                    return False
                
                for line in lines:
                    line = line.strip()
                    if line:
                        try:
                            # Try to convert to float (handles both int and float)
                            value = float(line)
                            self.data.append(value)
                        except ValueError:
                            print(f"Error: Invalid value '{line}' - expected a number.")
                            return False
            
            print(f"Successfully loaded {len(self.data)} data points.")
            return True
        
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
    
    def load_categories(self):
        """Load categorical data from a file."""
        if self.category_file is None:
            print("No category file specified.")
            return
        
        self.categories = extract_unique_categories(self.category_file)
        if self.categories:
            print(f"Successfully loaded {len(self.categories)} unique categories.")
    
    def calculate_statistics(self):
        """Calculate statistical measures for the dataset."""
        if len(self.data) == 0:
            print("Error: Cannot calculate statistics on empty dataset.")
            return False
        
        self.statistics = {
            'total': calculate_total(self.data),
            'average': calculate_average(self.data),
            'minimum': find_minimum(self.data),
            'maximum': find_maximum(self.data),
            'count': len(self.data),
            'unique_categories': len(self.categories)
        }
        return True
    
    def evaluate_performance(self):
        """Evaluate performance based on average and threshold."""
        if 'average' not in self.statistics:
            return "Unable to evaluate"
        
        average = self.statistics['average']
        if average >= self.threshold:
            return "High Performance"
        else:
            return "Needs Improvement"
    
    def display_results(self):
        """Display the calculated statistics."""
        if not self.statistics:
            print("No statistics to display. Run calculate_statistics() first.")
            return
        
        print("\n" + "="*50)
        print("DATASET ANALYSIS RESULTS")
        print("="*50)
        print(f"Total Data Points: {self.statistics['count']}")
        print(f"Total Sum: {self.statistics['total']:.2f}")
        print(f"Average: {self.statistics['average']:.2f}")
        print(f"Minimum Value: {self.statistics['minimum']:.2f}")
        print(f"Maximum Value: {self.statistics['maximum']:.2f}")
        print(f"Unique Categories: {self.statistics['unique_categories']}")
        print(f"Performance Status: {self.evaluate_performance()}")
        print(f"Threshold: {self.threshold}")
        print("="*50 + "\n")
    
    def save_report(self, output_file="analysis_report.txt"):
        """Save the analysis results to a file."""
        if not self.statistics:
            print("Error: No statistics to save. Run calculate_statistics() first.")
            return False
        
        try:
            with open(output_file, 'w') as file:
                file.write("="*50 + "\n")
                file.write("DATASET ANALYSIS REPORT\n")
                file.write("="*50 + "\n")
                file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                file.write("STATISTICS:\n")
                file.write(f"Total Data Points: {self.statistics['count']}\n")
                file.write(f"Total Sum: {self.statistics['total']:.2f}\n")
                file.write(f"Average: {self.statistics['average']:.2f}\n")
                file.write(f"Minimum Value: {self.statistics['minimum']:.2f}\n")
                file.write(f"Maximum Value: {self.statistics['maximum']:.2f}\n")
                file.write(f"Threshold: {self.threshold}\n\n")
                
                file.write("PERFORMANCE EVALUATION:\n")
                file.write(f"Status: {self.evaluate_performance()}\n\n")
                
                file.write("CATEGORIES:\n")
                file.write(f"Unique Categories Count: {self.statistics['unique_categories']}\n")
                if self.categories:
                    file.write("Categories:\n")
                    for i, category in enumerate(sorted(self.categories), 1):
                        file.write(f"  {i}. {category}\n")
                
                file.write("\n" + "="*50 + "\n")
            
            print(f"Report saved successfully to '{output_file}'")
            return True
        
        except Exception as e:
            print(f"Error saving report: {e}")
            return False


# ============= STEP 3: MAIN PROGRAM =============

def create_sample_files():
    """Create sample data files for demonstration."""
    # Create sample numerical data file
    with open("marks.txt", "w") as f:
        f.write("85\n92\n78\n88\n95\n76\n89\n91\n84\n87\n")
    
    # Create sample category file
    with open("courses.txt", "w") as f:
        f.write("Mathematics\nEnglish\nScience\nMathematics\nHistory\nEnglish\nScience\n")
    
    print("Sample files created: marks.txt and courses.txt\n")


def main():
    """Main program execution."""
    print("="*50)
    print("DATASET MANAGEMENT AND ANALYSIS SYSTEM")
    print("="*50 + "\n")
    
    # Create sample files for demonstration
    create_sample_files()
    
    # Create a DataSet object
    dataset = DataSet(
        data_file="marks.txt",
        category_file="courses.txt",
        threshold=75
    )
    
    # Load numerical data
    print("Loading numerical data...")
    if not dataset.load_data():
        print("Failed to load data. Exiting.")
        return
    
    # Load categorical data
    print("Loading categorical data...")
    dataset.load_categories()
    
    # Calculate statistics
    print("Calculating statistics...")
    if dataset.calculate_statistics():
        # Display results
        dataset.display_results()
        
        # Save report to file
        dataset.save_report("analysis_report.txt")
    else:
        print("Failed to calculate statistics.")


if __name__ == "__main__":
    main()