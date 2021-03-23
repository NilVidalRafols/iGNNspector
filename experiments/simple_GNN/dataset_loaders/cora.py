import mysql.connector as mariadb
import numpy as np


def load_cora():
    """
    Load the CORA dataset
    :return: Adjacency matrix, attributes of the nodes and target values. All of them in boolean matrix form.
    """
    classes = {
        'Genetic_Algorithms': [1, 0, 0, 0, 0, 0, 0],
        'Reinforcement_Learning': [0, 1, 0, 0, 0, 0, 0],
        'Theory': [0, 0, 1, 0, 0, 0, 0],
        'Rule_Learning': [0, 0, 0, 1, 0, 0, 0],
        'Case_Based': [0, 0, 0, 0, 1, 0, 0],
        'Probabilistic_Methods': [0, 0, 0, 0, 0, 1, 0],
        'Neural_Networks': [0, 0, 0, 0, 0, 0, 1]
    }
    # Load the data from a public database
    database = mariadb.connect(host='relational.fit.cvut.cz', port='3306',
                               user='guest', password='relational', database='CORA')
    cursor = database.cursor()

    # Load papers and their classes in one hot encoding
    cursor.execute('SELECT paper_id, class_label FROM paper order by paper_id ASC;')
    nodes = [(paper_id, classes[class_label]) for paper_id, class_label in cursor]
    node_indices = {
        nodes[i][0]: i
        for i in range(0, len(nodes))
    }
    target = np.zeros((len(nodes), 7))
    for i, node in enumerate(nodes):
        target[i] = node[1]

    # Load edges as an adjacency boolean matrix
    cursor.execute('SELECT citing_paper_id, cited_paper_id FROM cites;')
    edges = np.zeros((len(nodes), len(nodes)))
    for cited_paper_id, citing_paper_id in cursor:
        edges[node_indices[cited_paper_id], node_indices[citing_paper_id]] = 1.0

    # Load the words and their new indices
    cursor.execute('SELECT DISTINCT word_cited_id FROM content order by word_cited_id ASC;')
    word_indices = {word_cited_id: i for i, (word_cited_id,) in enumerate(cursor)}
    cursor.execute('SELECT paper_id, word_cited_id FROM content;')
    words = np.zeros((len(nodes), len(word_indices)))
    for paper_id, word_cited_id in cursor:
        words[node_indices[paper_id], word_indices[word_cited_id]] = 1.0

    database.close()

    return edges, words, target
