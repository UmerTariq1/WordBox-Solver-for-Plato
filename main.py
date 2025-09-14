#!/usr/bin/env python3
"""
Wordbox Game - Find valid words in a 5x5 grid following adjacency rules
Optimized version with Trie-based pruning for maximum performance
"""

import re
from collections import defaultdict
from typing import List, Tuple, Set, Dict, Optional
import sys
import time


class TrieNode:
    """Trie node for efficient prefix checking and word validation"""
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_word: bool = False


class Trie:
    """Trie data structure for fast prefix matching and word validation"""
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert a word into the trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
    
    def search(self, word: str) -> bool:
        """Check if a word exists in the trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word
    
    def has_prefix(self, prefix: str) -> bool:
        """Check if any word in the trie starts with the given prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def get_node(self, prefix: str) -> Optional[TrieNode]:
        """Get the trie node corresponding to a prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node


class WordboxGame:
    def __init__(self, grid_file: str = "grid.txt"):
        self.grid = []
        self.bonus_tiles = set()
        self.rows = 5
        self.cols = 5
        self.neighbors = {}  # Precomputed adjacency lookup
        self.trie = Trie()
        
        print("Loading dictionary...")
        start_time = time.time()
        self._load_dictionary()
        dict_time = time.time() - start_time
        print(f"Dictionary loaded in {dict_time:.3f}s")
        
        print("Loading grid...")
        self._load_grid(grid_file)
        
        print("Precomputing adjacency...")
        self._precompute_adjacency()
        
    def _load_grid(self, filename: str) -> None:
        """Load the 5x5 grid from file, marking bonus tiles"""
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            self.grid = []
            self.bonus_tiles = set()
            
            for row_idx, line in enumerate(lines[:5]):  # Only take first 5 lines
                row = line.strip().split()
                grid_row = []
                
                for col_idx, cell in enumerate(row[:5]):  # Only take first 5 columns
                    if cell.endswith('*'):
                        # Bonus tile
                        letter = cell[:-1]
                        self.bonus_tiles.add((row_idx, col_idx))
                    else:
                        letter = cell
                    
                    # Handle both single and multi-letter tiles properly
                    grid_row.append(letter.upper())
                
                self.grid.append(grid_row)
                
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading grid: {e}")
            sys.exit(1)
    
    def _load_dictionary(self) -> None:
        """Load dictionary and build trie for fast prefix checking"""
        words = set()
        
        # Method 1: Try wordfreq library with top_n_list (much faster)
        try:
            from wordfreq import top_n_list
            word_list = top_n_list('en', 50000)  # Top 50k most common words
            for word in word_list:
                if isinstance(word, str) and len(word) >= 3 and word.isalpha():
                    words.add(word.upper())
            if len(words) > 0:
                print(f"Loaded {len(words)} words from wordfreq library")
        except (ImportError, Exception):
            pass
        
        # Method 2: Try system dictionary if wordfreq failed
        if len(words) == 0:
            dict_paths = [
                '/usr/share/dict/words',
                '/usr/dict/words',
                'C:\\Windows\\System32\\drivers\\etc\\words'
            ]
            
            for path in dict_paths:
                try:
                    with open(path, 'r') as f:
                        for line in f:
                            word = line.strip().upper()
                            if len(word) >= 3 and word.isalpha():
                                words.add(word)
                    print(f"Loaded {len(words)} words from {path}")
                    break
                except FileNotFoundError:
                    continue
        
        # Method 3: Fallback to comprehensive word list (cleaned up)
        if len(words) == 0:
            fallback_words = {
                # Common 3-letter words
                'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
                'OUR', 'HAD', 'DAY', 'GET', 'USE', 'MAN', 'NEW', 'NOW', 'WAY', 'MAY', 'SAY', 'SHE',
                'TWO', 'HOW', 'ITS', 'WHO', 'OIL', 'SIT', 'SET', 'RUN', 'EAT', 'FAR', 'SEA', 'EYE',
                'YET', 'ASK', 'TRY', 'TEA', 'KEY', 'YES', 'LET', 'HIS', 'HAS', 'HIT', 'HOT', 'PUT',
                'CUT', 'LAY', 'TOP', 'LOT', 'SUN', 'SKY', 'RED', 'NET', 'PET', 'ART', 'EAR', 'END',
                'LEG', 'ELK', 'EEL', 'ALE', 'ASH', 'HEN', 'PEE', 'PEN', 'LAD', 'HAY', 'LAP',
                'HEP', 'AHS', 'ELS', 'ERE', 'ERR', 'HEY', 'PEA', 'REP', 'LEA', 'AYE', 'YEA', 'YEP',
                'SUP', 'UPS', 'NUT', 'TUN', 'SON', 'TON', 'TEN', 'WET', 'BET', 'MET', 'POT', 'ROT',
                
                # 4+ letter words commonly found in word games
                'TELL', 'CALL', 'KEEP', 'LAST', 'PART', 'TAKE', 'MAKE', 'WORK', 'KNOW', 'PLACE',
                'YEAR', 'BACK', 'THINK', 'GOOD', 'LIFE', 'WORLD', 'HAND', 'HIGH', 'LOOK', 'HOUSE',
                'POINT', 'WATER', 'GREAT', 'WHERE', 'HELP', 'MUCH', 'LINE', 'RIGHT', 'MOVE', 'THING',
                'SCHOOL', 'STUDY', 'STILL', 'LEARN', 'PLANT', 'COVER', 'FOOD', 'UNDER', 'NEVER',
                'START', 'CITY', 'EARTH', 'EYES', 'LIGHT', 'HEAD', 'STORY', 'BEGAN', 'ALWAYS',
                'PAPER', 'GROUP', 'OFTEN', 'CHILDREN', 'SIDE', 'FEET', 'MILE', 'NIGHT', 'WALK',
                'WHITE', 'GROW', 'TOOK', 'RIVER', 'FOUR', 'CARRY', 'STATE', 'ONCE', 'BOOK', 'HEAR',
                'STOP', 'SECOND', 'LATER', 'IDEA', 'ENOUGH', 'FACE', 'FACT', 'LEAVE', 'TURN',
                'CLOSE', 'SEEM', 'HARD', 'OPEN', 'BEGIN',
                
                # Words that might be in the given grid
                'JADE', 'JEER', 'JELL', 'JEST', 'SAIL', 'SALE', 'SAND', 'SASH', 'REEL', 'EARL',
                'EASE', 'EAST', 'DEEP', 'DEER', 'DELL', 'HELD', 'HEEL', 'HELL', 'HELP', 'KELP',
                'KEEL', 'LEAP', 'LEER', 'PEAL', 'PEAR', 'PEER', 'PEEL', 'PEEP', 'SEEP',
                'SEED', 'SEEK', 'SEEM', 'SEEN', 'SEER', 'ELSE', 'ELKS', 'HEAL', 'HEAT', 'HEAR',
                'HALE', 'HAYS', 'YEAS', 'YAKS', 'TALE', 'TEAL', 'TEAM', 'TEAR', 'TEARS', 'EELS',
                'EASES', 'USED', 'USER', 'USES', 'TRUE', 'EONS', 'EROS', 'EURO',
                'SURE', 'SOUR', 'SOUL', 'SONY', 'SOLE', 'SOLO', 'LOSE', 'LOST', 'LOTS', 'LUST',
                'NUTS', 'RUNT', 'RUNS', 'NUNS', 'LENS', 'TENS', 'NETS', 'LETS', 'PETS', 'PEST',
                'REST', 'NEST', 'TEST', 'BEST', 'JEST', 'LEST', 'WEST'
            }
            words = fallback_words
            print(f"Using fallback dictionary with {len(words)} words")
        
        # Build trie from dictionary
        print("Building trie...")
        start_time = time.time()
        for word in words:
            self.trie.insert(word)
        trie_time = time.time() - start_time
        print(f"Trie built in {trie_time:.3f}s")
    
    def _precompute_adjacency(self) -> None:
        """Precompute neighbor lookup table for all grid positions"""
        self.neighbors = {}
        for row in range(self.rows):
            for col in range(self.cols):
                neighbors = []
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:  # Skip current position
                            continue
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                            neighbors.append((new_row, new_col))
                self.neighbors[(row, col)] = neighbors
    
    def _calculate_base_score(self, length: int) -> int:
        """Calculate base score based on word length"""
        if length == 3:
            return 1
        elif length == 4:
            return 6
        elif length == 5:
            return 8
        elif length == 6:
            return 10
        elif length == 7:
            return 12
        else:  # 8+ letters
            return 14
    
    def _dfs_optimized(self, row: int, col: int, visited: Set[Tuple[int, int]], 
                      trie_node: TrieNode, buffer: List[str], 
                      path: List[Tuple[int, int]], found_words: Dict[str, Tuple[List[Tuple[int, int]], int]]) -> None:
        """Optimized DFS with trie-based pruning and buffer for string building"""
        
        char = self.grid[row][col]
        
        # Check if this character can extend any word (trie pruning)
        if char not in trie_node.children:
            return  # Prune this branch - no words start with this prefix
        
        # Add current position to path
        buffer.append(char)
        path.append((row, col))
        visited.add((row, col))
        
        # Move to next trie node
        next_node = trie_node.children[char]
        
        # Check if current word is valid (3+ letters and is a complete word)
        if len(buffer) >= 3 and next_node.is_word:
            word = ''.join(buffer)
            if word not in found_words:
                # Calculate score
                base_score = self._calculate_base_score(len(word))
                bonus_score = sum(3 for pos in path if pos in self.bonus_tiles)
                total_score = base_score + bonus_score
                found_words[word] = (path.copy(), total_score)
        
        # Continue searching if we haven't used all tiles (max 25 for 5x5 grid)
        if len(buffer) < 25:
            for next_row, next_col in self.neighbors[(row, col)]:
                if (next_row, next_col) not in visited:
                    self._dfs_optimized(next_row, next_col, visited, next_node, 
                                      buffer, path, found_words)
        
        # Backtrack
        buffer.pop()
        path.pop()
        visited.remove((row, col))
    
    def find_all_words(self) -> Dict[str, Tuple[List[Tuple[int, int]], int]]:
        """Find all valid words in the grid using optimized DFS with trie pruning"""
        found_words = {}
        
        print("Searching for words...")
        start_time = time.time()
        
        # Try starting from each position in the grid
        for row in range(self.rows):
            for col in range(self.cols):
                visited = set()
                buffer = []
                path = []
                
                self._dfs_optimized(row, col, visited, self.trie.root, 
                                  buffer, path, found_words)
        
        search_time = time.time() - start_time
        print(f"Word search completed in {search_time:.3f}s")
        
        return found_words
    
    def format_path(self, path: List[Tuple[int, int]]) -> str:
        """Format the path for display"""
        return " → ".join(f"({r},{c})" for r, c in path)
    
    def display_grid(self) -> None:
        """Display the current grid with coordinates"""
        print("\nCurrent Grid:")
        print("   ", end="")
        for c in range(self.cols):
            print(f"  {c} ", end="")
        print()
        
        for r in range(self.rows):
            print(f"{r}  ", end="")
            for c in range(self.cols):
                letter = self.grid[r][c]
                if (r, c) in self.bonus_tiles:
                    letter += "*"
                print(f" {letter:2} ", end="")
            print()
        print()
    
    def play(self) -> None:
        """Main game function"""
        print("🎮 Wordbox Game - Optimized Word Finder")
        print("=" * 50)
        
        self.display_grid()
        
        start_time = time.time()
        found_words = self.find_all_words()
        total_time = time.time() - start_time
        
        if not found_words:
            print("No valid words found!")
            return
        
        # Sort by score (descending) then alphabetically
        sorted_words = sorted(found_words.items(), 
                            key=lambda x: (-x[1][1], x[0]))
        
        print(f"\nFound {len(sorted_words)} valid words in {total_time:.3f}s total:")
        print("=" * 50)
        
        # Display up to 30 words
        for i, (word, (path, score)) in enumerate(sorted_words[:30]):
            bonus_tiles_used = sum(1 for pos in path if pos in self.bonus_tiles)
            bonus_indicator = f" (+{bonus_tiles_used * 3} bonus)" if bonus_tiles_used > 0 else ""
            
            print(f"{i+1:2d}. {word:15} | Score: {score:2d}{bonus_indicator}")
            print(f"     Path: {self.format_path(path)}")
            
            # Show which letters are bonus tiles
            if bonus_tiles_used > 0:
                bonus_positions = [pos for pos in path if pos in self.bonus_tiles]
                print(f"     Bonus tiles: {', '.join(f'({r},{c})' for r, c in bonus_positions)}")
            print()
        
        if len(sorted_words) > 30:
            print(f"... and {len(sorted_words) - 30} more words found!")
        
        print(f"\n⚡ Performance: Found {len(sorted_words)} words in {total_time:.3f}s")


def main():
    """Main entry point"""
    try:
        print("🚀 Starting Optimized Wordbox Game...")
        game = WordboxGame()
        game.play()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()