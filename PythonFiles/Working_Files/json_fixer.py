#https://chat.openai.com/share/0761994a-361a-455d-915b-585e983ff1a3
import json
import sys

def fix_large_json_file(input_file_path):
    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()

        for line_number, line in enumerate(lines):
            try:
                json.loads(line)
            except json.JSONDecodeError:
                # If there's an error, add a comma at the end of the line
                lines[line_number] = line.rstrip('\n') + ','

        with open(input_file_path, 'w') as file:
            file.writelines(lines)

        print("JSON file has been fixed and saved.")
    except FileNotFoundError:
        print("File not found:", input_file_path)

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_large_json_file.py <input_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    fix_large_json_file(input_file_path)

if __name__ == "__main__":
    main()
