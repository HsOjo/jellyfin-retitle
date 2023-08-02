import re


def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]


def get_episode_index(item_name: str, parent_name: str):
    while True:
        lcs_str = longest_common_substring(item_name, parent_name)

        if len(lcs_str) > 1 and not lcs_str.strip().isnumeric():
            item_name = item_name.replace(lcs_str, '')
        else:
            break

    indexes = re.findall(r'\d+', item_name)
    return indexes.pop(0)
