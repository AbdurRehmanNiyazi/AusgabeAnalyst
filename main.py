"""
AusgabeAnalyst - Main Streamlit Application
MVC Architecture Implementation
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pdf_parser import VolksbankPDFParser
from src.categorizer import TransactionCategorizer
from src.data_manager import DataManager
from src.visualizer import ExpenseVisualizer

# Page configuration
st.set_page_config(
    page_title="AusgabeAnalyst",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


class ExpenseTrackerApp:
    """Main application controller"""

    def __init__(self):
        """Initialize the application"""
        self.parser = VolksbankPDFParser()
        self.categorizer = TransactionCategorizer()
        self.data_manager = DataManager(data_dir='data')
        self.visualizer = ExpenseVisualizer()

        # Initialize session state
        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = []

    def run(self):
        """Main application entry point"""
        # Sidebar
        self._render_sidebar()

        # Main content
        st.title("💰 AusgabeAnalyst")
        st.markdown("---")

        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview",
            "📅 Monthly Analysis",
            "📂 Category Analysis",
            "📋 Transaction History"
        ])

        with tab1:
            self._render_overview_tab()

        with tab2:
            self._render_monthly_tab()

        with tab3:
            self._render_category_tab()

        with tab4:
            self._render_history_tab()

    def _render_sidebar(self):
        """Render the sidebar with upload and controls"""
        st.sidebar.title("🔧 Controls")

        # File upload section
        st.sidebar.header("📤 Upload Bank Statement")
        uploaded_file = st.sidebar.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload your Volksbank bank statement PDF"
        )

        if uploaded_file is not None:
            if st.sidebar.button("Process PDF", type="primary"):
                with st.spinner("Processing PDF..."):
                    self._process_uploaded_file(uploaded_file)

        st.sidebar.markdown("---")

        # Export section
        st.sidebar.header("📥 Export Data")
        if st.sidebar.button("Export to Excel"):
            self._export_data()

        st.sidebar.markdown("---")

        # Statistics
        st.sidebar.header("📈 Quick Stats")
        stats = self.data_manager.get_summary_statistics()

        st.sidebar.metric("Total Transactions", stats['total_transactions'])
        st.sidebar.metric("Net Savings", f"€{stats['net_savings']:.2f}")

        if stats['total_transactions'] > 0:
            st.sidebar.info(f"**Data Range:**\n{stats['date_range']}")

        # Add Delete Button (not working, giving error)

        st.sidebar.markdown("---")
        st.sidebar.header("⚠️ Danger Zone")
        if st.sidebar.button("Delete All Data", type="secondary", help="This will wipe your entire history!"):
            self.data_manager.clear_all_data()
            st.sidebar.success("All data deleted successfully.")
            st.rerun()

    def _process_uploaded_file(self, uploaded_file):
        """
        Process an uploaded PDF file

        Args:
            uploaded_file: Streamlit UploadedFile object
        """
        try:
            # Save temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Parse PDF
            result = self.parser.parse_pdf(temp_path)

            # Categorize transactions
            transactions = self.categorizer.categorize_batch(result['transactions'])

            # Add to database
            add_result = self.data_manager.add_transactions(transactions)

            # Clean up
            os.remove(temp_path)

            # Show results
            st.sidebar.success(f"""
            ✅ Processing complete!
            - Added: {add_result['added']} transactions
            - Skipped (duplicates): {add_result['skipped']} transactions
            """)

            # Force rerun to update displays
            st.rerun()

        except Exception as e:
            st.sidebar.error(f"Error processing file: {str(e)}")

    def _export_data(self):
        """Export data to Excel"""
        try:
            output_path = f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            self.data_manager.export_to_excel(output_path)

            with open(output_path, 'rb') as f:
                st.sidebar.download_button(
                    label="Download Excel Report",
                    data=f,
                    file_name=output_path,
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )

            # Clean up
            os.remove(output_path)

        except Exception as e:
            st.sidebar.error(f"Export failed: {str(e)}")

    def _render_overview_tab(self):
        """Render the overview tab"""
        st.header("📊 Financial Overview")

        stats = self.data_manager.get_summary_statistics()

        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Income",
                f"€{stats['total_income']:.2f}",
                delta=None,
                delta_color="normal"
            )

        with col2:
            st.metric(
                "Total Expenses",
                f"€{stats['total_expenses']:.2f}",
                delta=None,
                delta_color="inverse"
            )

        with col3:
            savings_color = "normal" if stats['net_savings'] >= 0 else "inverse"
            st.metric(
                "Net Savings",
                f"€{stats['net_savings']:.2f}",
                delta=None,
                delta_color=savings_color
            )

        with col4:
            st.metric(
                "Current Balance",
                f"€{stats['current_balance']:.2f}"
            )

        st.markdown("---")

        # Timeline chart
        df = self.data_manager.load_all_transactions()
        if not df.empty:
            st.subheader("Balance Timeline")
            fig = self.visualizer.create_timeline_chart(df)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📭 No transactions yet. Upload a bank statement to get started!")

    def _render_monthly_tab(self):
        """Render the monthly analysis tab"""
        st.header("📅 Monthly Analysis")

        monthly_data = self.data_manager.get_monthly_summary()

        if not monthly_data.empty:
            # Monthly bar chart
            st.subheader("Monthly Income vs Expenses")
            fig = self.visualizer.create_monthly_bar_chart(monthly_data)
            st.plotly_chart(fig, use_container_width=True)

            # Trend line
            st.subheader("Trend Analysis")
            fig = self.visualizer.create_income_expense_comparison(monthly_data)
            st.plotly_chart(fig, use_container_width=True)

            # Data table
            st.subheader("Monthly Summary Table")
            pivot_table = monthly_data.pivot(
                index='month',
                columns='type',
                values='amount'
            ).fillna(0)

            if 'Credit' in pivot_table.columns and 'Debit' in pivot_table.columns:
                pivot_table['Net'] = pivot_table['Credit'] - pivot_table['Debit']

            st.dataframe(
                pivot_table.style.format("€{:.2f}"),
                use_container_width=True
            )
        else:
            st.info("📭 No data available for monthly analysis")

    def _render_category_tab(self):
        """Render the category analysis tab"""
        st.header("📂 Category Analysis")

        category_data = self.data_manager.get_category_summary()

        if not category_data.empty:
            col1, col2 = st.columns(2)

            with col1:
                # Pie chart
                st.subheader("Expense Distribution")
                fig = self.visualizer.create_category_pie_chart(category_data)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Bar chart
                st.subheader("Top Categories")
                fig = self.visualizer.create_category_bar_chart(category_data)
                st.plotly_chart(fig, use_container_width=True)

            # Category table
            st.subheader("Category Breakdown")
            category_display = category_data.copy()
            category_display['total_amount'] = category_display['total_amount'].apply(
                lambda x: f"€{x:.2f}"
            )
            st.dataframe(category_display, use_container_width=True)
        else:
            st.info("📭 No expense data available for category analysis")

    def _render_history_tab(self):
        """Render the transaction history tab"""
        st.header("📋 Transaction History")

        df = self.data_manager.load_all_transactions()

        if not df.empty:
            # Filters
            col1, col2, col3 = st.columns(3)

            with col1:
                # Category filter
                categories = ['All'] + sorted(df['category'].unique().tolist())
                selected_category = st.selectbox("Filter by Category", categories)

            with col2:
                # Type filter
                types = ['All', 'Credit', 'Debit']
                selected_type = st.selectbox("Filter by Type", types)

            with col3:
                # Date range
                min_date = df['value_date'].min().date()
                max_date = df['value_date'].max().date()
                date_range = st.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )

            # Apply filters
            filtered_df = df.copy()

            if selected_category != 'All':
                filtered_df = filtered_df[filtered_df['category'] == selected_category]

            if selected_type != 'All':
                filtered_df = filtered_df[filtered_df['type'] == selected_type]

            if len(date_range) == 2:
                filtered_df = filtered_df[
                    (filtered_df['value_date'].dt.date >= date_range[0]) &
                    (filtered_df['value_date'].dt.date <= date_range[1])
                    ]

            # Display stats for filtered data
            st.markdown("### Filtered Results")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Transactions", len(filtered_df))

            with col2:
                total_amount = filtered_df['amount'].sum()
                st.metric("Total Amount", f"€{total_amount:.2f}")

            with col3:
                avg_amount = filtered_df['amount'].mean() if len(filtered_df) > 0 else 0
                st.metric("Average Amount", f"€{avg_amount:.2f}")

            # Display table
            display_df = filtered_df[[
                'value_date', 'description', 'category', 'amount', 'type'
            ]].copy()

            display_df['value_date'] = display_df['value_date'].dt.strftime('%Y-%m-%d')
            display_df['amount'] = display_df['amount'].apply(lambda x: f"€{x:.2f}")

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            # Download filtered data
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download Filtered Data (CSV)",
                data=csv,
                file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("📭 No transactions available")


def main():
    """Application entry point"""
    app = ExpenseTrackerApp()
    app.run()


if __name__ == "__main__":
    main()