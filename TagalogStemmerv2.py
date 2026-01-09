import sys

""" 
    CONSTANTS 
"""
VOWELS = "aeiouAEIOU"
CONSONANTS = "bcdfghklmnngpqrstvwyBCDFGHKLMNNGPQRSTVWY"

""" 
    Affixes
"""
PREFIX_SET = [
    'ikinapagpapaka',  # 7 syllables - longest prefix
    'nakikipag', 'pakikipag',
    'pinakama', 'pagpapa',
    'pinagka', 'panganga', 
    'makapag', 'nakapag', 
    'tagapag', 'makipag', 
    'nakipag', 'tigapag',
    'pakiki', 'magpa',
    'napaka', 'pinaka',
    'ipinag', 'pagka', 
    'pinag', 'mapag', 
    'mapa', 'taga', 
    'ipag', 'tiga', 
    'pala', 'pina', 
    'pang', 'naka',
    'nang', 'mang',
    'sing',
    'ipa', 'pam',
    'pan', 'pag',
    'tag', 'mai',
    'mag', 'nam',
    'nag', 'man',
    'may', 'ma',
    'na', 'ni',
    'pa', 'ka',
    'um', 'in',
    'i',
]

INFIX_SET = [
    'um', 'in',
]

SUFFIX_SET = [
    'hin',  # for words ending in consonant
    'han',  # for words ending in consonant
    'an',   # for words ending in vowel
    'in',   # for words ending in vowel
]

PERIOD_FLAG = True
PASS_FLAG = False

def stemmer(source):
    """ 
        Stems the tokens in a sentence.
        source: the string 
        returns LIST
    """

    global PERIOD_FLAG
    global PASS_FLAG

    word_info    = {}
    stemmed      = []
    
    pre_stem     = inf_stem = suf_stem = rep_stem = \
        du1_stem = du2_stem = cle_stem = '-'

    PREFIX     = []
    INFIX      = []
    SUFFIX     = []
    DUPLICATE  = []
    REPITITION = []
    CLEANERS   = []

    # Directly split the source string (Removed Mode Logic)
    tokens = source.split(' ')

    for token in tokens:        
        word_info["word"] = token
        
        # Accept both uppercase and lowercase inputs
        if token[0].isalpha():
            token    = token.lower()        
            du1_stem = clean_duplication(token, DUPLICATE)
            pre_stem = clean_prefix(du1_stem, PREFIX)
            rep_stem = clean_repitition(pre_stem, REPITITION)
            inf_stem = clean_infix(rep_stem, INFIX)
            rep_stem = clean_repitition(inf_stem, REPITITION)
            suf_stem = clean_suffix(rep_stem, SUFFIX)
            du2_stem = clean_duplication(suf_stem, DUPLICATE)
            cle_stem = clean_stemmed(du2_stem, CLEANERS, REPITITION)
            cle_stem = clean_duplication(cle_stem, DUPLICATE)

            if '-' in cle_stem:
                cle_stem = cle_stem.replace('-', '')

            # if stemmed is wrong, go to 2nd pass
            if check_validation(cle_stem) == False:
                PASS_FLAG = True
                du1_stem  = clean_duplication(cle_stem, DUPLICATE)
                pre_stem  = clean_prefix(du1_stem, PREFIX)
                rep_stem  = clean_repitition(pre_stem, REPITITION)
                inf_stem  = clean_infix(rep_stem, INFIX)
                rep_stem  = clean_repitition(inf_stem, REPITITION)
                suf_stem  = clean_suffix(rep_stem, SUFFIX)
                du2_stem  = clean_duplication(suf_stem, DUPLICATE)
                cle_stem  = clean_stemmed(du2_stem, CLEANERS, REPITITION)
                cle_stem  = clean_duplication(cle_stem, DUPLICATE)

            word_info["root"]   = cle_stem
            word_info["prefix"] = PREFIX
            word_info["infix"]  = INFIX
            word_info["suffix"] = SUFFIX
            word_info["repeat"] = REPITITION
            word_info["dupli"]  = DUPLICATE
            word_info["clean"]  = CLEANERS

            PASS_FLAG   = False
            PERIOD_FLAG = False
            PREFIX      = []
            INFIX       = []
            SUFFIX      = []
            DUPLICATE   = []
            REPITITION  = []
            CLEANERS    = []

        else:
            PERIOD_FLAG = False
            cle_stem = clean_stemmed(token, CLEANERS, REPITITION)
            word_info["root"]   = token
            word_info["prefix"] = '[]'
            word_info["infix"]  = '[]'
            word_info["suffix"] = '[]'
            word_info["repeat"] = '[]'
            word_info["dupli"]  = '[]'
            word_info["clean"]  = '[]'

        stemmed.append(word_info)
        
        # Simple output format: Original : Root
        print(token + ' : ' + word_info["root"])

        word_info = {}
        pre_stem = inf_stem = suf_stem = rep_stem = \
        du1_stem = du2_stem = cle_stem = '-'

    return stemmed


def clean_duplication(token, DUPLICATE):
    """
        Checks token for duplication. (ex. araw-araw = araw)
    """
    if check_validation(token):
        return token

    if '-' in token and token.index('-') != 0 and \
        token.index('-') != len(token) -  1:

        split = token.split('-')

        if all(len(tok) >= 3 for tok in split):
            if split[0] == token[1] or split[0][-1] == 'u' and change_letter(split[0], -1, 'o') == split[1] or \
                split[0][-2] == 'u' and change_letter(split[0], -2, 'o')  == split[1]:
                DUPLICATE.append(split[0])
                return split[0]

            elif split[0] == split[1][0:len(split[0])]:
                DUPLICATE.append(split[1])
                return split[1]

            elif split[0][-2:] == 'ng':
                if split[0][-3] == 'u':
                    if split[0][0:-3] + 'o' == split[1]:
                        DUPLICATE.append(split[1])
                        return split[1]

                if split[0][0:-2] == split[1]:
                    DUPLICATE.append(split[1])
                    return split[1]

        else:
            return '-'.join(split)
    
    return token


def clean_repitition(token, REPITITION):
    """
        Checks token for repitition. (ex. nakakabaliw = nabaliw)
    """
    if check_validation(token):
        return token

    if len(token) >= 4:
        if check_vowel(token[0]):
            if token[0] == token[1]:
                REPITITION.append(token[0])
                return token[1:]

        elif check_consonant(token[0]) and count_vowel(token) >= 2:
            if token[0: 2] == token[2: 4] and len(token) - 2 >= 4:
                REPITITION.append(token[2:4])
                return token[2:]
            
            elif token[0: 3] == token[3: 6] and len(token) - 3 >= 4:
                REPITITION.append(token[3:6])
                return token[3:]

    return token


def clean_prefix(token,  PREFIX):
    """
        Checks token for prefixes with morphophonemic rules:
        - Hyphenation: consonant/consonant (no hyphen), consonant/vowel (hyphen)
        - Phoneme /d/ -> /r/ when between vowels in prefixation
        Example: maG + Sama = magsama, maG + Away = mag-away
    """
    if check_validation(token):
        return token

    for prefix in PREFIX_SET:
        if len(token) - len(prefix) >= 3 and \
            count_vowel(token[len(prefix):]) >= 2:

            if prefix == ('i') and check_consonant(token[2]):
                continue

            # Handle hyphenated prefixes (consonant/vowel boundary)
            if '-' in token:    
                parts = token.split('-')

                if parts[0] == prefix and check_vowel(parts[1][0]):
                    PREFIX.append(prefix)
                    return parts[1]

                token = '-'.join(parts)

            if token[0: len(prefix)] == prefix:
                remaining = token[len(prefix):]
                
                if count_vowel(remaining) >= 2:
                    
                    if prefix == 'panganga':
                        PREFIX.append(prefix)
                        return 'ka' + remaining
                    
                    # Morphophonemic: restore /r/ -> /d/ when /d/ was between vowels
                    if len(remaining) > 0 and remaining[0] == 'r' and \
                       len(prefix) > 0 and check_vowel(prefix[-1]):
                        PREFIX.append(prefix)
                        return 'd' + remaining[1:]
                    
                    PREFIX.append(prefix)
                    return remaining

    return token

 
