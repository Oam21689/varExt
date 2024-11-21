# varExtractor

`varExtractor` is a Python tool designed to extract and document variables from Python code files or directories. It features a dynamic web-based interface powered by Flask and saves the extracted data as a CSV file for further use.

---

## Features

- Extracts variables from Python files, including:
  - **Variable Name**: Name of the variable.
  - **Data Type**: Inferred type (e.g., `int`, `str`, `list`).
  - **Default Value**: Assigned value, if available.
  - **Scope**: Indicates if the variable is global or belongs to a function.
- Dynamically generates styled web tables based on function scope.
- Saves the extracted variables to a CSV file in the `documentation/` folder.
- Provides a JSON API endpoint for programmatic access to variable data.
- Colorful terminal output for an enhanced user experience.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/oam21689/varExtractor.git
   cd varExtractor

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python varExt.py <path_to_python_file_or_directory>
   ```
4. Access the web interface:
   Open your web browser and navigate to `http://127.0.0.1:5000/` to view the extracted variables.

5. View the CSV documentation:
   The extracted variables are saved as a CSV file in the `documentation/` folder.

6. Use the JSON API:
   The script also provides a JSON API endpoint at `http://127.0.0.1:5000/api/variables` to access the variable data programmatically.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
