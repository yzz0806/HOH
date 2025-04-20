import re
import string

def compare_files(file1_path, file2_path):
    """
    Compares two .txt files line-by-line and calculates accuracy.
    The second file ignores timestamps at the beginning of each line.
    Capitalization and punctuation are also ignored.
    """
    try:
        # Read the contents of both files line by line
        with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()

        # Preprocess text to ignore capitalization and punctuation
        def preprocess_text(text):
            return text.lower().translate(str.maketrans('', '', string.punctuation))

        # Remove timestamps and preprocess each line
        def clean_line(line):
            # Remove the timestamp pattern [20xx-xx-xxTxx:xx:xx.xxxZ]
            line = re.sub(r'\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z\]\s*', '', line)
            return preprocess_text(line)

        lines1 = [clean_line(line.strip()) for line in lines1]
        lines2 = [clean_line(line.strip()) for line in lines2]

        # Calculate total lines and matching lines
        total_lines = max(len(lines1), len(lines2))
        matching_lines = sum(1 for l1, l2 in zip(lines1, lines2) if l1 == l2)

        # Calculate accuracy
        accuracy = (matching_lines / total_lines) * 100 if total_lines > 0 else 0

        print(f"Total Lines: {total_lines}")
        print(f"Matching Lines: {matching_lines}")
        print(f"Accuracy: {accuracy:.2f}%")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Input file paths
    file1_path = input("Enter the path to the first .txt file: ").strip()
    file2_path = input("Enter the path to the second .txt file: ").strip()

    # Compare the files
    compare_files(file1_path, file2_path)