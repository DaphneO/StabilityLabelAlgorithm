import igraph


def create_multi_node_graph(argumentation_theory, topic_literal):
    node_counters = {literal_str: 0 for literal_str in argumentation_theory.argumentation_system.language.keys()}
    rule_counters = {str(rule): 0 for rule in argumentation_theory.argumentation_system.rules}

    graph = igraph.Graph()

    draw_rule_list = set()

    graph.add_vertex(name='ROOT', type='root')

    topic_literal_str = str(topic_literal)
    node_counters[topic_literal_str] += 1
    literal_node_name = topic_literal_str + '-' + str(node_counters[topic_literal_str])
    graph.add_vertex(name=literal_node_name, type='literal_instance', literal=topic_literal, topic=True)
    graph.add_edge(source='ROOT', target=literal_node_name, visible=False)
    draw_rule_list = draw_rule_list | set([(literal_node_name, rule) for rule in topic_literal.children])

    contrary_edges = []

    for contrary_literal in topic_literal.contraries:
        contrary_literal_str = str(contrary_literal)
        node_counters[contrary_literal_str] += 1
        contrary_literal_node_name = contrary_literal_str + '-' + str(node_counters[contrary_literal_str])
        graph.add_vertex(name=contrary_literal_node_name, type='literal_instance', literal=contrary_literal)
        graph.add_edge(source='ROOT', target=contrary_literal_node_name, visible=False)
        draw_rule_list = draw_rule_list | set([(contrary_literal_node_name, contrary_rule)
                                               for contrary_rule in contrary_literal.children])
        contrary_edges.append((contrary_literal_node_name, literal_node_name))

    while draw_rule_list:
        conclusion_literal, draw_rule = draw_rule_list.pop()
        rule_str = str(draw_rule)
        rule_counters[rule_str] += 1
        rule_node_name = rule_str + '-' + str(rule_counters[rule_str])
        graph.add_vertex(name=rule_node_name, type='rule_instance', rule=draw_rule)
        graph.add_edge(rule_node_name, conclusion_literal, visible=True, color='black')

        for child_literal in draw_rule.antecedents:
            child_literal_str = str(child_literal)
            node_counters[child_literal_str] += 1
            child_literal_node_name = child_literal_str + '-' + str(node_counters[child_literal_str])
            graph.add_vertex(name=child_literal_node_name, type='literal_instance', literal=child_literal)
            graph.add_edge(child_literal_node_name, rule_node_name, visible=True, color='black')

            draw_rule_list = draw_rule_list | set([(child_literal_node_name, child_rule)
                                                   for child_rule in child_literal.children])

            for contrary_literal in child_literal.contraries:
                contrary_literal_str = str(contrary_literal)
                node_counters[contrary_literal_str] += 1
                contrary_literal_node_name = contrary_literal_str + '-' + str(node_counters[contrary_literal_str])
                graph.add_vertex(name=contrary_literal_node_name, type='literal_instance', literal=contrary_literal)
                graph.add_edge(contrary_literal_node_name, rule_node_name, visible=False)

                draw_rule_list = draw_rule_list | set([(contrary_literal_node_name, contrary_child_rule)
                                                       for contrary_child_rule in contrary_literal.children])

                contrary_edges.append((contrary_literal_node_name, child_literal_node_name))

    pos = graph.layout_reingold_tilford(root=graph.vs.find(name='ROOT').index).coords
    for index, vertex in enumerate(graph.vs):
        vertex['pos'] = [pos[index][0], -pos[index][1]]

    for source, target in contrary_edges:
        graph.add_edge(source, target, visible=True, color='red')

    return graph
