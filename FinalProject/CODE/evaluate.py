from syllable_count_distance import get_line_syllable_count_distance
from phoneme_repetition_similarity import get_phoneme_repetition_similarity
from musical_structure_distance import get_musical_structure_distance
from semantic_similarity import get_semantic_similarity
from rhyme_scheme_distance import get_rhyme_scheme_mapping_distance
from sound_comparer import get_phoneme_edit_distance, get_phoneme_bigrams_distance
from lyrics_aligner import get_aligned_translation
import os
import lzma
import pickle


def score_function(czech_sections : list[list[str]], english_sections : list[list[str]]) -> float:
    """
    Expects line aligned lyrics

    Sections divided by empty lines
    """

    score = []

    print("The Metric modified for czech and english texts:")

    line_syllable_count_distance = get_line_syllable_count_distance(czech_sections, english_sections)
    print("line syllable count distance: ", line_syllable_count_distance)
    score.append(line_syllable_count_distance)

    phoneme_repetition_correlation = get_phoneme_repetition_similarity(czech_sections, english_sections)
    print("Phoneme repetition correlation: ", phoneme_repetition_correlation)
    score.append(phoneme_repetition_correlation)

    musical_structure_distance = get_musical_structure_distance(czech_sections, english_sections)
    print("musical structure distance: ", musical_structure_distance)
    score.append(musical_structure_distance)

    semantic_similarity = get_semantic_similarity(czech_sections, english_sections)
    print("semantic similarity: ", semantic_similarity)
    score.append(semantic_similarity)


    
    print("\nMy own experiments:")

    rhyme_scheme_mapping_distance = get_rhyme_scheme_mapping_distance(czech_sections, english_sections)
    print("rhyme scheme mapping distance: ", rhyme_scheme_mapping_distance)
    score.append(rhyme_scheme_mapping_distance)

    phoneme_edit_distance = get_phoneme_edit_distance(czech_sections, english_sections)
    print("phoneme edit distance: ", phoneme_edit_distance)
    score.append(phoneme_edit_distance)

    phoneme_bigrams_distance = get_phoneme_bigrams_distance(czech_sections, english_sections)
    print("phoneme bigrams distance: ", phoneme_bigrams_distance)
    score.append(phoneme_bigrams_distance)

    return score




# def evaluate_original_and_translations(song_name):
#     print("\n\nEvaluating", song_name, "\n\n")
#     with open("C:/Users/barca/MOJE/ROCNIKAC/rp-barbora-stepankova/DATA/Musicals/" + song_name + "_cs.txt", "r", encoding="utf-8") as f:
#         text_cs = f.read()

#     with open("C:/Users/barca/MOJE/ROCNIKAC/rp-barbora-stepankova/DATA/Musicals/" + song_name + "_en.txt", "r", encoding="utf-8") as f:
#         text_en = f.read()

#     czech_sections, english_sections = align_lyrics_by_section_and_line(text_cs, text_en)

#     if len(czech_sections) != len(english_sections):
#         raise ValueError("The lyrics differ in number of sections.")

#     print("og lyrics:")
#     score_function(czech_sections, english_sections)


#     print("\n\n\ntranslated lyrics czech:")
#     score_function(czech_sections, get_aligned_translation(czech_sections, "cz"))


#     print("\n\n\ntranslated lyrics english:")
#     score_function(get_aligned_translation(english_sections, "en"), english_sections)



# evaluate_original_and_translations("frozen_01")
# evaluate_original_and_translations("frozen_02")
# evaluate_original_and_translations("frozen_03")

# evaluate_original_and_translations("moana_01")



# with lzma.open("C:/Users/barca/MOJE/UMEA/NLP-Umea/FinalProject/DATA/results.dict", "rb") as model_file:
#     model = pickle.load(model_file)





scores = {}
scores["HT"] = []
scores["cz_to_en"] = []
scores["en_to_cz"] = []

filenames = os.listdir("C:/Users/barca/MOJE/UMEA/NLP-Umea/FinalProject/DATA/Aligned_HT") 
lst = list(range(len(filenames)))
indicies = lst[0::10]


czech_og = []
counter = 0

filenames = ["frozen_03_cs.txt"]

for filename in filenames:

    # if counter not in indicies and counter - 1 not in indicies:
    #     counter += 1
    #     continue

    og_sections = []
    with open("C:/Users/barca/MOJE/UMEA/NLP-Umea/FinalProject/DATA/Aligned_HT/" + filename , "r", encoding="utf-8") as f:
        lines = f.readlines()
        temp = []
        for line in lines:
            line = line[:-1]
            if line == "":
                og_sections.append(temp.copy())
                temp.clear()
            else:
                temp.append(line)

    english_sections = get_aligned_translation(og_sections, "en")

    for sec in english_sections:
        for line in sec:
            print(line)
        print()

    

    if filename[-6:] == "en.txt":
        print("\n\n" + filename[:-7] + " from english to czech:")
        czech_sections = get_aligned_translation(og_sections, "cz")
        scores["en_to_cz"].append(score_function(czech_sections, og_sections))
        
        print("\n\n" + filename[:-7] + " - the original HT lyrics:")
        scores["HT"].append(score_function(czech_og, og_sections))
    else:
        print("\n\n" + filename[:-7] + " from czech to english:")
        english_sections = get_aligned_translation(og_sections, "en")
        scores["cz_to_en"].append(score_function(og_sections, english_sections))
        czech_og = og_sections

    counter += 1



# Serialize the model.
with lzma.open("C:/Users/barca/MOJE/UMEA/NLP-Umea/FinalProject/DATA/results.dict", "wb") as model_file:
    pickle.dump(scores, model_file)


        


















# title = "encanto_01"

# czech_sections = []
# english_sections = []

# with open("C:/Users/barca/MOJE/UMEA/NLP-Umea/FinalProject/DATA/Aligned_HT/" + title + "_cs.txt", "r", encoding="utf-8") as f:
#     lines = f.readlines()
#     temp = []
#     for line in lines:
#         line = line[:-1]
#         if line == "":
#             czech_sections.append(temp.copy())
#             temp.clear()
#         else:
#             temp.append(line)

# with open("C:/Users/barca/MOJE/UMEA/NLP-Umea/FinalProject/DATA/ChatGPT_translations/" + title + "_ch_en.txt", "r", encoding="utf-8") as f:
#     lines = f.readlines()
#     temp = []
#     for line in lines:
#         line = line[:-1]
#         if line == "":
#             english_sections.append(temp.copy())
#             temp.clear()
#         else:
#             temp.append(line)




# # for section_i in range(len(czech_sections)):
# #     while section_i >= len(english_sections):
# #         print(english_sections)
# #     for line_i in range(min(len(czech_sections[section_i]), len(english_sections[section_i]))):
# #         diff = len(syllabify(czech_sections[section_i][line_i], "cz")) - len(syllabify(english_sections[section_i][line_i], "en"))
# #         print(czech_sections[section_i][line_i], " --- ", english_sections[section_i][line_i], "--->", diff)
# #     print()
