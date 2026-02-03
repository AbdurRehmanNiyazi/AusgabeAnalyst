"""
Visualization Module
Creates charts and plots for expense analysis
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional


class ExpenseVisualizer:
    """Creates visualizations for expense data"""

    def __init__(self):
        """Initialize visualizer with color schemes"""
        self.color_scheme = {
            'income': '#2ecc71',
            'expense': '#e74c3c',
            'primary': '#3498db',
            'secondary': '#9b59b6'
        }

    def create_monthly_bar_chart(self, monthly_data: pd.DataFrame) -> go.Figure:
        """
        Create a bar chart showing monthly income and expenses

        Args:
            monthly_data: DataFrame with monthly totals

        Returns:
            Plotly figure
        """
        if monthly_data.empty:
            return self._create_empty_chart("No data available for monthly chart")

        # Pivot data for grouped bar chart
        pivot_data = monthly_data.pivot(index='month', columns='type', values='amount').fillna(0)

        fig = go.Figure()

        # Add bars for each type
        if 'Credit' in pivot_data.columns:
            fig.add_trace(go.Bar(
                name='Income',
                x=pivot_data.index,
                y=pivot_data['Credit'],
                marker_color=self.color_scheme['income']
            ))

        if 'Debit' in pivot_data.columns:
            fig.add_trace(go.Bar(
                name='Expenses',
                x=pivot_data.index,
                y=pivot_data['Debit'],
                marker_color=self.color_scheme['expense']
            ))

        fig.update_layout(
            title='Monthly Income vs Expenses',
            xaxis_title='Month',
            yaxis_title='Amount (€)',
            barmode='group',
            template='plotly_white',
            hovermode='x unified'
        )

        return fig

    def create_category_pie_chart(self, category_data: pd.DataFrame) -> go.Figure:
        """
        Create a pie chart showing expense distribution by category

        Args:
            category_data: DataFrame with category totals

        Returns:
            Plotly figure
        """
        if category_data.empty:
            return self._create_empty_chart("No data available for category chart")

        fig = px.pie(
            category_data,
            values='total_amount',
            names='category',
            title='Expense Distribution by Category',
            hole=0.3  # Makes it a donut chart
        )

        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Amount: €%{value:.2f}<br>Percentage: %{percent}'
        )

        fig.update_layout(
            template='plotly_white'
        )

        return fig

    def create_timeline_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create a timeline chart showing balance over time

        Args:
            df: DataFrame with all transactions

        Returns:
            Plotly figure
        """
        if df.empty:
            return self._create_empty_chart("No data available for timeline chart")

        # Calculate cumulative balance
        df_sorted = df.sort_values('value_date').copy()
        df_sorted['cumulative_balance'] = df_sorted['amount'].cumsum()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_sorted['value_date'],
            y=df_sorted['cumulative_balance'],
            mode='lines+markers',
            name='Balance',
            line=dict(color=self.color_scheme['primary'], width=2),
            marker=dict(size=4),
            fill='tozeroy',
            fillcolor='rgba(52, 152, 219, 0.1)'
        ))

        fig.update_layout(
            title='Account Balance Over Time',
            xaxis_title='Date',
            yaxis_title='Balance (€)',
            template='plotly_white',
            hovermode='x unified'
        )

        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

        return fig

    def create_category_bar_chart(self, category_data: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Create a horizontal bar chart for top spending categories

        Args:
            category_data: DataFrame with category totals
            top_n: Number of top categories to show

        Returns:
            Plotly figure
        """
        if category_data.empty:
            return self._create_empty_chart("No data available for category bar chart")

        # Get top N categories
        top_categories = category_data.head(top_n)

        fig = go.Figure(go.Bar(
            x=top_categories['total_amount'],
            y=top_categories['category'],
            orientation='h',
            marker_color=self.color_scheme['secondary'],
            text=top_categories['total_amount'].apply(lambda x: f'€{x:.2f}'),
            textposition='auto'
        ))

        fig.update_layout(
            title=f'Top {top_n} Spending Categories',
            xaxis_title='Total Amount (€)',
            yaxis_title='Category',
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'}
        )

        return fig

    def create_income_expense_comparison(self, monthly_data: pd.DataFrame) -> go.Figure:
        """
        Create a line chart comparing income and expenses over time

        Args:
            monthly_data: DataFrame with monthly totals

        Returns:
            Plotly figure
        """
        if monthly_data.empty:
            return self._create_empty_chart("No data available for comparison chart")

        # Pivot data
        pivot_data = monthly_data.pivot(index='month', columns='type', values='amount').fillna(0)

        fig = go.Figure()

        if 'Credit' in pivot_data.columns:
            fig.add_trace(go.Scatter(
                x=pivot_data.index,
                y=pivot_data['Credit'],
                mode='lines+markers',
                name='Income',
                line=dict(color=self.color_scheme['income'], width=3),
                marker=dict(size=8)
            ))

        if 'Debit' in pivot_data.columns:
            fig.add_trace(go.Scatter(
                x=pivot_data.index,
                y=pivot_data['Debit'],
                mode='lines+markers',
                name='Expenses',
                line=dict(color=self.color_scheme['expense'], width=3),
                marker=dict(size=8)
            ))

        fig.update_layout(
            title='Monthly Income vs Expenses Trend',
            xaxis_title='Month',
            yaxis_title='Amount (€)',
            template='plotly_white',
            hovermode='x unified'
        )

        return fig

    def _create_empty_chart(self, message: str) -> go.Figure:
        """
        Create an empty chart with a message

        Args:
            message: Message to display

        Returns:
            Empty plotly figure
        """
        fig = go.Figure()

        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )

        fig.update_layout(
            template='plotly_white',
            xaxis={'visible': False},
            yaxis={'visible': False}
        )

        return fig