def clean_infix(token, INFIX):
    """
        Checks token for infixes (/-in-/ and /-um-/):
        - Infix occurs after first consonant of root word
        - /-in-/ can also appear after first consonant of prefix
        Example: b-um-ili = bili, s-in-ulat = sulat
    """
    if check_validation(token):
        return token

    for infix in INFIX_SET:
        infix_len = len(infix)
        
        if len(token) - infix_len >= 3 and count_vowel(token[infix_len:]) >= 2:
            
            # Standard case: infix after first consonant of root/prefix
            # Check if first character is consonant and infix follows
            if check_consonant(token[0]) and token[1:1+infix_len] == infix:
                remaining = token[0] + token[1+infix_len:]
                if count_vowel(remaining) >= 2:
                    INFIX.append(infix)
                    return remaining
            
            # Duplication with infix pattern
            if token[0] == token[4] and token[1: 4] == infix:
                INFIX.append(infix)
                return token[4:]

            elif token[2] == token[4] and token[1: 3] == infix:
                INFIX.append(infix)
                return token[0] + token[3:]

            elif token[1: 3] == infix and check_vowel(token[3]):
                INFIX.append(infix)
                return token[0] + token[3:]

    return token


def clean_suffix(token, SUFFIX):
    """
        Checks token for suffixes with morphophonemic rules:
        - /-in/ or /-an/ for words ending with vowel
        - /-hin/ or /-han/ for words ending with consonant
        - Phoneme /r/ -> /d/ in final position (restoration when suffixed by -in/-an)
        - Phoneme /u/ -> /o/ in last syllable (restoration)
        Example: bigayan = bigay, basahin = basa
    """
    SUF_CANDIDATE = []

    if check_validation(token):
        return token
    
    for suffix in SUFFIX_SET:
        suffix_len = len(suffix)
        if len(token) - suffix_len >= 3:
            remaining = token[0:len(token) - suffix_len]
            
            if token[-suffix_len:] == suffix and count_vowel(remaining) >= 2:
                
                # Apply morphophonemic restoration rules
                restored_root = remaining
                
                # Rule 1: Restore /r/ -> /d/ in final position (for -in/-an suffixes)
                if suffix in ['in', 'an'] and len(restored_root) > 0 and restored_root[-1] == 'r':
                    restored_root = change_letter(restored_root, -1, 'd')
                
                # Rule 2: Restore /u/ -> /o/ in last syllable
                if len(restored_root) >= 2:
                    # Check if 'u' is in last syllable (before consonant or as last letter)
                    if check_consonant(restored_root[-1]) and restored_root[-2] == 'u':
                        restored_root = change_letter(restored_root, -2, 'o')
                    elif restored_root[-1] == 'u':
                        restored_root = change_letter(restored_root, -1, 'o')
                
                if check_validation(restored_root):
                    SUFFIX.append(suffix)
                    return restored_root
                elif len(SUF_CANDIDATE) == 0:
                    SUF_CANDIDATE.append(suffix)
                    SUF_CANDIDATE.append(restored_root)

    if len(SUF_CANDIDATE) == 2:
        SUFFIX.append(SUF_CANDIDATE[0])
        return SUF_CANDIDATE[1]

    return token


def check_vowel(substring):
    return all(letter in VOWELS for letter in substring)


def check_consonant(substring):
    return all(letter in CONSONANTS for letter in substring)


def count_vowel(token):
    count = 0
    for tok in token:
        if check_vowel(tok):
            count+=1
    return count


def count_consonant(token):
    count = 0
    for tok in token:
        if check_consonant(tok):
            count+=1
    return count


def change_letter(token, index, letter):
    _list = list(token)
    _list[index] = letter
    return ''.join(_list)


