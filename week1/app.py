from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/Dash-Course/US-Exports/2011_us_ag_exports.csv")

y_var: list[str] = ["beef", "pork", "fruits fresh"]
fig = px.bar(df[df["state"] == "Alabama"], x='state', y=y_var, title="Beef, Pork, Fruits by State")

app = Dash(__name__)

app.layout = html.Div([
    html.Div(id="my-title", children="US Agricultural Exports in 2011"), 
    dcc.Dropdown(id='state-dropdown', className='state-dropdown',
        options=df["state"],
        value='Alabama', 
        multi = True
    ), 
    dcc.Graph(figure=fig, id="graph1", className="graph1")
])

@callback (
    Output(component_id="graph1", component_property="figure"), 
    Input(component_id="state-dropdown", component_property="value"), 
    prevent_initial_call = True
)
def update_graph(states_selected: list[str]):
    new_df = df[df["state"].isin(states_selected)]
    new_fig = px.bar(new_df, x="state", y=y_var, title="Beef, Pork, Fruits by State")
    return new_fig

if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload=True)
