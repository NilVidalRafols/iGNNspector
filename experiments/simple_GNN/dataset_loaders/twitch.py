import csv
import numpy as np
from scipy.linalg import block_diag


def __load_twitch(edges_path, nodes_path):
    with open(nodes_path) as nodes_file:
        nodes_csv = csv.reader(nodes_file, delimiter=',', )
        next(nodes_csv)  # Skip header

        nodes = np.zeros((0, 3))
        target = np.zeros(0)
        rows_dict = {}
        for i, row in enumerate(nodes_csv):
            nodes = np.concatenate((nodes, np.array([[
                int(row[1]),  # days
                1.0 if row[4] == "True" else 0.0,  # partner
                int(row[3])  # views
            ]])))
            target = np.append(target, 1.0 if row[2] == "True" else 0.0) # mature
            rows_dict[row[5]] = i

    with open(edges_path) as edges_file:
        edges_csv = csv.reader(edges_file, delimiter=',')
        next(edges_csv)
        edges = np.eye(target.shape[0])
        for (from_idx, to_idx) in edges_csv:
            edges[rows_dict[from_idx], rows_dict[to_idx]] = 1.0
            edges[rows_dict[to_idx], rows_dict[from_idx]] = 1.0

    return edges, nodes, target


def load_twitch():
    edges_de, nodes_de, target_de = __load_twitch('datasets/twitch/DE/musae_DE_edges.csv', 'datasets/twitch/DE/musae_DE_target.csv')
    edges_engb, nodes_engb, target_engb = __load_twitch('datasets/twitch/ENGB/musae_ENGB_edges.csv', 'datasets/twitch/ENGB/musae_ENGB_target.csv')
    edges_es, nodes_es, target_es = __load_twitch('datasets/twitch/ES/musae_ES_edges.csv', 'datasets/twitch/ES/musae_ES_target.csv')
    edges_fr, nodes_fr, target_fr = __load_twitch('datasets/twitch/FR/musae_FR_edges.csv', 'datasets/twitch/FR/musae_FR_target.csv')
    edges_ptbr, nodes_ptbr, target_ptbr = __load_twitch('datasets/twitch/PTBR/musae_PTBR_edges.csv', 'datasets/twitch/PTBR/musae_PTBR_target.csv')
    edges_ru, nodes_ru, target_ru = __load_twitch('datasets/twitch/RU/musae_RU_edges.csv', 'datasets/twitch/RU/musae_RU_target.csv')

    edges = block_diag(edges_de, edges_engb, edges_es, edges_fr, edges_ptbr, edges_ru)
    nodes = np.concatenate((nodes_de, nodes_engb, nodes_es, nodes_fr, nodes_ptbr, nodes_ru))
    target = np.concatenate((target_de, target_engb, target_es, target_fr, target_ptbr, target_ru))
    return edges, nodes, target