def clean_stemmed(token, CLEANERS, REPITITION):
    """
        Checks for left-over affixes and morphophonemic changes.
    """
    global PERIOD_FLAG
    global PASS_FLAG

    CC_EXP = ['dr', 'gl', 'gr', 'ng', 'kr', 'kl', 'kw', 'ts', 'tr', 'pr', 'pl', 'pw', 'sw', 'sy'] 

    if token[-1] == '.' and PASS_FLAG == False:
        PERIOD_FLAG = True

    if not check_vowel(token[-1]) and not check_consonant(token[-1]):
        CLEANERS.append(token[-1])
        token = token[0:-1]

    if not check_vowel(token[0]) and not check_consonant(token[0]):
        CLEANERS.append(token[0])
        token = token[1:]

    if check_validation(token):
        return token

    if len(token) >= 3 and count_vowel(token) >= 2:
        token = clean_repitition(token, REPITITION)

        # Restore 'u' to 'o' if it was the 2nd to last letter
        if check_consonant(token[-1]) and token[- 2] == 'u':
            CLEANERS.append('u')
            token = change_letter(token, -2, 'o')

        # Restore 'u' to 'o' if it was the last letter
        if token[len(token) - 1] == 'u':
            CLEANERS.append('u')
            token = change_letter(token, -1, 'o')

        # Restore 'r' to 'd' (Morphophonemic change)
        if token[-1] == 'r':
            CLEANERS.append('r')
            token = change_letter(token, -1, 'd')

        if token[-1] == 'h' and check_vowel(token[-1]):
            CLEANERS.append('h')
            token = token[0:-1]

        if token[0] == token[1]:
            CLEANERS.append(token[0])
            token = token[1:]

        if (token[0: 2] == 'ka' or token[0: 2] == 'pa') and check_consonant(token[2]) \
            and count_vowel(token) >= 3:
            
            CLEANERS.append(token[0: 2])
            token = token[2:]

        if(token[-3:]) == 'han' and count_vowel(token[0:-3]) == 1:
            CLEANERS.append('han')
            token = token[0:-3] + 'i'

        if(token[-3:]) == 'han' and count_vowel(token[0:-3]) > 1:
            CLEANERS.append('han')
            token = token[0:-3]

        if len(token) >= 2 and count_vowel(token) >= 3:
            if token[-1] == 'h' and check_vowel(token[-2]):
                CLEANERS.append('h')
                token = token[0:-1]

        if len(token) >= 6 and token[0:2] == token[2:4]:
            CLEANERS.append('0:2')
            token = token[2:]

        if any(REP[0] == 'r' for REP in REPITITION):
            CLEANERS.append('r')
            token = change_letter(token, 0, 'd')

        if token[-2:] == 'ng' and token[-3] == 'u':
            CLEANERS.append('u')
            token = change_letter(token, -3, 'o')

        if token[-1] == 'h':
            CLEANERS.append('h')
            token = token[0:-1]

        if any(token[0:2] != CC for CC in CC_EXP) and check_consonant(token[0:2]):
            CLEANERS.append(token[0:2])
            token = token[1:]

    return token


def check_validation(token):
    try:
        # Try UTF-16 encoding first (common for Windows files), then UTF-8
        try:
            with open('validation.txt', 'r', encoding='utf-16') as valid:
                data = valid.read().replace('\n', ' ').split(' ')
        except UnicodeError:
            with open('validation.txt', 'r', encoding='utf-8') as valid:
                data = valid.read().replace('\n', ' ').split(' ')
        return True if token in data else False
    except FileNotFoundError:
        # If no validation file exists, assume validation fails
        return False


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("=" * 60)
    print("TAGALOG STEMMER - Interactive Mode")
    print("=" * 60)
    print("This stemmer removes affixes from Tagalog words.")
    print("Enter a Tagalog word to get its root form.")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        try:
            # Get user input
            user_input = input("Enter a Tagalog word: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'q', '']:
                print("\nThank you for using Tagalog Stemmer! Goodbye!")
                break
            
            # Process the word
            result = stemmer(user_input)
            
            # Display results
            if result and len(result) > 0:
                word_data = result[0]
                print("\n" + "-" * 60)
                print(f"Original Word: {word_data['word']}")
                print(f"Root Word:     {word_data['root']}")
                
                # Show detected affixes
                affixes_found = []
                if word_data['prefix']:
                    affixes_found.append(f"Prefix: {word_data['prefix']}")
                if word_data['infix']:
                    affixes_found.append(f"Infix: {word_data['infix']}")
                if word_data['suffix']:
                    affixes_found.append(f"Suffix: {word_data['suffix']}")
                if word_data['repeat']:
                    affixes_found.append(f"Repetition: {word_data['repeat']}")
                if word_data['dupli']:
                    affixes_found.append(f"Duplication: {word_data['dupli']}")
                
                if affixes_found:
                    print("Affixes Found: " + ", ".join(affixes_found))
                else:
                    print("Affixes Found: None (word may already be in root form)")
                print("-" * 60 + "\n")
            else:
                print("No result returned.\n")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")