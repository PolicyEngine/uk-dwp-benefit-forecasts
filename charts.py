import plotly.express as px
import plotly.graph_objects as go

def create_benefit_chart(df, benefit, spending):
    subset = df[(df.Type == ("Spending" if spending else "Caseloads")) & (df["Benefit"] == benefit)]
    fig = px.line(
        subset,
        x="Year",
        y="Value",
        color="Forecast year",
    ).update_layout(
        height=600,
        title=f"Benefit {'spending' if spending else 'caseload'} forecast for {benefit}",
        width=800,
        yaxis_range=[0, subset.Value.max()],
        yaxis_tickprefix="£" if spending else "",
        yaxis_title="Spending" if spending else "Caseload",
        xaxis_title="Financial year",
    )

    # Make all lines dotted

    for i, trace in enumerate(fig.data):
        trace.line.dash = "dot"

    # Add a solid line with the actual data
    outturns = df[(df.Type == ("Spending" if spending else "Caseloads")) & (~df.Forecast) & (df["Benefit"] == benefit) & (df["Forecast year"] == 2024)]

    fig.add_trace(
        go.Scatter(
            x=outturns.Year,
            y=outturns.Value,
            mode="lines",
            name="Outturn",
            line=dict(color="black", width=3),
        )
    )

    fig.update_layout(
        xaxis_range=[2017, 2030],
    )

    return fig