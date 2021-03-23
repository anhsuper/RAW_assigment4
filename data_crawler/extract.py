import heapq
import re
from collections import defaultdict
from os import listdir
from os.path import isfile
from os.path import join

mypath_vi = "./vne_spider/data"
mypath_en = "./vne_spider/data_english"
remove_characters = [".", ",", "-", "(", ")", "*", "&", "_"]
words_pattern_vi = (
    "[a-záàảãạăắằẳẫặâấầẩẫậêếềểễệíìỉĩịúùủũụưứừửữựóòỏõọơớờởỡợôốồổỗộýỳỷỹỵđ]+"
)
words_pattern_en = "[a-z]+"


def get_words(mypath, words_pattern):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    all_text = defaultdict(int)
    all_text_per_file = defaultdict(int)

    total_word = 0
    for filename in onlyfiles:
        with open(f"{mypath}/{filename}", "r") as openfile:
            text_temp = set()
            content = openfile.read()
            for remove_character in remove_characters:
                content = content.replace(remove_character, " ")
            words = re.findall(words_pattern, content, flags=re.IGNORECASE)
            for word in words:
                total_word += 1
                word = word.lower()
                if word not in text_temp:
                    text_temp.add(word)
                    all_text_per_file[word] += 1

                all_text[word] += 1

    return all_text, all_text_per_file, total_word


all_text_vi, all_text_per_file_vi, total_word_vi = get_words(
    mypath_vi, words_pattern_vi
)
all_text_en, all_text_per_file_en, total_word_en = get_words(
    mypath_en, words_pattern_en
)


def get_results(all_text_1, all_text_2, all_text_per_file_1, all_text_per_file_2):
    results = []
    for word in all_text_1:
        if word in all_text_2:
            if (
                all_text_1[word] > all_text_2[word]
                and all_text_per_file_1[word] > all_text_per_file_2[word]
            ) or all_text_1[word] > 20:
                results.append(word)
        elif all_text_1[word] > 5 and all_text_per_file_1[word] > 2:
            results.append(word)
    return results


results_vi = get_results(
    all_text_vi, all_text_en, all_text_per_file_vi, all_text_per_file_en
)
results_en = get_results(
    all_text_en, all_text_vi, all_text_per_file_en, all_text_per_file_vi
)


def get_top(all_text):
    top_word = heapq.nlargest(2, all_text.keys(), key=lambda k: all_text[k])[0]
    return top_word, all_text[top_word]


vi = "./vne_spider/vi.txt"
en = "./vne_spider/en.txt"

with open(f"{vi}", "w") as openfile:
    for i in results_vi:
        openfile.write(i + "\r\n")

with open(f"{en}", "w") as openfile:
    for i in results_en:
        openfile.write(i + "\r\n")
