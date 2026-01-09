# Tagalog Stemmer - Google Colab Setup

## 📋 Overview
This Tagalog Stemmer removes affixes (prefixes, infixes, suffixes) from Tagalog words to extract their root forms.

## 🎯 Linguistic Rules Implemented
- **Prefixation**: 1-7 syllables (e.g., ma-, ikinapagpapaka-)
- **Suffixation**: /-in/, /-an/, /-hin/, /-han/
- **Infixation**: /-in-/, /-um-/
- **Morphophonemic Rules**: /d/↔/r/ and /o/↔/u/ transformations

## 🚀 How to Use in Google Colab

### Step 1: Upload Files
1. Open Google Colab (https://colab.research.google.com/)
2. Create a new notebook
3. Upload these files:
   - `TagalogStemmer_Colab.py`
   - `validation.txt`

**To upload files in Colab:**
```python
from google.colab import files
uploaded = files.upload()
```

### Step 2: Run the Stemmer
```python
# Method 1: Run directly
!python TagalogStemmer_Colab.py
```

OR

```python
# Method 2: Import and use
from TagalogStemmer_Colab import stemmer

# Test single word
result = stemmer("magmahal")
print(result)

# Test multiple words
words = ["magmahal", "bumili", "sinulat", "bigayan"]
for word in words:
    result = stemmer(word)
```

### Step 3: Interactive Mode
When you run the stemmer, it will prompt you for input:
```
============================================================
TAGALOG STEMMER - Interactive Mode
============================================================
This stemmer removes affixes from Tagalog words.
Enter a Tagalog word to get its root form.
Type 'exit' or 'quit' to stop.

Enter a Tagalog word: magmahal
```

### Step 4: View Results
```
------------------------------------------------------------
Original Word: magmahal
Root Word:     mahal
Affixes Found: Prefix: ['mag']
------------------------------------------------------------
```

## 📝 Example Usage

```python
from TagalogStemmer_Colab import stemmer

# Example 1: Prefix
stemmer("magmahal")  # Output: mahal

# Example 2: Infix
stemmer("bumili")    # Output: bili

# Example 3: Suffix
stemmer("bigayan")   # Output: bigay

# Example 4: Multiple affixes
stemmer("ikinapagpapakaganda")  # Output: ganda
```

## 🔍 Features

### Accepts Any Capitalization
- `magmahal` → mahal ✓
- `Magmahal` → mahal ✓
- `MAGMAHAL` → mahal ✓

### Handles Hyphenated Words
- `mag-away` → away ✓

### Detects Multiple Affix Types
- Prefixes
- Infixes
- Suffixes
- Reduplication
- Repetition

## 📊 Sample Test Cases

| Input | Root | Affixes |
|-------|------|---------|
| magmahal | mahal | Prefix: mag |
| bumili | bili | Infix: um |
| sinulat | sulat | Infix: in |
| bigayan | bigay | Suffix: an |
| basahin | basa | Suffix: hin |
| narala | dala | Prefix: na (with /d/→/r/ rule) |
| lutuin | luto | Suffix: in (with /o/→/u/ rule) |

## 🛠️ Troubleshooting

### Issue: "validation.txt not found"
**Solution**: Make sure `validation.txt` is uploaded to the same directory as the script.

### Issue: "UnicodeDecodeError"
**Solution**: The script handles both UTF-8 and UTF-16 encoding automatically.

### Issue: Word not stemming correctly
**Solution**: Check if the root word exists in `validation.txt`. Add it if missing.

## 📦 Files Included
- `TagalogStemmer_Colab.py` - Main stemmer script (interactive mode)
- `TagalogStemmerv2.py` - Original version with same functionality
- `validation.txt` - Dictionary of valid Tagalog root words
- `README_COLAB.md` - This file

## 💡 Tips for Google Colab

1. **Run in a code cell:**
   ```python
   !python TagalogStemmer_Colab.py
   ```

2. **For batch processing:**
   ```python
   from TagalogStemmer_Colab import stemmer
   
   words = ["magmahal", "bumili", "sinulat"]
   results = [stemmer(word) for word in words]
   ```

3. **To stop the interactive mode:**
   - Type `exit` or `quit`
   - Or press `Ctrl+C` (in terminal)

## 📚 References
Based on Tagalog morphological rules:
- Prefixation with morphophonemic changes
- Suffixation with vowel/consonant rules
- Infixation patterns

## 👨‍💻 Author
NLP-Diapana Project

## 📄 License
Free to use for educational purposes

---

**Enjoy stemming Tagalog words! 🇵🇭**
