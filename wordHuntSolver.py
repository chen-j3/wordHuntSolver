# uses trie to make it faster
import time

# 8 possible directions to search from a grid (up, down, left, right, and the 4 diagonals) -- similar to other file
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# TrieNode class to represent each node in the Trie
class TrieNode:
    def __init__(self):
        # dictionary to store child nodes -- keys are chars and the values are trienode instances
        self.children = {}
        # boolean to see if current node represents the end of a valid word
        self.is_end_of_word = False

# Trie class which has insertion, prefix search, and word search operations
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        # start at root node
        node = self.root
        for char in word:
            # go through each characer in the current word and see if the char is not already in there 
            # then we create a new TrieNode
            if char not in node.children:
                node.children[char] = TrieNode()
            # move to child node corresponding to current character
            node = node.children[char]
        # mark the last node as the end of a word that is valid
        node.is_end_of_word = True

    def starts_with(self, prefix):
        node = self.root
        # Go through each character in prefix
        for char in prefix:
            # If the character is not found in the current's children then prefix DNE
            if char not in node.children:
                return False
            node = node.children[char]
        # All letters in the prefix were found so we return true
        return True

    def search(self, word):
        # similar to start with except going through a word
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        # Return true only once we reach the final node (letter) of a word
        return node.is_end_of_word

# Function to perform backtracking and find words in the grid
def backtrack(grid, x, y, current_word, visited, trie, res):
    # If the current word is valid then we will add it to the result
    # Very similar algorithm to previous -- Used to compare and highlight how the trie class speeds up the program
    if trie.search(current_word):
        res.add(current_word)

    # Explore all 8 possible directions
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy

        row_size = len(grid)
        column_size = len(grid[0])
        # Check if the next cell is within bounds, hasn't been visited, and is a valid prefix
        if 0 <= nx < row_size and 0 <= ny < column_size and not visited[nx][ny]:
            if trie.starts_with(current_word + grid[nx][ny]):  # Check if the prefix is valid
                visited[nx][ny] = True
                backtrack(grid, nx, ny, current_word + grid[nx][ny], visited, trie, res)
                visited[nx][ny] = False  # Backtrack to explore that option later on again

# Function to find all valid words in the grid
def find_words_in_grid(grid, trie):
    row_size, column_size = len(grid), len(grid[0])
    res = set()

    # Visited array to keep track of the cells we've already used in a word
    visited = [[False] * column_size for _ in range(row_size)]

    # Start backtracking from each cell in the grid
    for i in range(row_size):
        for j in range(column_size):
            visited[i][j] = True
            backtrack(grid, i, j, grid[i][j], visited, trie, res)
            # Reset the visited array after each cell to explore again later on
            visited[i][j] = False 

    return res

# Function to load a large dictionary from a file and insert into Trie
def load_dictionary(file_path):
    trie = Trie()
    with open(file_path, 'r') as f:
        for line in f:
            # Ensure all letters are upper case like the input grid case
            word = line.strip().upper()
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
def main(input_file='input.txt', output_file='output2.txt', dictionary_file='Collins Scrabble Words (2019).txt'):
    # Load the grid from the input file
    grid = load_grid(input_file)

    # Load the Trie with a larger dictionary from a file
    trie = load_dictionary(dictionary_file)  # Replace with your dictionary file path

    # Record the start time
    start_time = time.time()

    # Find all words in the grid
    found_words = find_words_in_grid(grid, trie)

    # Sort the words by length (longest first)
    sorted_words = sorted(found_words, key=lambda word: (-len(word), word))

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Write the results and running time to the output file
    write_results(output_file, sorted_words, elapsed_time)

# Call the main function
if __name__ == "__main__":
    main()
