import pandas as pd
import plotly.graph_objects as go


class BioTwinControlCharts:
    """
    Generates standardized, publication-grade interactive Plotly charts 
    for monitoring latent variable soft-sensor metrics in real time.
    """

    @staticmethod
    def build_statistical_trend_chart(
        df_history: pd.DataFrame,
        value_column: str,
        ucl_column: str,
        title: str,
        line_color: str = "#0066CC"
    ) -> go.Figure:
        """
        Constructs an explicit Statistical Process Control (SPC) line chart 
        mapping streaming values against a predefined Upper Control Limit boundary.
        """
        fig = go.Figure()

        # Handle empty histories gracefully before rendering canvas bounds
        if df_history.empty or value_column not in df_history.columns:
            fig.update_layout(title="No live stream telemetry data captured yet.", template="plotly_dark")
            return fig

        # 1. Plot the running calculated metric scores
        fig.add_trace(
            go.Scatter(
                x=df_history["timestamp"] if "timestamp" in df_history.columns else df_history.index,
                y=df_history[value_column],
                mode="lines+markers",
                name=value_column.upper().replace("_", " "),
                line=dict(color=line_color, width=2.5),
                marker=dict(size=4)
            )
        )

        # 2. Overlay the static or dynamic statistical GxP Upper Control Limit (UCL)
        if ucl_column in df_history.columns:
            fig.add_trace(
                go.Scatter(
                    x=df_history["timestamp"] if "timestamp" in df_history.columns else df_history.index,
                    y=df_history[ucl_column],
                    mode="lines",
                    name="Upper Control Limit (UCL)",
                    line=dict(color="#FF3333", width=2, dash="dash")
                )
            )

        # 3. Apply standard clinical dark-room UI parameters
        fig.update_layout(
            title=dict(text=title, font=dict(size=16, color="#FFFFFF")),
            template="plotly_dark",
            height=320,
            margin=dict(l=40, r=20, t=50, b=40),
            hovermode="x unified",
            xaxis=dict(
                title="Historical Execution Windows",
                showgrid=True,
                gridcolor="#2A2E3D",
                zeroline=False
            ),
            yaxis=dict(
                title="Statistical Score Magnitude",
                showgrid=True,
                gridcolor="#2A2E3D",
                zeroline=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig
