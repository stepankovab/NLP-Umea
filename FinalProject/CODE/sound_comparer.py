import Imports.tagger as tagger
import re

from Imports.phon_czech import ipa_czech
import eng_to_ipa as ipa

strong_similarity = {
    ('aː', 'a'),
    ('ɛː', 'ɛ'),
    ('ɛː', 'ə'),
    ('ɛː', 'æ'),
    ('iː', 'i'),
    ('iː', 'ɪ'),
    ('oː', 'ɔ'),
    ('uː', 'u'),
    ('uː', 'ʊ'),
    ('u', 'ʊ'),
    ('yː', 'y'),
    ('ə', 'a'),
    ('ə', 'aː'),
    ('ə', 'ɛ'),
    ('ɛ', 'æ'),
    ('m', 'n'),
    ('ŋ', 'n'),
    ('ŋ', 'm'),
    ('t͡s', 'c'),
    ('ð', 'd'),
    ('o', 'ɔ')
}

vocals = {'aː', 'a', 'ɛː', 'ɛ', 'ə', 'æ', 'iː', 'i', 'ɪ', 'oː', 'ɔ', 'o', 'uː', 'u', 'ʊ', 'yː', 'y'}


def get_line_bigram_probabilities(phonemes : list[str]) -> dict[str, float]:
    bigram_dict = {}
    bigram_count = 0
    
    for p in range(len(phonemes) - 1):
        bigram = phonemes[p] + phonemes[p + 1]
        bigram_count += 1

        if bigram not in bigram_dict:
            bigram_dict[bigram] = 0
        
        bigram_dict[bigram] += 1
    
    for bigram in bigram_dict.keys():
        bigram_dict[bigram] /= bigram_count

    return bigram_dict



# TODO make this function actually work xdd
# Unification?
def get_distance_between_bigram_probabilities_dict(czech_dict : dict[str, float], english_dict : dict[str, float]) -> float:
    bigram_dict = {}

    for bigram in czech_dict.keys():
        if bigram not in bigram_dict:
            bigram_dict[bigram] = 0
        bigram_dict[bigram] += (czech_dict[bigram] / 2) 

    for bigram in english_dict.keys():
        if bigram not in bigram_dict:
            bigram_dict[bigram] = 0
        bigram_dict[bigram] += (english_dict[bigram] / 2) 

    bigram_probability_distance = 0
    for bigram in czech_dict.keys():
        bigram_probability_distance += abs(czech_dict[bigram] - bigram_dict[bigram])
    for bigram in english_dict.keys():
        bigram_probability_distance += abs(english_dict[bigram] - bigram_dict[bigram])

    return bigram_probability_distance / (len(czech_dict) + len(english_dict))



def get_phoneme_bigrams_distance(czech_sections : list[list[str]], english_sections : list[list[str]]) -> float:
    czech_lines = []
    for section in czech_sections:
        czech_lines.extend(section)
    
    english_lines = []
    for section in english_sections:
        english_lines.extend(section)

    if len(czech_lines) != len(english_lines):
        raise ValueError("The lyrics differ in number of lines.")
    
    n_lines = len(czech_lines)
    distance_sum = 0

    for i in range(n_lines):
        czech_phonemes = ipa_czech(czech_lines[i]).split() + ["^"]
        english_phonemes = re.sub('[ˈ\s]', '', ipa.convert(english_lines[i], stress_marks='primary')) + "^"

        czech_dict = get_line_bigram_probabilities(czech_phonemes)
        english_dict = get_line_bigram_probabilities(english_phonemes)

        distance_sum += get_distance_between_bigram_probabilities_dict(czech_dict, english_dict)
    
    return distance_sum / n_lines



