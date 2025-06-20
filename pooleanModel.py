import re

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.split()

 # {term :{1,2,3}} , term apper in the doc
def inverted_index(documents):
    index = {}
    for doc_id, text in documents.items():
        for word in preprocess(text):
            index.setdefault(word, set()).add(doc_id)
    return index

#Convert to Postfix (set process precedence)
def to_postfix(tokens): # ['a','b','c','not','or','and']
    precedence = {'not': 3, 'and': 2, 'or': 1}
    output = []
    stack = []
    for token in tokens:
        if token in precedence:
            while stack and precedence.get(stack[-1], 0) >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        else:
            output.append(token)
    while stack:
        output.append(stack.pop())
    return output


def search(query, index):
    tokens = preprocess(query)
    postfix = to_postfix(tokens)
    stack = []

    # doc ID type set
    all_doc_ids = set() # {d1,d2,d3,d4,d5}
    for doc_ids in index.values():
        all_doc_ids.update(doc_ids)

    for token in postfix: # ['hassan', 'omar', 'alomari', 'not', 'and', 'or']
        if token == 'not':
            operand = stack.pop()
            stack.append(all_doc_ids - operand) # {1,2,3} - {2,3} = {1},Apply not (reflex) 
        elif token == 'and':
            right = stack.pop()
            left = stack.pop()
            stack.append(left & right)# {1,2,3} & {2,3} = {2,3}
        elif token == 'or':
            right = stack.pop()
            left = stack.pop()
            stack.append(left | right) # {1,2,3} & {2,3} = {1,2,3}
        else:
            # term , not op
            stack.append(index.get(token, set()))

    return stack[0] if stack else set()# resulte 

def boolean_model(query, dic):
    index = inverted_index(dic)
    doc_ids = search(query, index)
    results = [f"{doc_id}: {dic[doc_id]}" for doc_id in sorted(doc_ids)]
    return results

