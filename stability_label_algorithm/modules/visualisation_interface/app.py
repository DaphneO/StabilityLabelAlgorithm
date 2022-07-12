# -*- coding: utf-8 -*-
import dash
import pathlib
from os import listdir
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import dash_daq as daq

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system import \
    ArgumentationSystem
from stability_label_algorithm.modules.argumentation.importers.argumentation_system_xlsx_reader import \
    ArgumentationSystemXLSXReader
from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory import \
    ArgumentationTheory
from stability_label_algorithm.modules.visualisation_interface.html_divs.structured_column_div import \
    get_structured_column_div

visualisation_screen = dash.Dash(__name__)

server = visualisation_screen.server

visualisation_screen.config.suppress_callback_exceptions = True

visualisation_screen.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

argumentation_system_options_path = pathlib.Path(__file__).parent.parent.parent / 'resources' / 'rule_sets'
argumentation_system_options_str = [f for f in listdir(argumentation_system_options_path) if f.endswith('.xlsx')]
argumentation_system_options_str.sort()

visualisation_screen.title = 'Structured argumentation visualisation'

index_elements = [
    html.Div([
        html.Img(
            src='https://nationaal-politielab.sites.uu.nl/wp-content/uploads/sites/536/2019/11/'
                'banner-politielab-1600x400.jpg',
            style={'width': '100%', 'display': 'block'}),
        html.H1('Estimating Stability for Efficient Argument-based Inquiry | Visualisation',
                style={'font-family': '"Open Sans","Frutiger",Helvetica,Arial,sans-serif',
                       'font-weight': '100', 'font-size': '40px', 'line-height': '1',
                       'textAlign': 'center',
                       'padding-left': '15px', 'padding-top': '15px', 'padding-bottom': '15px',
                       'padding-right': '15px'}),
        html.Div([], style={'width': '100%', 'height': '40px', 'background-color': 'black'})
    ], style={'background-color': 'rgb(255, 205, 0)', 'width': '100%'}),
    html.Div([
        html.Div([
            html.H2('Welcome at this demo', style={
                'font-family': '"Merriweather","Bembo",Georgia,Times,"Times New Roman",serif',
                'font-size': '35px', 'line-height': '35px'}),
            html.P(
                'Here you can see visualisations of multiple labelling algorithms on multiple argumentation setups.\n'
                'Choose one of the links below to go the visualisation of that argumentation setup.',
                style={
                    'font-family': '"Merriweather","Bembo",Georgia,Times,"Times New Roman",serif',
                    'font-size': '22px', 'line-height': '28px'})
        ], style={'width': '100%',
                  # 'background-color': 'lightgrey'
                  })

    ], style={'margin': 'auto', 'width': '70%', 'padding': '10px'}),
    html.Br([])
]
argumentation_systems = {}
about_texts = {}
for file_str in argumentation_system_options_str:
    try:
        label = file_str[:-5]
        asr = ArgumentationSystemXLSXReader(
            pathlib.Path(__file__).parent.parent.parent / 'resources' / 'rule_sets' / file_str)
        argumentation_systems[label] = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        about_texts[label] = asr.about_text

        index_as = []
        show_name = label.replace('_', ' ')
        if show_name.startswith('0'):
            show_name = show_name[3:]

        index_as.append(html.H2(show_name, style={
            'font-family': '"Merriweather","Bembo",Georgia,Times,"Times New Roman",serif',
            'font-size': '25px', 'line-height': '30px'}))
        index_as.append(html.P([about_texts[label],
                                html.Br(),
                                html.Br(),
                                dcc.Link('Go to \"' + show_name + '\"', href='/' + label, style={'color': 'black'})],
                               style={
                                   'font-family': '"Merriweather","Bembo",Georgia,Times,"Times New Roman",serif',
                                   'font-size': '18px', 'line-height': '25px'})
                        )
        index_elements.append(html.Div(index_as, style={'margin': 'auto', 'width': '70%',
                                                        'background-color': 'rgb(239,239,239)',
                                                        'padding': '10px'}))
        index_elements.append(html.Br())
    except ImportError:
        print('This argumentation system could not be loaded: ' + file_str)

