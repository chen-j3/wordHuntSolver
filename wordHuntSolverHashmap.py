#uses hashmap instead of trie

import time
from collections import defaultdict

# Directions: 8 possible directions (up, down, left, right, and the 4 diagonals)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# Function to perform backtracking and find words
def backtrack(grid, x, y, current_word, visited, dictionary_prefix_map, result, memo):
    # If the current word is valid and not already added to the result, add it
    if current_word in dictionary_prefix_map:
        result.add(current_word)

    # If current word's prefix is not valid, no need to continue further
    if current_word not in dictionary_prefix_map:
        return

    # Memoization check to avoid revisiting the same state
    if (x, y, current_word) in memo:
        return

    # Memoize this state
    memo.add((x, y, current_word))

    # Explore all 8 directions
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy

        # Check if the next cell is within bounds and hasn't been visited
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and not visited[nx][ny]:
            visited[nx][ny] = True
            backtrack(grid, nx, ny, current_word + grid[nx][ny], visited, dictionary_prefix_map, result, memo)
            visited[nx][ny] = False  # Backtrack

# Function to find all valid words in the grid
def find_words_in_grid(grid, dictionary_prefix_map):
    rows, cols = len(grid), len(grid[0])
    result = set()

    # Visited array to keep track of the cells we've already used in a word
    visited = [[False] * cols for _ in range(rows)]

    # Set to memoize previous states
    memo = set()

    # Start backtracking from each cell in the grid
    for i in range(rows):
        for j in range(cols):
            visited[i][j] = True
            backtrack(grid, i, j, grid[i][j], visited, dictionary_prefix_map, result, memo)
            visited[i][j] = False  # Reset the visited array after each cell

    return result

# Function to load a large dictionary from a file and create a prefix hashmap
def load_dictionary(file_path):
    dictionary = set()
    dictionary_prefix_map = defaultdict(set)

    with open(file_path, 'r') as f:
        for line in f:
            word = line.strip().upper()  # Convert to uppercase to match the grid case
            dictionary.add(word)
            # Add all possible prefixes to the dictionary_prefix_map
            for i in range(1, len(word) + 1):
                prefix = word[:i]
                dictionary_prefix_map[prefix].add(word)

    return dictionary, dictionary_prefix_map

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
def main(input_file='input.txt', output_file='output.txt', dictionary_file='words.txt'):
    # Load the grid from the input file
    grid = load_grid(input_file)

    # Load the dictionary from a file and create the prefix hashmap
    dictionary, dictionary_prefix_map = load_dictionary(dictionary_file)

    # Record the start time
    start_time = time.time()

    # Find all words in the grid
    found_words = find_words_in_grid(grid, dictionary_prefix_map)

    # Filter out words that are less than 3 letters long
    filtered_words = [word for word in found_words if len(word) >= 3]

    # Sort the words by length (longest first)
    sorted_words = sorted(filtered_words, key=len, reverse=True)

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Write the results and running time to the output file
    write_results(output_file, sorted_words, elapsed_time)

# Call the main function
if __name__ == "__main__":
    main()
