import dash
from dash import html, html, Input, Output,callback, dcc, Dash, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('Données_clean.csv', encoding='ISO-8859-1')

app = Dash(__name__)

app = dash.Dash()
app.css.append_css({'external_url': '/assets/styles.css'})

app.layout = html.Div(style={}, children=[

    # Corps de la page
    html.Div(className='container', children=[
        html.Div(className='banner', children=[
            html.Div(className='logo', children=[
                html.Img(src="https://i.ibb.co/S3nMD0F/aloubooks-removebg-preview.png",style={'width': '100%', 'height': 'auto'})
            ]),
            html.Div(className='titre', children="Analyse de ventes")

        ]),
        html.Div(className='bloc1', children=[
             html.Div(className='b1_gauche', children=[
                html.H3( style={'opacity':'100%'}, children=" Filtres "),

            #Filtres
                dcc.Dropdown(
                    id='age-filter',
                    options=[{'label': TrancheAge, 'value': TrancheAge} for TrancheAge in df['TrancheAge'].unique()],
                    value=df['TrancheAge'].unique().tolist(),
                    multi=True
                    ),
                dcc.Dropdown(
                    id='sexe-filter',
                    options=[{'label': sex, 'value': sex} for sex in df['sex'].unique()],
                    value=df['sex'].unique().tolist(),
                    multi=True
                    ),
                dcc.RangeSlider(
                    id='montant-filter',
                    min=df['Montant'].min(),
                    max=df['Montant'].max(),
                    value=[df['Montant'].min(), df['Montant'].max()],
                    marks={i: str(i) for i in range(int(df['Montant'].min()), int(df['Montant'].max()), 10000)},
                    step=200
                    ),


            ]),
            html.Div(className='b1_droite', children=[
                html.Div(className='b1d_contexte', children=[
                #contexte
                 html.Div(className='dropdown-paragraph', children=[
            html.H3(id='toggle-paragraph', style={'cursor': 'pointer','opacity':'100%','margin-left':'20px'}, children=" Contexte  ▼"),
            html.Div(id='paragraph-content', style={'display': 'none'}, children=[
                "Le présent tableau de bord étudie les données clients d\'une librairie en 2022. Chaque ligne représente un client, avec des informations allant de l'âge, le sexe, le montant total payé, la fréquence d'achat, la dernière visite, et le paiement par catégorie de livre. Les catégories de livres sont au nombre de 3, allant des livres les plus accessibles aux plus chers. Le pie chart nous donne une représentation des taux d\'achat par catégorie. L`histogramme visualise la fréquence d\'achat en fonction de nos filtres. Enfin, le scatter plot identifie les clients à relancer.  "
            ])
        ])
                ]),
                html.Div(className='b1d_dataframe', children=[
                    dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    page_size=10
                    ),
                ]),
            ]),
        ]),
        html.Div(className='bloc2', children=[
            html.Div(className='b2g', children=[
                dcc.Graph(id='pie-chart'),
                ]),
                html.Div(className='b2d', children=[
                dcc.Graph(id='histogram'),
                ]),
            ]),
        html.Div(className='bloc3', children=[
            dcc.Graph(id='scatter-plot'),
            ]),


    ])
])
# contexte sous titre
@app.callback(
    Output('paragraph-content', 'style'),
    [Input('toggle-paragraph', 'n_clicks')],

)
def toggle_paragraph(n_clicks):
    if n_clicks is None:
        return {'display': 'none'}  # Par défaut, le contenu est masqué
    elif n_clicks % 2 == 1:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# Callback pour le Pie Chart
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('age-filter', 'value'),
     Input('sexe-filter', 'value'),
     Input('montant-filter', 'value')]
)
def update_pie_chart(selected_tranche_age, selected_sexe, selected_montant):
    filtered_df = df[df['TrancheAge'].isin(selected_tranche_age) &
                     df['sex'].isin(selected_sexe) &
                     (df['Montant'] >= selected_montant[0]) &
                     (df['Montant'] <= selected_montant[1])]

    pie_data = filtered_df[['Prix_Categ0', 'Prix_Categ1', 'Prix_Categ2']].sum().reset_index()
    pie_data.columns = ['Category', 'Value']

    fig = px.pie(pie_data, values='Value', names='Category', title='Répartition par Catégorie de Prix')
    return fig

# Callback pour l'Histogramme
@app.callback(
    Output('histogram', 'figure'),
    [Input('age-filter', 'value'),
     Input('sexe-filter', 'value'),
     Input('montant-filter', 'value')]
)
def update_histogram(selected_tranche_age, selected_sexe, selected_montant):
    filtered_df = df[df['TrancheAge'].isin(selected_tranche_age) &
                     df['sex'].isin(selected_sexe) &
                     (df['Montant'] >= selected_montant[0]) &
                     (df['Montant'] <= selected_montant[1])]

    fig = px.histogram(filtered_df, x='Fréquence',
                       nbins=30,
                       title='Histogramme de Fréquence')

    fig.update_layout(bargap=0.2)
    return fig

# Callback pour le Scatter Plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('age-filter', 'value'),
     Input('sexe-filter', 'value'),
     Input('montant-filter', 'value')]
)
def update_scatter_plot(selected_tranche_age, selected_sexe, selected_montant):
    filtered_df = df[df['TrancheAge'].isin(selected_tranche_age) &
                     df['sex'].isin(selected_sexe) &
                     (df['Montant'] >= selected_montant[0]) &
                     (df['Montant'] <= selected_montant[1])]


    fig = px.scatter(filtered_df, x='Fréquence', y='Récence',

                     )

    fig.update_layout(title='Scatter Plot de Fréquence vs Récence')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
