# Import time module to print out execution time
import time 

# 8 possible directions to search from a grid (up, down, left, right, and the 4 diagonals)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# Use backtracking to find words on given grid in the input
def backtrack(grid, x, y, current_word, visited, word_Dictionary, res):
    # If the current word is valid and not already added to the result, add it
    if current_word in word_Dictionary:
        res.add(current_word)

    # Explore all directions
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy

        # Check if the next cell is within bounds of the row and column and hasn't been visited
        row_size = len(grid)
        column_size = len(grid[0])
        if 0 <= nx < row_size and 0 <= ny < column_size and not visited[nx][ny]:
            visited[nx][ny] = True
            backtrack(grid, nx, ny, current_word + grid[nx][ny], visited, word_Dictionary, res)
            visited[nx][ny] = False  # Backtrack to explore that option later on again

# Function to find all valid words in the grid
def find_words_in_grid(grid, word_Dictionary):
    row_size, column_size = len(grid), len(grid[0])
    res = set()

    # Visited array to keep track of the cells we've already used in a word
    visited = [[False] * column_size for _ in range(row_size)]

    # Start backtracking from each cell in the grid
    for i in range(row_size):
        for j in range(column_size):
            visited[i][j] = True
            backtrack(grid, i, j, grid[i][j], visited, word_Dictionary, res)
            # Reset the visited array after each cell to explore again later on
            visited[i][j] = False 

    return res

# Function to load a large dictionary from a file
def load_dictionary(file_path):
    word_Dictionary = set()
    with open(file_path, 'r') as f:
        for line in f:
            # Ensure all letters are upper case like the input grid case
            word = line.strip().upper() 
            word_Dictionary.add(word)
    return word_Dictionary

# Function to load the grid from an input file
def load_grid(input_file):
    grid = []
    with open(input_file, 'r') as f:
        for line in f:
            grid.append(line.strip().split())
    return grid

# Function to write the results and running time to an output file
def write_results(output_file, words, elapsed_time):
    with open(output_file, 'w') as f:
        f.write("Found words (longest to shortest, excluding less than 3 letters):\n")
        for word in words:
            f.write(word + "\n")
        f.write(f"\nRunning time: {elapsed_time:.6f} seconds")

# Main function for testing
def main(input_file='input.txt', output_file='output.txt', dictionary_file='Collins Scrabble Words (2019).txt'):
    # Load the grid from the input file
    grid = load_grid(input_file)

    # Load the dictionary from a file
    word_Dictionary = load_dictionary(dictionary_file)

    # Record the start time for time complexity
    start_time = time.time()

    # Find all words in the grid
    found_words = find_words_in_grid(grid, word_Dictionary)

    # Filter out words that are less than 3 letters long -- testing out three letter words
    filtered_words = [word for word in found_words if len(word) >= 3]

    # Sort the words by length (longest first)
    sorted_words = sorted(filtered_words, key=lambda word: (-len(word), word))

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Write the results and running time to the output file
    write_results(output_file, sorted_words, elapsed_time)

# Call the main function
if __name__ == "__main__":
    main()