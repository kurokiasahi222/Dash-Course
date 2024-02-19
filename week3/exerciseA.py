from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Dash-Course/US-Exports/2011_us_ag_exports.csv')

app = Dash(__name__)

app.layout = html.Div([
   html.Div("Us Agricultural Exports in 2011", id="my-title"),
   dcc.Dropdown(id="state-dropdown", options=df.state.unique(), multi=True),
   html.Button("submit", id="state-button", disabled=True),
   html.Div(
      dbc.Alert("Please select states", color="warning", id="alert"),
   ), 
   dcc.Graph(id="graph1")
])

@app.callback(Output('state-button', 'disabled'),
              Output("alert", "is_open"), 
              [Input('state-dropdown', 'value')], 
              prevent_initial_call=True, 
            )
def set_button_enabled_state(states_selected):
    if states_selected and len(states_selected) > 0:
       return False, False
    return True, True

@app.callback(
   Output(component_id='graph1', component_property='figure'),
   Input(component_id="state-button", component_property="n_clicks"), 
   State(component_id='state-dropdown', component_property='value'),
   prevent_initial_call=True
)
def update_graph(n_clicks, states_selected):
    if (n_clicks > 0):
        df_states = df[df.state.isin(states_selected)]
        fig1 = px.bar(data_frame=df_states, x='state', y=['beef','pork','fruits fresh'])
        return fig1
    
    return px.bar()

if __name__ == '__main__':
  app.run(debug=True)