def get_rhyme_scheme_mapping_accuracy(czech_sections : list[list[str]], english_sections : list[list[str]]) -> float:
    
    czech_lines = []
    for section in czech_sections:
        czech_lines.extend(section)
    
    english_lines = []
    for section in english_sections:
        english_lines.extend(section)

    if len(czech_lines) != len(english_lines):
        raise ValueError("The lyrics differ in number of lines.")
    
    n_lines = len(czech_lines)

    rt_cs = tagger.RhymeTagger()
    rt_cs.load_model("C:/Users/barca/MOJE/ROCNIKAC/rp-barbora-stepankova/CODE/ExperimentsDump/rhymetagger-master/models/cs", verbose=False)
    rhymes_cs = rt_cs.tag(poem=czech_lines, output_format=1)

    rt_en = tagger.RhymeTagger()
    rt_en.load_model("C:/Users/barca/MOJE/ROCNIKAC/rp-barbora-stepankova/CODE/ExperimentsDump/rhymetagger-master/models/en", verbose=False)
    rhymes_en = rt_en.tag(poem=english_lines, output_format=1)

    czech_detected = 0
    czech_agreements = 0
    english_detected = 0
    english_agreements = 0

    for i in range(len(rhymes_cs)):
        cs_line_rhymes = rhymes_cs[i]
        en_line_rhymes = rhymes_en[i]

        for number in cs_line_rhymes:
            czech_detected += 1
            if number in en_line_rhymes:
                czech_agreements += 1
        
        for number in en_line_rhymes:
            english_detected += 1
            if number in cs_line_rhymes:
                english_agreements += 1


    if czech_detected == 0 or english_detected == 0:
        return 0.0
    
    accuracy = (czech_agreements/czech_detected + english_agreements/english_detected)/2  * max(czech_detected, english_detected) / n_lines

    return accuracy



def get_phoneme_edit_distance(czech_sections : list[list[str]], english_sections : list[list[str]]) -> float:
    
    czech_lines = []
    for section in czech_sections:
        czech_lines.extend(section)
    
    english_lines = []
    for section in english_sections:
        english_lines.extend(section)

    if len(czech_lines) != len(english_lines):
        raise ValueError("The lyrics differ in number of lines.")

    n_lines = len(czech_lines)

    distance_sum = 0

    for i in range(n_lines):
        czech_pho = ipa_czech(czech_lines[i]).split() + ["^"]
        english_pho = [*re.sub('[ˈ\s]', '', ipa.convert(english_lines[i], stress_marks='primary')) + "^"]

        # print("".join(czech_pho))
        # print("".join(english_pho))

        dist = edit_distance(czech_pho, english_pho, len(czech_pho), len(english_pho))

        distance_sum += (dist/( 2 * len(czech_pho)) + dist/(2 * len(english_pho)))
        # print((dist/( 2 * len(czech_pho)) + dist/(2 * len(english_pho))))

    return(distance_sum/n_lines)





def edit_distance(str1, str2, m, n):
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):
 
            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]

            elif (str1[i-1], str2[j-1]) in strong_similarity or (str2[j-1], str1[i-1]) in strong_similarity:
                dp[i][j] = dp[i-1][j-1] + 0.1


            elif str1[i-1] in vocals and str2[j-1] in vocals:
                dp[i][j] = dp[i-1][j-1] + 0.4


            elif str1[i-1] not in vocals and str2[j-1] not in vocals:
                dp[i][j] = dp[i-1][j-1] + 0.7        

 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace
 
    return dp[m][n]



# get_phoneme_mapping_accuracy([["Mám styl Čendy", "Nevím kde ho Čenda vzal", "Já ho sebral od něho", "A on si ho moc nehlídal"]],
#                             [["I'm still standing", "better than I've ever been", "Feeling like a true survivor", "feeling like a little kid"]])


# get_phoneme_bigrams_distance([["Mám styl Čendy", "Nevím kde ho Čenda vzal", "Já ho sebral od něho", "A on si ho moc nehlídal"]],
#                             [["I'm still standing", "better than I've ever been", "Feeling like a true survivor", "feeling like a little kid"]])