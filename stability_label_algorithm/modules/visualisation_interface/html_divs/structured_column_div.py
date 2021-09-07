import plotly.graph_objs as go

from ..argumentation_graphs.multi_node_argumentation_system_graph import create_multi_node_graph
from ..argumentation_graphs.read_single_node_argumentation_system_graph import create_single_node_graph
from ...argumentation.labelers.four_bool_labeler import FourBoolLabeler
from ...argumentation.labelers.acceptability_labeler import JustificationLabeler
from ...argumentation.labelers.fqas_labeler import FQASLabeler
from ...argumentation.labelers.labels import StabilityLabel


def get_structured_column_div(argumentation_theory, topic_literal, labeler_str):
    if topic_literal.position is None:
        argumentation_theory_graph = create_multi_node_graph(argumentation_theory, topic_literal)
    else:
        argumentation_theory_graph = create_single_node_graph(argumentation_theory)

    trace_recode = []

    for edge in list(argumentation_theory_graph.es):
        if edge['visible']:
            x0, y0 = argumentation_theory_graph.vs[edge.source]['pos']
            x1, y1 = argumentation_theory_graph.vs[edge.target]['pos']
            edge_trace = go.Scatter(x=tuple([x0, x1, None]), y=tuple([y0, y1, None]),
                                    mode='lines',
                                    line_shape='spline',
                                    line_color=edge['color'],
                                    opacity=1)
            trace_recode.append(edge_trace)

    relevant_literal_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text',
                                        textposition='top center',
                                        hoverinfo='text',
                                        marker={'size': 50, 'color': 'SkyBlue'})
    observed_literal_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text',
                                     textposition='top center',
                                     hoverinfo='text',
                                     marker={'size': 50, 'color': 'darkblue'})
    other_literal_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text', textposition='top center',
                               hoverinfo='text',
                               marker={'size': 50, 'color': 'lightgrey'})

    # Label using the selected Labels
    if labeler_str == 'four_bool':
        labeler = FourBoolLabeler()
    elif labeler_str == 'fqas':
        labeler = FQASLabeler()
    else:
        labeler = JustificationLabeler()
    labels = labeler.label(argumentation_theory)

    unsatisfiable_literal_true_trace = go.Scatter(x=[], y=[],
                                                  hovertext=[], text=[],
                                                  hoverinfo='text',
                                                  mode='markers',
                                                  marker={'size': 40, 'color': 'black'})
    defended_literal_true_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                             hoverinfo='text',
                                             marker={'size': 30, 'color': 'green'})
    out_literal_true_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                        hoverinfo='text',
                                        marker={'size': 20, 'color': 'red'})
    blocked_literal_true_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                            hoverinfo='text',
                                            marker={'size': 10, 'color': 'yellow'})
    unsatisfiable_literal_false_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                                   hoverinfo='text',
                                                   marker={'size': 40, 'color': 'lightgrey'})
    defended_literal_false_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                              hoverinfo='text',
                                              marker={'size': 30, 'color': 'lightgrey'})
    out_literal_false_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                         hoverinfo='text',
                                         marker={'size': 20, 'color': 'lightgrey'})
    blocked_literal_false_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                             hoverinfo='text',
                                             marker={'size': 10, 'color': 'lightgrey'})

    unsatisfiable_rule_true_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                               hoverinfo='text',
                                               marker={'size': 40, 'color': 'black', 'symbol': 'diamond'})
    defended_rule_true_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                          hoverinfo='text',
                                          marker={'size': 30, 'color': 'green', 'symbol': 'diamond'})
    out_rule_true_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                     hoverinfo='text',
                                     marker={'size': 20, 'color': 'red', 'symbol': 'diamond'})
    blocked_rule_true_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                         hoverinfo='text',
                                         marker={'size': 10, 'color': 'yellow', 'symbol': 'diamond'})
    unsatisfiable_rule_false_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                                hoverinfo='text',
                                                marker={'size': 40, 'color': 'lightgrey', 'symbol': 'diamond'})
    defended_rule_false_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                           hoverinfo='text',
                                           marker={'size': 30, 'color': 'lightgrey', 'symbol': 'diamond'})
    out_rule_false_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                      hoverinfo='text',
                                      marker={'size': 20, 'color': 'lightgrey', 'symbol': 'diamond'})
    blocked_rule_false_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers',
                                          hoverinfo='text',
                                          marker={'size': 10, 'color': 'lightgrey', 'symbol': 'diamond'})

    for vertex in list(argumentation_theory_graph.vs):
        if vertex['name'] != 'ROOT':
            x, y = vertex['pos']
            if vertex['type'] == 'rule_instance':
                if len(labels.rule_labeling) > 0:
                    rule_label = labels.rule_labeling[vertex['rule']]
                else:
                    rule_label = StabilityLabel(False, False, False, False)

                if rule_label.unsatisfiable:
                    unsatisfiable_rule_true_trace['x'] += (x,)
                    unsatisfiable_rule_true_trace['y'] += (y,)
                    unsatisfiable_rule_true_trace['hovertext'] += (str(vertex['rule']),)
                else:
                    unsatisfiable_rule_false_trace['x'] += (x,)
                    unsatisfiable_rule_false_trace['y'] += (y,)
                    unsatisfiable_rule_false_trace['hovertext'] += (str(vertex['rule']),)
                if rule_label.defended:
                    defended_rule_true_trace['x'] += (x,)
                    defended_rule_true_trace['y'] += (y,)
                    defended_rule_true_trace['hovertext'] += (str(vertex['rule']),)
                else:
                    defended_rule_false_trace['x'] += (x,)
                    defended_rule_false_trace['y'] += (y,)
                    defended_rule_false_trace['hovertext'] += (str(vertex['rule']),)
                if rule_label.out:
                    out_rule_true_trace['x'] += (x,)
                    out_rule_true_trace['y'] += (y,)
                    out_rule_true_trace['hovertext'] += (str(vertex['rule']),)
                else:
                    out_rule_false_trace['x'] += (x,)
                    out_rule_false_trace['y'] += (y,)
                    out_rule_false_trace['hovertext'] += (str(vertex['rule']),)
                if rule_label.blocked:
                    blocked_rule_true_trace['x'] += (x,)
                    blocked_rule_true_trace['y'] += (y,)
                    blocked_rule_true_trace['hovertext'] += (str(vertex['rule']),)
                else:
                    blocked_rule_false_trace['x'] += (x,)
                    blocked_rule_false_trace['y'] += (y,)
                    blocked_rule_false_trace['hovertext'] += (str(vertex['rule']),)
            else:
                if vertex['literal'] in argumentation_theory.knowledge_base:
                    trace = observed_literal_trace
                else:
                    trace = other_literal_trace
                trace['text'] += (vertex['literal'],)
                trace['x'] += tuple([x])
                trace['y'] += tuple([y])

                literal_label = labels.literal_labeling[vertex['literal']]

                if literal_label.unsatisfiable:
                    unsatisfiable_literal_true_trace['x'] += (x,)
                    unsatisfiable_literal_true_trace['y'] += (y,)
                    unsatisfiable_literal_true_trace['hovertext'] += (vertex['literal'],)
                else:
                    unsatisfiable_literal_false_trace['x'] += (x,)
                    unsatisfiable_literal_false_trace['y'] += (y,)
                    unsatisfiable_literal_false_trace['hovertext'] += (vertex['literal'],)
                if literal_label.defended:
                    defended_literal_true_trace['x'] += (x,)
                    defended_literal_true_trace['y'] += (y,)
                    defended_literal_true_trace['hovertext'] += (vertex['literal'],)
                else:
                    defended_literal_false_trace['x'] += (x,)
                    defended_literal_false_trace['y'] += (y,)
                    defended_literal_false_trace['hovertext'] += (vertex['literal'],)
                if literal_label.out:
                    out_literal_true_trace['x'] += (x,)
                    out_literal_true_trace['y'] += (y,)
                    out_literal_true_trace['hovertext'] += (vertex['literal'],)
                else:
                    out_literal_false_trace['x'] += (x,)
                    out_literal_false_trace['y'] += (y,)
                    out_literal_false_trace['hovertext'] += (vertex['literal'],)
                if literal_label.blocked:
                    blocked_literal_true_trace['x'] += (x,)
                    blocked_literal_true_trace['y'] += (y,)
                    blocked_literal_true_trace['hovertext'] += (vertex['literal'],)
                else:
                    blocked_literal_false_trace['x'] += (x,)
                    blocked_literal_false_trace['y'] += (y,)
                    blocked_literal_false_trace['hovertext'] += (vertex['literal'],)

    trace_recode.append(unsatisfiable_rule_true_trace)
    trace_recode.append(unsatisfiable_rule_false_trace)
    trace_recode.append(defended_rule_true_trace)
    trace_recode.append(defended_rule_false_trace)
    trace_recode.append(out_rule_true_trace)
    trace_recode.append(out_rule_false_trace)
    trace_recode.append(blocked_rule_true_trace)
    trace_recode.append(blocked_rule_false_trace)

    trace_recode.append(observed_literal_trace)
    trace_recode.append(relevant_literal_trace)
    trace_recode.append(other_literal_trace)
    trace_recode.append(unsatisfiable_literal_true_trace)
    trace_recode.append(unsatisfiable_literal_false_trace)
    trace_recode.append(defended_literal_true_trace)
    trace_recode.append(defended_literal_false_trace)
    trace_recode.append(out_literal_true_trace)
    trace_recode.append(out_literal_false_trace)
    trace_recode.append(blocked_literal_true_trace)
    trace_recode.append(blocked_literal_false_trace)

    edge_annotation_list = []
    for edge in list(argumentation_theory_graph.es):
        if edge['visible'] and edge['color'] != 'red':
            x0, y0 = argumentation_theory_graph.vs[edge.source]['pos']
            x1, y1 = argumentation_theory_graph.vs[edge.target]['pos']

            start_f = 0.45
            end_f = 1 - start_f

            x_start = x0 + start_f * (x1 - x0)
            x_end = x0 + end_f * (x1 - x0)
            y_start = y0 + start_f * (y1 - y0)
            y_end = y0 + end_f * (y1 - y0)

            edge_annotation_list.append({
                'ax': x_end,
                'ay': y_end,
                'x': x_start,
                'y': y_start,
                'axref': 'x',
                'ayref': 'y',
                'xref': 'x',
                'yref': 'y',
                'showarrow': True,
                'arrowsize': 2,
                'arrowwidth': 1
            })

    figure = {
        "data": trace_recode,
        "layout": go.Layout(
            showlegend=False,
            hovermode='closest',
            margin={'b': 10, 'l': 10, 'r': 10, 't': 10},
            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
            height=600,
            annotations=edge_annotation_list
        )
    }

    return figure
