import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import duckdb
import time

# Set page configuration
st.set_page_config(
    page_title="Supply Chain Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Card styling */
    .metric-card {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Divider styling */
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(75, 192, 192, 0), rgba(75, 192, 192, 0.75), rgba(75, 192, 192, 0));
    }
    
    /* Section header styling */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #4bc0c0;
    }
</style>
""", unsafe_allow_html=True)

# Caching the function to load the dataset
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Loading the data
with st.spinner('Loading data...'):
    df = load_data('supply_chain_data.csv')

# Dashboard header with animation
st.markdown(
    """
    <div style="text-align: center; animation: fadeIn 1.5s ease-in-out;">
        <h1 style="font-size: 3.5em; font-weight: 700; color: #4bc0c0; margin-bottom: 0.5em;">
            📊 Supply Chain Analytics
        </h1>
        <p style="font-size: 1.2em; color: #a3a8b8; margin-bottom: 2em;">
            Interactive insights for optimized supply chain management
        </p>
    </div>
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Dataset exploration option
with st.expander("📋 Explore Dataset"):
    st.write(df)

# Executive summary section
st.markdown(
    """
    <div class="metric-card">
        <div class="section-header">Executive Summary</div>
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 12px; display: flex; align-items: center;">
                <span style="background: #4bc0c0; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">1</span>
                <strong style="color: #4bc0c0;">Revenue Growth:</strong> Skincare products generated major revenue, boosting overall supply chain growth
            </li>
            <li style="margin-bottom: 12px; display: flex; align-items: center;">
                <span style="background: #9966ff; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">2</span>
                <strong style="color: #9966ff;">Quality Control Insight:</strong>Most cost and defects arise from failed and pending inspections.
            </li>
            <li style="margin-bottom: 12px; display: flex; align-items: center;">
                <span style="background: #36a2eb; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">3</span>
                <strong style="color: #36a2eb;">Order & Transportation Pattern:</strong> Most orders use road transport; major quantity comes from Kolkata.
            </li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["Key Metrics", "Production & Manufacturing", "Logistics & Transportation"])

# === TAB 1: KEY METRICS ===
with tab1:
    # KPI Row - 3 main metrics with improved styling
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
    with kpi_col1:
        # Total Revenue with improved styling
        query = """
        SELECT SUM("Revenue generated")::DECIMAL(8, 2) AS total_revenue
        FROM df
        """
        result = duckdb.query(query).df()
        total_revenue = result['total_revenue'][0]
        
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="number",
            value=total_revenue,
            title={"text": "Total Revenue", "font": {"size": 24, "color": "#ffffff"}},
            number={"prefix": "$", "valueformat": ".2f", "font": {"size": 32, "color": "#4bc0c0"}},
            domain={"x": [0, 1], "y": [0, 1]}
        ))
        
        fig.update_layout(
            height=220,
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            plot_bgcolor='rgba(30, 33, 48, 0)',
            font_color='white',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with kpi_col2:
        # Total Orders Quantity with improved styling
        query = """
        SELECT SUM("Order quantities") AS "Total Orders Quantity"
        FROM df
        """
        result = duckdb.query(query).fetchall()
        total_orders_quantity = result[0][0]
        
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="number",
            value=total_orders_quantity,
            title={"text": "Total Orders", "font": {"size": 24, "color": "#ffffff"}},
            number={"valueformat": ",.0f", "font": {"size": 32, "color": "#9966ff"}},
            domain={"x": [0, 1], "y": [0, 1]}
        ))
        
        fig.update_layout(
            height=220,
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            plot_bgcolor='rgba(30, 33, 48, 0)',
            font_color='white',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with kpi_col3:
        # Total Availability with improved styling
        total_availability = df['Availability'].sum()
        
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="number",
            value=total_availability,
            title={"text": "Total Availability", "font": {"size": 24, "color": "#ffffff"}},
            number={"font": {"size": 32, "color": "#36a2eb"}},
            domain={"x": [0, 1], "y": [0, 1]}
        ))
        
        fig.update_layout(
            height=220,
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            plot_bgcolor='rgba(30, 33, 48, 0)',
            font_color='white',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Revenue analysis section
    st.markdown("<div class='section-header'>Revenue Analysis</div>", unsafe_allow_html=True)
    
    revenue_col1, revenue_col2 = st.columns(2)
    
    with revenue_col1:
        # Revenue by Product Type - Bar chart with consistent colors
        query = """
        SELECT "Product Type",
        SUM("Revenue generated")::DECIMAL(8, 2) AS total_revenue
        FROM df
        GROUP BY "Product Type"
        ORDER BY total_revenue DESC
        """
        result = duckdb.query(query).df()
        
        fig = px.bar(result, 
                x='Product type', 
                y='total_revenue', 
                title='Revenue by Product Type',
                labels={'total_revenue': 'Total Revenue ($)', 'Product type': 'Product Type'},
                color_discrete_sequence=['#4bc0c0', '#9966ff', '#36a2eb'])
        
        fig.update_layout(
            xaxis_title="Product Type",
            yaxis_title="Total Revenue ($)",
            yaxis_tickprefix="$",
            yaxis_tickformat=".2f",
            margin=dict(l=40, r=40, t=50, b=40),
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            bargap=0.2,
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with revenue_col2:
        # Revenue Distribution by Location - Pie chart with consistent colors
        query = """
        SELECT "location",
               SUM("Revenue generated")::DECIMAL(8, 2) AS total_revenue
        FROM df
        GROUP BY "location"
        ORDER BY total_revenue DESC
        """
        result = duckdb.query(query).df()
        
        fig = px.pie(result, 
                values='total_revenue', 
                names='Location', 
                title='Revenue Distribution by Location',
                labels={'total_revenue': 'Total Revenue ($)', 'Location': 'Location'},
                color_discrete_sequence=['#4bc0c0', '#9966ff', '#36a2eb', '#ffcd56', '#ff6384'])
        
        fig.update_layout(
            margin=dict(l=40, r=40, t=50, b=40),
            font=dict(size=14, color='white'),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.3,
                xanchor='center',
                x=0.5
            ),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Profitability analysis
    st.markdown("<div class='section-header'>Profitability Analysis</div>", unsafe_allow_html=True)
    
    profit_col1, profit_col2 = st.columns(2)
    
    with profit_col1:
        # Cost vs Price Analysis - Grouped bar chart
        price_costs_by_product = df.groupby('Product type').agg(
            Price=('Price', 'sum'),
            Manufacturing_costs=('Manufacturing costs', 'sum')
        ).reset_index()
        
        price_costs_by_product['Price'] = price_costs_by_product['Price'].round(2)
        price_costs_by_product['Manufacturing_costs'] = price_costs_by_product['Manufacturing_costs'].round(2)
        price_costs_by_product['Profit_margin'] = (price_costs_by_product['Price'] - price_costs_by_product['Manufacturing_costs']).round(2)
        price_costs_by_product = price_costs_by_product.sort_values(by='Product type')
        
        fig = px.bar(price_costs_by_product, 
                x='Product type', 
                y=['Price', 'Manufacturing_costs'],
                title='Price vs Manufacturing Costs by Product',
                labels={'value': 'Amount ($)', 'Product type': 'Product Type', 'variable': 'Cost Type'},
                color_discrete_sequence=['#4bc0c0', '#ff6384'],
                barmode='group')
        
        fig.update_layout(
            xaxis_title="Product Type",
            yaxis_title="Amount ($)",
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            bargap=0.2,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.3,
                xanchor='center',
                x=0.5
            ),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with profit_col2:
        # Overall Profitability - Bar chart with diverging colors
        profitability_by_product = df.groupby('Product type').agg(
            Revenue=('Revenue generated', 'sum'),
            Cost=('Costs', 'sum')
        ).reset_index()
        
        profitability_by_product['Profit'] = (profitability_by_product['Revenue'] - profitability_by_product['Cost']).round(2)
        profitability_by_product = profitability_by_product.sort_values(by='Product type')
        
        fig = px.bar(profitability_by_product, 
                x='Product type', 
                y='Profit',
                title='Overall Profitability by Product Type',
                labels={'Profit': 'Profit ($)', 'Product type': 'Product Type'},
                color='Profit',
                color_continuous_scale=['#ff6384', '#ffb1c1', '#f8f9fa', '#9ee4d9', '#4bc0c0'],
                color_continuous_midpoint=0)
        
        fig.update_layout(
            xaxis_title="Product Type",
            yaxis_title="Profit ($)",
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            bargap=0.2,
        )
        
        st.plotly_chart(fig, use_container_width=True)

# === TAB 2: PRODUCTION & MANUFACTURING ===
with tab2:
    # Production metrics
    st.markdown("<div class='section-header'>Production & Stock Analysis</div>", unsafe_allow_html=True)
    
    # Stock and Lead Time Gauges
    gauge_col1, gauge_col2 = st.columns(2)
    
    with gauge_col1:
        query = """
        SELECT SUM("stock levels") AS "Stock Levels",
               SUM("Lead Times") AS "Lead Times"
        FROM df;
        """
        result = duckdb.query(query).df()
        total_stock_levels = result['Stock Levels'][0]
        total_lead_times = result['Lead Times'][0]
        
        fig_stock_levels = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total_stock_levels,
            title={'text': "Total Stock Levels", 'font': {'size': 24, 'color': 'white'}},
            gauge={
                'axis': {'range': [0, max(total_stock_levels, total_lead_times) + 100], 'tickfont': {'color': 'white'}},
                'bar': {'color': "#4bc0c0"},
                'steps': [
                    {'range': [0, max(total_stock_levels, total_lead_times) / 3], 'color': "rgba(75, 192, 192, 0.2)"},
                    {'range': [max(total_stock_levels, total_lead_times) / 3, max(total_stock_levels, total_lead_times) * 2/3], 'color': "rgba(75, 192, 192, 0.4)"},
                    {'range': [max(total_stock_levels, total_lead_times) * 2/3, max(total_stock_levels, total_lead_times)], 'color': "rgba(75, 192, 192, 0.6)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 2},
                    'thickness': 0.75,
                    'value': total_stock_levels
                }
            },
            number={'font': {'color': '#4bc0c0', 'size': 28}}
        ))
        
        fig_stock_levels.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=60, b=20),
            font=dict(color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
        )
        
        st.plotly_chart(fig_stock_levels, use_container_width=True)
    
    with gauge_col2:
        fig_lead_times = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total_lead_times,
            title={'text': "Total Lead Times", 'font': {'size': 24, 'color': 'white'}},
            gauge={
                'axis': {'range': [0, max(total_stock_levels, total_lead_times) + 100], 'tickfont': {'color': 'white'}},
                'bar': {'color': "#9966ff"},
                'steps': [
                    {'range': [0, max(total_stock_levels, total_lead_times) / 3], 'color': "rgba(153, 102, 255, 0.2)"},
                    {'range': [max(total_stock_levels, total_lead_times) / 3, max(total_stock_levels, total_lead_times) * 2/3], 'color': "rgba(153, 102, 255, 0.4)"},
                    {'range': [max(total_stock_levels, total_lead_times) * 2/3, max(total_stock_levels, total_lead_times)], 'color': "rgba(153, 102, 255, 0.6)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 2},
                    'thickness': 0.75,
                    'value': total_lead_times
                }
            },
            number={'font': {'color': '#9966ff', 'size': 28}}
        ))
        
        fig_lead_times.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=60, b=20),
            font=dict(color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
        )
        
        st.plotly_chart(fig_lead_times, use_container_width=True)
    
    # Manufacturing analysis
    st.markdown("<div class='section-header'>Manufacturing Analysis</div>", unsafe_allow_html=True)
    
    manuf_col1, manuf_col2 = st.columns(2)
    
    with manuf_col1:
        # Manufacturing Costs by Product Type - Bar chart with gradients
        costs_by_product = df.groupby('Product type')['Manufacturing costs'].sum().reset_index()
        costs_by_product['Manufacturing costs'] = costs_by_product['Manufacturing costs'].round(2)
        costs_by_product = costs_by_product.sort_values(by='Manufacturing costs', ascending=False)
        
        fig = px.bar(costs_by_product, 
                x='Product type', 
                y='Manufacturing costs', 
                title='Manufacturing Costs by Product',
                labels={'Manufacturing costs': 'Manufacturing Costs ($)', 'Product type': 'Product Type'},
                color='Manufacturing costs',
                color_continuous_scale=['#36a2eb', '#4bc0c0', '#9966ff'])
        
        fig.update_layout(
            xaxis_title="Product Type",
            yaxis_title="Manufacturing Costs ($)",
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            bargap=0.2,
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with manuf_col2:
        # Manufacturing Costs vs Production Volumes - Scatter plot with trend line
        production_summary = df.groupby('Production volumes')['Manufacturing costs'].sum().reset_index()
        
        fig = px.scatter(production_summary, 
                x='Production volumes', 
                y='Manufacturing costs', 
                trendline='ols',
                title='Manufacturing Costs vs Production Volumes',
                labels={'Manufacturing costs': 'Manufacturing Costs ($)', 'Production volumes': 'Production Volumes'},
                color_discrete_sequence=['#4bc0c0'])
        
        fig.update_traces(marker=dict(size=10))
        
        fig.update_layout(
            xaxis_title="Production Volumes",
            yaxis_title="Manufacturing Costs ($)",
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
        )
        
        # Update trendline color
        for trace in fig.data:
            if trace.mode == 'lines':
                trace.line.color = '#ff6384'
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Quality and Defects Analysis
    st.markdown("<div class='section-header'>Quality & Defects Analysis</div>", unsafe_allow_html=True)
    
    defect_col1, defect_col2 = st.columns(2)
    
    with defect_col1:
        # Manufacturing Costs by Inspection Results - Pie chart with modern colors
        cost_summary = df.groupby('Inspection results').agg({'Manufacturing costs': 'sum'}).reset_index()
        total_costs = cost_summary['Manufacturing costs'].sum()
        cost_summary['Percentage Contribution'] = (cost_summary['Manufacturing costs'] / total_costs * 100).round(2)
        cost_summary['Manufacturing costs'] = cost_summary['Manufacturing costs'].astype(float).round(2)
        cost_summary['Percentage Contribution'] = cost_summary['Percentage Contribution'].astype(float).round(2)
        cost_summary = cost_summary.sort_values(by='Manufacturing costs', ascending=False)
        
        fig = px.pie(
            cost_summary,
            names='Inspection results',
            values='Manufacturing costs',
            title='Manufacturing Costs by Inspection Results',
            color_discrete_sequence=['#4bc0c0', '#9966ff', '#36a2eb', '#ffcd56', '#ff6384'],
            hole=0.4
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hoverinfo='label+value+percent'
        )
        
        fig.update_layout(
            font=dict(size=14, color='white'),
            showlegend=False,
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with defect_col2:
        # Defect Rates Analysis - Sunburst chart with modern colors
        sum_defect_rates = df.groupby('Inspection results')['Defect rates'].sum().reset_index()
        total_defect_rate = df['Defect rates'].sum()
        sum_defect_rates['Percentage of Total Defect Rate'] = (sum_defect_rates['Defect rates'] / total_defect_rate * 100)
        avg_defect_rate = df.groupby('Inspection results')['Defect rates'].mean().reset_index()
        result = pd.merge(sum_defect_rates, avg_defect_rate, on='Inspection results', suffixes=('_sum', '_avg'))
        result = result.sort_values(by='Defect rates_sum', ascending=False)
        
        fig = px.sunburst(result, path=['Inspection results'], values='Defect rates_sum',
                    hover_data=['Percentage of Total Defect Rate', 'Defect rates_avg'],
                    title='Defect Rates by Inspection Results',
                    color='Defect rates_sum',
                    color_continuous_scale=['#4bc0c0', '#9966ff', '#36a2eb'])
        
        fig.update_layout(
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)', 
            paper_bgcolor='rgba(30, 33, 48, 0.8)', 
        )
        
        st.plotly_chart(fig, use_container_width=True)

# === TAB 3: LOGISTICS & TRANSPORTATION ===
with tab3:
    # Transportation overview
    st.markdown("<div class='section-header'>Transportation Mode Analysis</div>", unsafe_allow_html=True)
    
    transport_col1, transport_col2 = st.columns(2)
    
    with transport_col1:
        # Transportation Modes Distribution - Sunburst chart
        order_summary = df.groupby('Transportation modes')['Order quantities'].sum().reset_index()
        
        fig = px.sunburst(
            order_summary,
            path=['Transportation modes'],
            values='Order quantities',
            title='Order Quantities by Transportation Mode',
            color='Order quantities',
            color_continuous_scale=['#36a2eb', '#4bc0c0', '#9966ff'],
        )
        
        fig.update_layout(
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with transport_col2:
        # Transportation Modes Frequency - Pie chart with hole
        mode_counts = df['Transportation modes'].value_counts()
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=mode_counts.index,
            values=mode_counts.values,
            textinfo='percent',
            marker_colors=['#4bc0c0', '#9966ff', '#36a2eb', '#ffcd56'],
            textposition='inside',
            hole=0.6
        ))
        
        fig.update_layout(
            title='Frequency of Transportation Modes',
            annotations=[dict(text='Transport<br>Modes', x=0.5, y=0.5, font_size=15, showarrow=False, font_color='white')],
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.3,
                xanchor='center',
                x=0.5
            ),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Shipping and Lead Times Analysis
    st.markdown("<div class='section-header'>Shipping & Lead Times Analysis</div>", unsafe_allow_html=True)
    
    shipping_col1, shipping_col2 = st.columns(2)
    
    with shipping_col1:
        # Average Lead Time vs Shipping Time by Transportation Mode - Line chart
        numeric_columns = ['Shipping times', 'Lead times']
        transport_summary = df.groupby('Transportation modes')[numeric_columns].mean().reset_index()
        
        fig = px.line(transport_summary, 
                x='Shipping times', 
                y='Lead times', 
                color='Transportation modes',
                title='Lead Times vs. Shipping Times by Transport Mode',
                labels={'Shipping times': 'Shipping Times (days)', 'Lead times': 'Lead Times (days)', 'Transportation modes': 'Transportation Mode'},
                color_discrete_sequence=['#4bc0c0', '#9966ff', '#36a2eb', '#ffcd56'],
                line_shape='spline')
        
        fig.update_traces(mode='lines+markers', marker=dict(size=10))
        
        fig.update_layout(
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            xaxis_title='Shipping Times (days)',
            yaxis_title='Lead Times (days)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with shipping_col2:
        # Average Lead Time by Product Type - Bar chart with color gradient
        average_lead_time_by_product = df.groupby('Product type')['Lead times'].mean().reset_index()
        average_lead_time_by_product['Average Lead Time'] = average_lead_time_by_product['Lead times'].round(2)
        average_lead_time_by_product = average_lead_time_by_product.sort_values(by='Product type')
        
        fig = px.bar(average_lead_time_by_product, 
                x='Product type', 
                y='Average Lead Time',
                title='Average Lead Time by Product Type',
                labels={'Average Lead Time': 'Average Lead Time (days)', 'Product type': 'Product Type'},
                color='Average Lead Time',
                color_continuous_scale=['#36a2eb', '#4bc0c0', '#9966ff'],
                )
        
        fig.update_layout(
            xaxis_title="Product Type",
            yaxis_title="Average Lead Time (days)",
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            bargap=0.2,
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Shipping Costs Analysis
    st.markdown("<div class='section-header'>Shipping Cost Analysis</div>", unsafe_allow_html=True)
    
    cost_col1, cost_col2 = st.columns(2)
    
    with cost_col1:
        # Shipping Costs by Carrier - Bar chart with categories
        shipping_summary = df.groupby('Shipping carriers')['Shipping costs'].sum().reset_index()
        
        fig = px.bar(
            shipping_summary,
            x='Shipping carriers',
            y='Shipping costs',
            title='Distribution of Shipping Costs by Carrier',
            labels={'Shipping carriers': 'Shipping Carriers', 'Shipping costs': 'Shipping Costs ($)'},
            color='Shipping carriers',
            color_discrete_sequence=['#4bc0c0', '#9966ff', '#36a2eb', '#ffcd56', '#ff6384']
        )
        
        fig.update_layout(
            font=dict(size=14, color='white'),
            xaxis_title=None,
            yaxis_title='Shipping Costs ($)',
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            showlegend=False,
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with cost_col2:
        # Shipping Costs by Transportation Mode - Bar chart with consistent colors
        transportation_summary = df.groupby('Transportation modes')['Shipping costs'].sum().reset_index()
        
        fig = px.bar(transportation_summary, 
                x='Transportation modes', 
                y='Shipping costs', 
                title='Shipping Costs by Transportation Mode',
                labels={'Shipping costs': 'Shipping Costs ($)', 'Transportation modes': 'Transportation Mode'},
                color='Transportation modes',
                color_discrete_sequence=['#4bc0c0', '#9966ff', '#36a2eb', '#ffcd56'])
        
        fig.update_layout(
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            xaxis_title='Transportation Modes',
            yaxis_title='Shipping Costs ($)',
            showlegend=False,
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Location analysis
    st.markdown("<div class='section-header'>Location & Production Analysis</div>", unsafe_allow_html=True)
    
    location_col1, location_col2 = st.columns(2)
    
    with location_col1:
        # Production Volumes by Location - Treemap with modern colors
        location_summary = df.groupby('Location').agg({'Production volumes': 'sum'}).reset_index()
        location_summary = location_summary.sort_values(by='Production volumes', ascending=False)
        
        fig = px.treemap(
            location_summary,
            path=['Location'],
            values='Production volumes',
            color='Production volumes',
            color_continuous_scale=['#36a2eb', '#4bc0c0', '#9966ff', '#ffcd56'],
            title='Production Volumes by Location'
        )
        
        fig.update_layout(
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with location_col2:
        # Order Quantities by Location - Bar chart with consistent colors
        result = df.groupby('Location')['Order quantities'].sum().reset_index()
        result = result.sort_values(by='Order quantities', ascending=False)
        
        fig = px.bar(result, x='Location', y='Order quantities',
                title='Order Quantities by Location',
                labels={'Location': 'Location', 'Order quantities': 'Total Order Quantities'},
                color='Location',
                color_discrete_sequence=['#4bc0c0', '#9966ff', '#36a2eb', '#ffcd56', '#ff6384'])
        
        fig.update_layout(
            xaxis_title="Location",
            yaxis_title="Total Order Quantities",
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(30, 33, 48, 0)',
            paper_bgcolor='rgba(30, 33, 48, 0.8)',
            bargap=0.2,
            showlegend=False,
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown(
    """
    <hr>
    <div style='text-align: center; padding: 20px 0;'>
        <p style='font-size: 1.2em; font-family: "Helvetica Neue", sans-serif; color: #a3a8b8;'>
             Supply Chain Analytics Dashboard | Created with by <a href='https://github.com/rabhinav0906' target='_blank' style='color: #4bc0c0; text-decoration: none;'>Abhinav Rai</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)