index_page = html.Div(index_elements, style={'width': '100%'})


def get_language_div(argumentation_system, about_text):
    knowledge_base_div = \
        html.Div([
            html.H3(style={'textAlign': 'center'}, children=[
                'Knowledge base',
                '   ',
                html.Abbr("❔",
                          title="This is the system's current knowledge base.")
            ]),
            dcc.Dropdown(
                id='knowledge_base',
                options=[
                    {'label': str(literal), 'value': str(literal)}
                    for literal in argumentation_system.language.values()
                    if literal.is_observable
                ],
                value=[],
                multi=True,
                style={'width': '100%'}
            )
        ])

    dropdown_options = [{'label': literal_str, 'value': literal_str}
                        for literal_str, literal in argumentation_system.language.items()
                        if not literal.negated]
    if 't' in argumentation_system.language:
        topic_literal = 't'
    elif 'fraud' in argumentation_system.language:
        topic_literal = 'fraud'
    else:
        topic_literal = dropdown_options[0]['value']

    topic_div = html.Div(
        [html.P('Select topic literal', style={'width': '25%', 'float': 'left'}),
         dcc.Dropdown(
             options=dropdown_options,
             value=topic_literal,
             id='topic-literal-str',
             style={'width': '75%', 'float': 'left'})],
        style={'width': '100%'})

    about_div = html.Div(
        [
            html.H3('About this argumentation system'),
            html.P(about_text),
            html.B(),
            dcc.Link('Go back to the main page', href='/')
        ], style={'width': '100%'})

    return html.Div(children=[knowledge_base_div, html.Br(),
                              topic_div,
                              html.Br(), html.Br(), html.Br(),
                              about_div
                              ],
                    style={'textAlign': 'left',
                           'width': '25%',
                           'float': 'left'},
                    id='full-language-div')


def get_page_layout(argumentation_system, about_text):
    labeler_dd = \
        html.Div([
            html.P(['Select label method', '   ',
                    html.Abbr("❔", title="Choose here which method you want to use for labelling the "
                                         "literals and rules. FourBoolStability is the algorithm proposed "
                                         "in our paper submitted to COMMA 2020. SingleLabelStability is the "
                                         "algorithm proposed by Testerink et al. in the 2019 FQAS paper. "
                                         "CurrentAcceptability shows the acceptability of literals and "
                                         "rules in the current argumentation setup (and does not take into "
                                         "account future observations).")
                    ], style={'float': 'left', 'width': '30%'}),
            dcc.Dropdown(id='labeler_dropdown',
                         options=[
                             {'label': 'FourBoolStability', 'value': 'four_bool'},
                             {'label': 'SingleLabelStability [Testerink et al, 2019]', 'value': 'fqas'},
                             {'label': 'CurrentAcceptability', 'value': 'acceptability'}
                         ],
                         value='four_bool',
                         style={'float': 'left', 'width': '70%'}
                         )
        ],
            style={
                # 'overflow': 'hidden',
                'width': '100%', 'float': 'left'}
        )

    legenda_div = html.Div([
        daq.Indicator(value=True, color='black', label='Unsatisfiable', style={'float': 'left', 'width': '16%'}),
        daq.Indicator(value=True, color='green', label='Defended', style={'float': 'left', 'width': '16%'}),
        daq.Indicator(value=True, color='red', label='Out', style={'float': 'left', 'width': '16%'}),
        daq.Indicator(value=True, color='yellow', label='Blocked', style={'float': 'left', 'width': '16%'}),
        daq.Indicator(value=True, color='darkblue', label='Observed', style={'float': 'left', 'width': '16%'})
    ],
        style={'overflow': 'hidden', 'float': 'left', 'width': '100%'}
    )

    left_col_div = html.Div(children=[html.H3(['Argumentation theory visualisation',
                                               '   ',
                                               html.Abbr("❔",
                                                         title="The figure below visualises the current state of the "
                                                               "argumentation setup. Literals are visualised by circles"
                                                               ", rules are visualised by diamonds. Literals and rules "
                                                               "can be shown multiple times to improve readability.\n"
                                                               "The colors of a circle or diamond (black/green/red/"
                                                               "yellow/grey) correspond to the label. For example, if "
                                                               "a circle is green, black and grey, then the "
                                                               "corresponding literal is labelled <1, 1, 0, 0>.\n"
                                                               "Observed literals get a dark blue edge."
                                                         )
                                               ]),
                                      labeler_dd,
                                      legenda_div,
                                      dcc.Graph(id='structured-graph', style={'float': 'left', 'width': '100%'})
                                      ],
                            id='structured-div',
                            style={'textAlign': 'center', 'width': '70%',
                                   'float': 'left'
                                   })
    right_col_div = get_language_div(argumentation_system, about_text)

    main_div = \
        html.Div(id='main-div',
                 children=[left_col_div, right_col_div],
                 style={
                     'width': '100%',
                     'overflow': 'hidden'
                 },
                 )
    return main_div


