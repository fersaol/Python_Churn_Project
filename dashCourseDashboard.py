from dash import Dash,dcc,html,Input,Output,callback,State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_csv("churn.csv").head(100)
df = df.drop(columns=["RowNumber","Surname","CustomerId"])
for i in ["HasCrCard","IsActiveMember","Exited"]:
    df[i] = df[i].astype("bool")

options_uni = df.columns
options_bi = df.select_dtypes(include="number").columns
cate_options = df.select_dtypes(exclude="number").columns

app = Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1',colors={"background":"black","border":"#486A63","primary":"#14B492"},
        children=[
        dcc.Tab(label='Univariate Analysis', value='tab-1',children=[
            html.Div([
                html.Label('Eje X:'),
                dcc.Dropdown(
                    id='dropdownUni1',
                    options=options_uni,
                    value='CreditScore'
                ),
                html.Label("Activate Segmentation:"),
                dcc.RadioItems(id="segmentActivation",
                               options=["Yes","No"],
                               value="No"),
                html.Label('Segment:'),
                dcc.Dropdown(
                    id='segmentUni1',
                    options=cate_options,
                    value='Geography'
                ),
                dcc.Graph(
                    id='uniGraph1',
                    figure={})])
        ]),
        dcc.Tab(label='Bi-Multivariate Analysis', value='tab-2', children=[
            html.Div([
                html.Label("Analysis Type:"),
                dcc.RadioItems(options=["Scatter","CountPlot","HeatMap"],
                                value="Scatter",
                                id="BiAnalysis",
                                inline=True,),
                html.Br(),
                html.Label("Activate Segmentation:"),
                dcc.RadioItems(id="segmentActivationBi",
                                options=["Yes","No"],
                                value="No"),
                html.Label('Segment:'),
                dcc.Dropdown(
                    id='segmentBi',
                    options=cate_options,
                    value='Geography'
                ),
                html.Br(),
                html.Label('Eje X:'),
                dcc.Dropdown(
                    id='dropdownBi1',
                    options=options_bi,
                    value='Balance'
                ),
                html.Br(),
                html.Label('Eje Y:'),
                dcc.Dropdown(
                    id='dropdownBi2',
                    options=options_bi,
                    value='EstimatedSalary'
                    ),
                html.Br(),
                html.Label("Activate Size:"),
                dcc.RadioItems(id="SizeActivationBi",
                                options=["Yes","No"],
                                value="No"),
                html.Label("Choose a Bubble Size"),
                dcc.Dropdown(
                                options=options_bi,
                                id="bubbleSize",
                                value="CreditScore"),
                dcc.Graph(id='biGraph1',figure={})])])
    ])
])
@callback(Output(component_id="uniGraph1",component_property="figure"),
            Input(component_id="dropdownUni1",component_property="value"),
                Input(component_id="segmentActivation",component_property="value"),
                    Input(component_id="segmentUni1",component_property="value"))
def updateGraphTab1(xaxis,seg_activation,segment):
    col_type = str(df[xaxis].dtypes)
    if col_type in ["int64","float64"]:
        if seg_activation == "No":
            figUni1 = px.histogram(data_frame=df,x=xaxis,marginal="box",template="plotly_dark")
        else:
            figUni1 = px.histogram(data_frame=df,x=xaxis,marginal="box",
                                    color=df[segment].astype(str),template="plotly_dark")
        return figUni1
    else:
        figUni2 = px.bar(data_frame=df,x=xaxis,color=xaxis,template="plotly_dark")
        return figUni2

@callback(Output(component_id="biGraph1",component_property="figure"),
            Input(component_id="BiAnalysis",component_property="value"),
                Input(component_id="dropdownBi2",component_property="value"),
                    Input(component_id="dropdownBi1",component_property="value"),
                        Input(component_id="segmentActivationBi",component_property="value"),
                            Input(component_id="segmentBi",component_property="value"),
                                Input(component_id="bubbleSize",component_property="value"),
                                    Input(component_id="SizeActivationBi",component_property="value"))
def updateGraphTab2(analysis,yaxis,xaxis,acti_seg,segment,size,acti_size):
    if acti_seg == "No":
        if acti_size == "No":
            if analysis=="Scatter":
                figBi = px.scatter(data_frame=df,y=yaxis,x=xaxis,template="plotly_dark")
            elif analysis == "Countplot":
                figBi = px.bar(data_frame=df,x=xaxis,template="plotly_dark")
            else:
                figBi = px.density_heatmap(df[options_bi].corr("pearson"))

    elif acti_seg == "No":
        if acti_size == "Yes":
            if analysis=="Scatter":
                figBi = px.scatter(data_frame=df,y=yaxis,x=xaxis,size=size,template="plotly_dark")
            elif analysis == "Countplot":
                figBi = px.bar(data_frame=df,x=xaxis,template="plotly_dark")
            else:
                figBi = px.density_heatmap(df[options_bi].corr("pearson"))

    elif acti_seg == "Yes":
        if acti_size == "No":
            if analysis=="Scatter":
                figBi = px.scatter(data_frame=df,y=yaxis,x=xaxis,color=segment,template="plotly_dark")
            elif analysis == "Countplot":
                figBi = px.bar(data_frame=df,x=xaxis,color=segment,template="plotly_dark")
            else:
                figBi = px.density_heatmap(df[options_bi].corr("pearson"))


    elif acti_seg == "Yes":
        if acti_size == "Yes":
            if analysis=="Scatter":
                figBi = px.scatter(data_frame=df,y=yaxis,x=xaxis,color=segment,size=size,template="plotly_dark")
            elif analysis == "Countplot":
                figBi = px.bar(data_frame=df,x=xaxis,color=segment,template="plotly_dark")
            else:
                figBi = px.density_heatmap(df[options_bi].corr("pearson"))
        return figBi


if __name__ == '__main__':
    app.run_server(debug=True)
