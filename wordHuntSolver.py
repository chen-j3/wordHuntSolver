# uses trie to make it faster

import time

# Directions: 8 possible directions (up, down, left, right, and the 4 diagonals)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# TrieNode class to represent each node in the Trie
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

# Trie class to handle insertion, prefix search, and word search
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

# Function to perform backtracking and find words in the grid
def backtrack(grid, x, y, current_word, visited, trie, result):
    # If the current word is valid, add it to the result
    if trie.search(current_word):
        result.add(current_word)

    # Explore all 8 possible directions
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy

        # Check if the next cell is within bounds, hasn't been visited, and is a valid prefix
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and not visited[nx][ny]:
            if trie.starts_with(current_word + grid[nx][ny]):  # Check if the prefix is valid
                visited[nx][ny] = True
                backtrack(grid, nx, ny, current_word + grid[nx][ny], visited, trie, result)
                visited[nx][ny] = False  # Backtrack

# Function to find all valid words in the grid
def find_words_in_grid(grid, trie):
    rows, cols = len(grid), len(grid[0])
    result = set()

    # Visited array to keep track of the cells we've already used in a word
    visited = [[False] * cols for _ in range(rows)]

    # Start backtracking from each cell in the grid
    for i in range(rows):
        for j in range(cols):
            visited[i][j] = True
            backtrack(grid, i, j, grid[i][j], visited, trie, result)
            visited[i][j] = False  # Reset the visited array after each cell

    return result

# Function to load a large dictionary from a file and insert into Trie
def load_dictionary(file_path):
    trie = Trie()
    with open(file_path, 'r') as f:
        for line in f:
            word = line.strip().upper()  # Convert to uppercase to match the grid case
            if len(word) >= 3:  # We are only interested in words of length 3 or more
                trie.insert(word)
    return trie

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

    # Load the Trie with a larger dictionary from a file
    trie = load_dictionary(dictionary_file)  # Replace with your dictionary file path

    # Record the start time
    start_time = time.time()

    # Find all words in the grid
    found_words = find_words_in_grid(grid, trie)

    # Sort the words by length (longest first)
    sorted_words = sorted(found_words, key=len, reverse=True)

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Write the results and running time to the output file
    write_results(output_file, sorted_words, elapsed_time)

# Call the main function
if __name__ == "__main__":
    main()
