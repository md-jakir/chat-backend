# from ragas.langchain.evalchain import RagasEvaluatorChain
from ragas.integrations.langchain import EvaluatorChain as RagasEvaluatorChain
import json
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
)

# create evaluation chains
faithfulness_chain = RagasEvaluatorChain(metric=faithfulness)
answer_rel_chain = RagasEvaluatorChain(metric=answer_relevancy)
# context_rel_chain = RagasEvaluatorChain(metric=context_precision)
# context_recall_chain = RagasEvaluatorChain(metric=context_recall)


def evaluate(blocks):
    for block in blocks:
        print(block)
        faithfulness_score = faithfulness_chain(blocks[block])["faithfulness"]
        ans_rel_score = answer_rel_chain(blocks[block])["answer_relevancy"]
        blocks[block]['faithfulness_score'] = faithfulness_score
        blocks[block]['ans_rel_score'] = ans_rel_score
    return blocks

def generate_report(file):
    blocks = json.load(open(file, "r"))
    blocks = evaluate(blocks)
    json.dump(blocks, open(file+"_result", "w"), indent=2)

gg = {'question': 'What makes Wagyu beef famous and what special care and diets are given to Wagyu cattle?',
 'contexts': ['•Holstein : Known for their high milk yield, Holsteins are the most common dairy\nbreed worldwide. They have distinctive black and white markings and are highly\nproductive, with some individuals producing over 30,000 pounds of milk annually.\n•Jersey : Jerseys produce milk with high butterfat content, making it ideal for\ncheese and butter. They are smaller in size compared to Holsteins and have a\ngentle disposition.\n•Guernsey : This breed is valued for its rich, golden-colored milk, which contains\nhigh levels of beta-carotene. Guernseys are known for their efficiency in converting\nfeed into milk.\n4.2 Beef Breeds\nBeef breeds are developed for their ability to produce high-quality meat. They have\ncharacteristics that make them efficient in gaining weight and producing tender, flavorful\nmeat.\n•Angus : Angus cattle are known for their marbled meat, which is tender and flavor-\nful. They are hardy and adapt well to various environments, making them popular\nin beef production.\n•Hereford : Herefords are hardy and well-suited to various climates, making them\npopular in beef production. They have a distinctive red and white coat and are\nknown for their docile temperament.\n•Wagyu : Originating from Japan, Wagyu beef is famous for its intense marbling\nand rich taste. Wagyu cattle are raised with special care and diets to enhance the\nquality of their meat.\n4.3 Dual-Purpose Breeds\nSome breeds are versatile and can be used for both milk and meat production. These\ndual-purpose breeds offer flexibility to farmers and are often found in regions where both\ndairy and beef products are in demand.\n5 Cows in Agriculture\nCows are indispensable in agriculture, providing a range of products and services. They\nare integral to both small-scale and industrial farming operations. Their contributions to\nthe agricultural sector are vast and multifaceted.\n5.1 Milk Production\nMilk from cows is a staple in many diets around the world. Dairy farming involves\nthe careful management of cow health, nutrition, and milking processes to ensure high-\nquality milk. Advances in dairy technology, such as automated milking systems and\ngenetic selection, have significantly improved milk production efficiency.\n3'],
 'ground_truth': 'Wagyu beef is famous for its intense marbling and rich taste. Wagyu cattle are raised with special care and diets to enhance the quality of their meat.',
 'evolution_type': 'simple',
 'metadata': [{'source': 'cow.pdf', 'page': 2, 'filename': 'cow.pdf'}],
 'episode_done': True,
 'answer': 'Wagyu beef is famous for its intense marbling and rich taste. Wagyu cattle are raised with special care and diets to enhance the quality of their meat.',
 'faithfulness': 0.75
 }
big_chain = RagasEvaluatorChain(metric=answer_relevancy)
scores = big_chain(gg)
print(scores)