@visualisation_screen.callback(Output('page-content', 'children'),
                               [Input('url', 'pathname')])
def display_page(path_name):
    if path_name == '/':
        return index_page
    if path_name and len(path_name) > 1 and path_name[1:] in argumentation_systems.keys():
        return get_page_layout(argumentation_systems[path_name[1:]], about_texts[path_name[1:]])
    return html.H3('404')


@visualisation_screen.callback(Output('knowledge_base', 'options'),
                               [Input('url', 'pathname'), Input('knowledge_base', 'value')])
def update_observation_options(path_name, current_value):
    if path_name == '/':
        return []
    argumentation_system = argumentation_systems[path_name[1:]]
    current_literals = [argumentation_system.language[literal_str] for literal_str in current_value]
    new_options = [
        {'label': str(literal), 'value': str(literal)}
        for literal in argumentation_system.language.values()
        if literal.is_observable and all(
            [literal not in observed_literal.contraries for observed_literal in current_literals])
    ]
    return new_options


@visualisation_screen.callback(Output(component_id='knowledge_base', component_property='value'),
                               [Input(component_id='url', component_property='pathname'),
                                Input(component_id='answer-options', component_property='value')],
                               [State(component_id='knowledge_base', component_property='value')])
def update_knowledge_base_from_question(path_name, answer_value, old_knowledge_base):
    if path_name == '/':
        return []

    if answer_value:
        old_knowledge_base.append(answer_value)

    return old_knowledge_base


@visualisation_screen.callback(Output(component_id='structured-graph', component_property='figure'),
                               [
                                   Input(component_id='url', component_property='pathname'),
                                   Input(component_id='knowledge_base', component_property='value'),
                                   Input(component_id='topic-literal-str', component_property='value'),
                                   Input(component_id='structured-graph', component_property='clickData'),
                                   Input(component_id='labeler_dropdown', component_property='value')]
                               )
def update_figure(path_name, knowledge_base_str, topic_literal_str, click_data, labeler_value):
    if path_name == '/':
        return None, '', '', []

    argumentation_system = argumentation_systems[path_name[1:]]

    knowledge_base = argumentation_system.get_queryables(knowledge_base_str)
    argumentation_theory = ArgumentationTheory(argumentation_system, knowledge_base)

    topic_literal = argumentation_system.language[topic_literal_str]

    figure = get_structured_column_div(argumentation_theory, topic_literal, labeler_value)

    return figure


if __name__ == '__main__':
    visualisation_screen.run_server()
