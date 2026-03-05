import pandas as pd
import os

class ExcelHandler:
    @staticmethod
    def read_numbers(file_path):
        """
        Reads phone numbers from an Excel or CSV file.
        Expects a column named 'phone' or 'number' or uses the first column.
        """
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please upload CSV or Excel.")

        # Try to find the number column
        possible_cols = ['phone', 'number', 'mobile', 'cell']
        target_col = None
        for col in df.columns:
            if col.lower() in possible_cols:
                target_col = col
                break
        
        if target_col is None:
            target_col = df.columns[0] # Fallback to first column
            
        # Extract and clean numbers
        numbers = df[target_col].astype(str).tolist()
        return [self.clean_number(n) for n in numbers if n.strip()]

    @staticmethod
    def clean_number(n):
        """Cleans a phone number by removing non-numeric characters."""
        return "".join(filter(str.isdigit, n))

    @staticmethod
    def save_results(data, output_dir, filename):
        """Saves checking results to an Excel file."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        df = pd.DataFrame(data, columns=['Phone Number', 'WhatsApp Status'])
        file_path = os.path.join(output_dir, filename)
        df.to_excel(file_path, index=False)
        return file_path
