import re

def compare_files(file1_path, file2_path):
    """
    Compares two .txt files word-for-word and calculates accuracy.
    The second file ignores timestamps at the beginning of each line.
    """
    try:
        # Read the contents of both files
        with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
            text1 = file1.read().split()
            
            # Remove timestamps from each line in the second file
            text2 = []
            for line in file2:
                # Remove the timestamp pattern [20xx-xx-xxTxx:xx:xx.xxxZ]
                cleaned_line = re.sub(r'\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z\]\s*', '', line)
                text2.extend(cleaned_line.split())

        # Calculate total words and matching words
        total_words = max(len(text1), len(text2))
        matching_words = sum(1 for w1, w2 in zip(text1, text2) if w1 == w2)

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