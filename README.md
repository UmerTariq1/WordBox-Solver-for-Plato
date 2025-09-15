# 🎮 Wordbox/Boggle Game Solver

A fast, interactive web application that finds all valid words in a 5×5 letter grid following adjacency rules.
Originally designed to solve the Plato games 5x5 english games.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Play%20Now-blue?style=for-the-badge)](https://umertariq1.github.io/WordBox-Solver-for-Plato/)

## 🚀 Quick Start

1. **Visit [Live Demo](https://umertariq1.github.io/WordBox-Solver-for-Plato/)** or open `index.html` in any modern web browser
2. **Enter your 5×5 grid** in the left panel (or use the pre-filled example)
3. **Click Calculate** to find all words instantly
4. **Click any word** in the results to see its path visualization
5. **Easy navigation** when you click on a word to see its path, you can navigate to the next or previous word by clicking on the arrow buttons or pressing left or right keys. 

That's it! No installation required.

## 🧠 How I use it for Plato Wordbox

1. Take a screenshot of the Plato Wordbox 5×5 grid.
2. Upload the image to an LLM (e.g., ChatGPT, Gemini) and tell it:
   - It's a 5×5 matrix of letters
   - Extract the grid as lines of 5 space‑separated items
   - Respond with the grid only (no extra text)
3. Copy the extracted grid and paste it into the [my website/application ](https://umertariq1.github.io/WordBox-Solver-for-Plato/)
4. Click Calculate.
5. Make the words shown and use the left/right arrow buttons to move to previous/next word.

## 🎯 Features

- ⚡ **Instant Results** - Finds 300+ words in milliseconds
- 🎨 **Interactive Grid** - Visual representation with bonus tiles
- 🔍 **Path Visualization** - Click words to see formation paths
- 📱 **Mobile Responsive** - Works on all devices
- 🎮 **Clean UI** - Modern, intuitive interface

## 🎮 How to Play

### Grid Format
```
A T A N O
C H L A O
E N H E V*
R Qu N R E
O Y H C H
```

- **Letters**: Separate with spaces
- **Bonus tiles**: Add `*` after letter (e.g., `V*`)
- **Multi-letter tiles**: Supported (e.g., `Qu`, `Th`)
- **Grid size**: Must be exactly 5×5

### Game Rules

1. **Word Formation**: Connect adjacent letters (8 directions)
2. **Minimum Length**: At least 3 letters
3. **No Reuse**: Each tile used only once per word
4. **Valid Words**: Must be in dictionary

### Scoring System

| Word Length | Base Points |
|-------------|-------------|
| 3 letters   | 1 point     |
| 4 letters   | 6 points    |
| 5 letters   | 8 points    |
| 6 letters   | 10 points   |
| 7 letters   | 12 points   |
| 8+ letters  | 14 points   |

**Bonus**: +3 points per bonus tile used (marked with `*`)

## 💡 Tips

- **Longer words** score significantly more points
- **Bonus tiles** provide substantial score boosts
- **Look for** common prefixes and suffixes
- **Try different** starting positions for each word
- **Use the visualization** to understand valid paths

## 🔧 Technical Details

- **Algorithm**: Optimized Depth-First Search with Trie pruning
- **Dictionary**: Comprehensive English word list
- **Performance**: Sub-millisecond search times
- **Browser Support**: All modern browsers
- **No Dependencies**: Pure HTML, CSS, JavaScript

## 📄 File Structure

```
wordbox/
├── index.html          # Complete web application
└── README.md          # This file
```

---

**🌟 Start solving word grids instantly!** No setup, no installation - just open and play.