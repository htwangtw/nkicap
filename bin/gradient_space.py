from pathlib import Path
import json
import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from nkicap.gradient import map_space
from nkicap.utils import read_tsv, get_project_path


def cap_to_gradient(data_path=None):
    """Map all cap map to gradient space on real data."""
    if Path(data_path).exists:
        return read_tsv(data_path)
    # load data collection
    path_cap_collection = Path(get_project_path()) / "data/cap.json"
    with open(path_cap_collection) as json_file:
        path_cap = json.load(json_file)

    # load group cap and map to gradient space
    path_group_cap = path_cap["group"]
    group_cap = read_tsv(path_group_cap, index_col=0)
    gradient_space = {
        label: {"group": map_space(cap_val)}
        for label, cap_val in group_cap.items()
    }

    # load subject cap and map to gradient space
    for sub, path in path_cap["subject"].items():
        sub_cap = read_tsv(path, index_col=0)
        for label, cap_val in sub_cap.items():
            gradient_space[label][sub] = map_space(cap_val)

    # covert to dataframe
    collect = []
    for key in gradient_space:
        df = pd.DataFrame(gradient_space[key], index=[f"Gradient {i+1}" for i in range(3)]).T
        df["CAP"] = key[-2:]
        df.index.name = "participant_id"
        df = df.reset_index()
        collect.append(df)
    gradient_space = pd.concat(collect, axis=0)
    if data_path:
        gradient_space.to_csv(data_path, sep="\t", index=False)
    return gradient_space

gradient_space = cap_to_gradient(Path(get_project_path()) / "data/cap_gradient_space.tsv")

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="gradient-space"),
    html.P("CAP label"),
    dcc.Checklist(
        id='cap-label',
        options=[
        {'label': f'{i}', 'value': f'{i}'} for i in range (1, 9)],
        value=["1", "2"],
        labelStyle={'display': 'inline-block'}
    ),
])

@app.callback(
    Output("gradient-space", "figure"),
    [Input("cap-label", "value")])
def update_chart(value):
    mask = []
    for i in value:
        mask.extend(gradient_space[gradient_space["CAP"] == int(i)].index.tolist())
    fig = px.scatter_3d(gradient_space.iloc[mask, :],
        x='Gradient 1', y='Gradient 2', z='Gradient 3',
        range_x=[-1, 1], range_y=[-1, 1], range_z=[-1, 1],
        range_color=[1, 8],
        color="CAP", opacity=0.5, width=800, height=500)
    return fig

app.run_server(debug=True)

if __name__ == '__main__':
    app.run_server()