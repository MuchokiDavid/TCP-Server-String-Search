"""
Sort the data in the input file based on the first numerical value in each line and save the sorted data to the output file.

Parameters:
    Input_file - The file containing unsorted data.
    Output_file - The file where the sorted data will be saved.
"""
#!/usr/bin/env python3
def sort_data(input_file, output_file):
    # Read all lines from the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Parse each line and prepare for sorting
    # We'll convert the first value to an integer for proper numerical sorting
    parsed_lines = []
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            parts = line.split(';')
            if parts and len(parts) > 0:
                try:
                    # Convert first value to integer for numerical sorting
                    first_val = int(parts[0])
                    parsed_lines.append((first_val, line))
                except ValueError:
                    # If conversion fails, just use the line as is
                    continue
    
    # Sort the lines based on the first value (numerically)
    sorted_lines = sorted(parsed_lines, key=lambda x: x[0])
    
    # Write the sorted lines to the output file
    with open(output_file, 'w') as f:
        for _, line in sorted_lines:
            f.write(line + '\n')

if __name__ == "__main__":
    input_file = "data/200k.txt"
    output_file = "data/200k_sorted.txt"
    sort_data(input_file, output_file)
    print(f"Data sorted and saved to {output_file}")