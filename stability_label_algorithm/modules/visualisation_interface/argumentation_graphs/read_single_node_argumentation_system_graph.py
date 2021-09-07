import igraph
from statistics import mean


def create_single_node_graph(argumentation_theory):

    graph = igraph.Graph(directed=True)

    for literal_str, literal in argumentation_theory.argumentation_system.language.items():
        graph.add_vertex(name=literal_str, type='literal_instance', literal=literal, pos=list(literal.position))

    for rule in argumentation_theory.argumentation_system.rules:
        positions_connected_literals = [literal.position for literal in [rule.consequent] + list(rule.antecedents)]
        rule_vertex_x = mean([pos[0] for pos in positions_connected_literals])
        rule_vertex_y = mean([pos[1] for pos in positions_connected_literals])

        graph.add_vertex(name=str(rule), type='rule_instance', rule=rule, pos=[rule_vertex_x, rule_vertex_y])
        graph.add_edge(str(rule.consequent), str(rule), visible=True, color='black')
        for child in rule.antecedents:
            graph.add_edge(str(rule), str(child), visible=True, color='black')

    for literal_str, literal in argumentation_theory.argumentation_system.language.items():
        for contrary_literal in literal.contraries:
            graph.add_edge(literal_str, str(contrary_literal), visible=True, color='red')

    return graph
