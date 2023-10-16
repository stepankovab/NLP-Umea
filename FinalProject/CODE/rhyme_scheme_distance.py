import Imports.tagger as tagger


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
    rt_cs.load_model("./Imports/cs", verbose=False)
    rhymes_cs = rt_cs.tag(poem=czech_lines, output_format=1)

    rt_en = tagger.RhymeTagger()
    rt_en.load_model("./Imports/en", verbose=False)
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