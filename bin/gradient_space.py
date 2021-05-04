"""Explore the plot in plotly."""

from pathlib import Path

import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from nkicap.gradient import cap_to_gradient
from nkicap.utils import get_project_path


gradient_space = cap_to_gradient(
    Path(get_project_path()) / "data/cap_gradient_space.tsv"
)

gradient_space["type"] = None
mask_group = gradient_space["participant_id"] == "group"
gradient_space.loc[mask_group, "type"] = "group"
gradient_space.loc[~mask_group, "type"] = "sub"


app = JupyterDash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id="gradient-space"),
        html.P("CAP label"),
        dcc.Checklist(
            id="cap-label",
            options=[{"label": f"{i}", "value": f"{i}"} for i in range(1, 9)],
            value=["1", "2"],
            labelStyle={"display": "inline-block"},
        ),
    ]
)


@app.callback(
    Output("gradient-space", "figure"), [Input("cap-label", "value")]
)
def update_chart(value):
    mask = []
    for i in value:
        cap = gradient_space[gradient_space["CAP"] == int(i)]
        mask.extend(cap.index.tolist())

    fig = px.scatter_3d(
        gradient_space.iloc[mask, 1:],
        x="Gradient 1",
        y="Gradient 2",
        z="Gradient 3",
        range_x=[-1, 1],
        range_y=[-1, 1],
        range_z=[-1, 1],
        range_color=[1, 8],
        symbol="type",
        color="CAP",
        opacity=0.1,
        width=800,
        height=500,
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
