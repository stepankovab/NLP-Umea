import lzma
import pickle





with lzma.open("C:/Users/barca/MOJE/UMEA/NLP-Umea/FinalProject/DATA/results.dict", "rb") as model_file:
    scores = pickle.load(model_file)


parameters = len(scores["HT"][0])
songs = len(scores["HT"])
averages_HT = []
averages_cs_to_en = []
averages_en_to_cs = []

for i in range(parameters):
    for j in range(songs):
        averages_HT.append(max(scores["HT"][j][i], 0))
        averages_cs_to_en.append(max(scores["cz_to_en"][j][i],0))
        averages_en_to_cs.append(max(scores["en_to_cz"][j][i],0))
    print("HT", sum(averages_HT)/songs)
    print("cz_to_en", sum(averages_cs_to_en)/songs)
    print("en_to_cz", sum(averages_en_to_cs)/songs)
    print("\n")

    averages_HT.clear()
    averages_cs_to_en.clear()
    averages_en_to_cs.clear()








