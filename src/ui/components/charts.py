import pandas as pd
import plotly.graph_objects as go


class BioTwinControlCharts:
    @staticmethod
    def build_statistical_trend_chart(df_history: pd.DataFrame, value_col: str, ucl_col: str, title: str, trace_color: str) -> go.Figure:
        fig = go.Figure()
        if df_history.empty or value_col not in df_history.columns:
            fig.update_layout(title="Awaiting pipeline snapshot ingestion updates.", template="plotly_dark")
            return fig

        x_axis = df_history["timestamp"] if "timestamp" in df_history.columns else df_history.index
        
        fig.add_trace(go.Scatter(x=x_axis, y=df_history[value_col], mode="lines+markers", name=value_col.upper(), line=dict(color=trace_color, width=2.5)))
        if ucl_col in df_history.columns:
            fig.add_trace(go.Scatter(x=x_axis, y=df_history[ucl_col], mode="lines", name="Upper Control Limit", line=dict(color="red", dash="dash", width=2)))

        fig.update_layout(
            title=dict(text=title, font=dict(size=14)),
            template="plotly_dark", height=280,
            margin=dict(l=30, r=15, t=40, b=30),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        return fig
