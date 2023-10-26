from syllabator import syllabify

title = "encanto_01"

czech_sections = []
english_sections = []

with open("C:/Users/barca/MOJE/UMEA/NLP-Umea/FinalProject/DATA/Aligned_HT/" + title + "_cs.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    temp = []
    for line in lines:
        line = line[:-1]
        if line == "":
            czech_sections.append(temp.copy())
            temp.clear()
        else:
            temp.append(line)

with open("C:/Users/barca/MOJE/UMEA/NLP-Umea/FinalProject/DATA/ChatGPT_translations/" + title + "_ch_en.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    temp = []
    for line in lines:
        line = line[:-1]
        if line == "":
            english_sections.append(temp.copy())
            temp.clear()
        else:
            temp.append(line)




for section_i in range(len(czech_sections)):
    while section_i >= len(english_sections):
        print(english_sections)
    for line_i in range(min(len(czech_sections[section_i]), len(english_sections[section_i]))):
        diff = len(syllabify(czech_sections[section_i][line_i], "cz")) - len(syllabify(english_sections[section_i][line_i], "en"))
        print(czech_sections[section_i][line_i], " --- ", english_sections[section_i][line_i], "--->", diff)
    print()
