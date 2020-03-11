def naiv_string_matching(text_source, pattern):
    result = []
    with open(text_source, 'r', errors='ignore') as file:
        text = file.read()
        for s in range(0, len(text) - len(pattern)):
            if (pattern == text[s : s + len(pattern)]):
                result.append(s)
    return result

##############################################3    

def prefix_function(pattern):
    pi = [0]
    k = 0
    for q in range(1, len(pattern)):
        while (k > 0 and pattern[k] != pattern[q]):
            k = pi[k - 1]
        if(pattern[k] == pattern[q]):
            k = k + 1
        pi.append(k)
    return pi

def transition_table(pattern):
    result = [{}]
    alphabet = set(pattern)
    pi = prefix_function(pattern)
    result[0][pattern[0]] = 1
    for q in range(1, len(pattern) + 1):
        result.append({})
        for a in alphabet:
            if q == len(pattern) or pattern[q] != a:
                if a in result[pi[q - 1]]:
                    result[q][a] = result[pi[q - 1]][a]
            else:
                k = min(len(pattern), q + 1)
                while True:
                    if pattern[:k] == (pattern[:q] + a)[q - k + 1 : q + 1]:
                        break
                    k -= 1
                result[q][a] = k
    return result

def transition_table_old(pattern):
    result = []
    alphabet = set(pattern)
    for q in range(0, len(pattern) + 1):
        result.append({})
        for a in alphabet:
            k = min(len(pattern) + 1, q + 2)
            while True:
                k = k - 1
                if pattern[:k] == (pattern[:q] + a)[q - k + 1 : q + 1]:
                    break
            result[q][a] = k
    return result 

def fa_string_matching(text_source, pattern):
    delta = transition_table(pattern)
    result = []
    q = 0
    with open(text_source, 'r', errors='ignore') as file:
        text = file.read()
        for s in range(0, len(text)):
            # q = delta[q].get(line[s], 0) # Wolno!!!
            q = delta[q][text[s]] if text[s] in delta[q] else 0
            if (q == len(delta) - 1):
                result.append(s + 1 - q)
    return result

############################################################

def kmp_string_matching(text_source, pattern):
    pi = prefix_function(pattern)
    result = []
    q = 0
    with open(text_source, 'r', errors='ignore') as file:
        text = file.read()
        for i in range(0, len(text)):
            while (q > 0 and pattern[q] != text[i]):
                q = pi[q - 1]
            if (pattern[q] == text[i]):
                q = q + 1
            if (q == len(pattern)):
                result.append(i + 1 - q)
                q = pi[q - 1]
    return result