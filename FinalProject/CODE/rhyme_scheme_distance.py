import Imports.tagger as tagger
from lyrics_aligner import align_lyrics_by_section_and_line, get_aligned_translation


def get_section_rhyme_scheme_distance(czech_lines : list[str], english_lines : list[str], rt_cs : tagger.RhymeTagger, rt_en : tagger.RhymeTagger) -> float:
    if len(czech_lines) != len(english_lines):
        raise ValueError("The lyrics differ in number of lines.")
    
    n_lines = len(czech_lines)

    rhymes_cs = rt_cs.tag(poem=czech_lines, output_format=1)
    rhymes_en = rt_en.tag(poem=english_lines, output_format=1)

    distance = 0
    for i in range(n_lines):
        difference = len(set(rhymes_en[i]).symmetric_difference(rhymes_cs[i]))
        distance += (difference / max(len(rhymes_cs[i]), 1)) + (difference / max(len(rhymes_en[i]), 1))

    a = abs((len(rhymes_cs) - rhymes_cs.count([])) - (len(rhymes_en) - rhymes_en.count([])))
    distance =  distance * (a + 0.5) / (2 * n_lines)

    return distance



def get_rhyme_scheme_mapping_distance(czech_sections : list[list[str]], english_sections : list[list[str]]) -> float:
    '''
    Get a distance between rhymes of two song lyrics.
    '''
    rt_cs = tagger.RhymeTagger()
    rt_cs.load_model("cs", verbose=False)

    rt_en = tagger.RhymeTagger()
    rt_en.load_model("en", verbose=False)

    total_distance = 0
    for i in range(len(czech_sections)):
        total_distance += get_section_rhyme_scheme_distance(czech_sections[i], english_sections[i], rt_cs, rt_en)

    total_distance /= len(czech_sections)

    return total_distance
    



with open("C:/Users/barca/MOJE/ROCNIKAC/rp-barbora-stepankova/DATA/Musicals/" + "frozen_03" + "_cs.txt", "r", encoding="utf-8") as f:
    text_cs = f.read()

with open("C:/Users/barca/MOJE/ROCNIKAC/rp-barbora-stepankova/DATA/Musicals/" + "frozen_03" + "_en.txt", "r", encoding="utf-8") as f:
    text_en = f.read()


czech_sections, english_sections = align_lyrics_by_section_and_line(text_cs, text_en)

english_sections = get_aligned_translation(czech_sections, "cz")

print(get_rhyme_scheme_mapping_distance(czech_sections, english_sections))