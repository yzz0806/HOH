import re
import string

def compare_files(file1_path, file2_path):
    """
    Compares two .txt files line-by-line and calculates word-level accuracy.
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

        # Clean and split lines into words
        lines1 = [clean_line(line.strip()).split() for line in lines1]
        lines2 = [clean_line(line.strip()).split() for line in lines2]

        total_words = 0
        matching_words = 0

        # Compare each line individually
        for words1, words2 in zip(lines1, lines2):
            total_words += max(len(words1), len(words2))
            matching_words += sum(1 for w1, w2 in zip(words1, words2) if w1 == w2)

        # Calculate accuracy
        accuracy = (matching_words / total_words) * 100 if total_words > 0 else 0

        print(f"Total Words: {total_words}")
        print(f"Matching Words: {matching_words}")
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