import streamlit as st
import html
import json
import asyncio
from typing import List, Dict, Any, Optional
import sys
import os
from dotenv import load_dotenv
# Import the GoogleSearchService
from app.services.google_search import GoogleSearchService

# Add the app directory to the path so we can import from it
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Load environment variables from .env file in the project root
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

# Verify required environment variables
required_vars = ['GOOGLE_API_KEY', 'GOOGLE_SEARCH_ENGINE_ID']
for var in required_vars:
    if not os.getenv(var):
        st.error(f"Error: {var} is not set in the .env file")
        st.stop()



# Set page config
st.set_page_config(
    page_title="Company Website Finder",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 10px 15px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        color: white;
        font-weight: bold;
        padding: 10px 24px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .result-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    .title {
        color: #1e88e5;
        margin-bottom: 5px;
    }
    .snippet {
        color: #424242;
        font-size: 0.9em;
        margin: 8px 0;
    }
    .url {
        color: #0d47a1;
        font-size: 0.8em;
        word-break: break-all;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f5f7fa 0%, #e4e8eb 100%);
    }
    
    /* Table Styles */
    .result-table {
        width: 100%;
        table-layout: fixed;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 0.9em;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        /* Ensure consistent column widths */
        border-spacing: 0;
        /* Force the table to respect column widths */
        width: 100% !important;
    }
    
    .result-table thead {
        background-color: #4f8bf9;
        color: white;
    }
    
    .result-table thead th {
        position: relative;
    }
    
    .result-table thead th,
    .result-table tbody td {
        padding: 12px 15px;
        border: 1px solid #e0e0e0;
        text-align: left;
        vertical-align: middle;
        word-wrap: break-word;
        overflow: hidden;
        text-overflow: ellipsis;
        /* Ensure consistent cell sizing */
        box-sizing: border-box;
        height: 100%;
        /* Force cells to respect width */
        width: auto !important;
        min-width: 0 !important;
        max-width: none !important;
    }
    
    .result-table th {
        font-weight: 600;
        text-align: left;
        border-bottom: 2px solid #e0e0e0;
    }
    
    .result-table tbody tr {
        border-bottom: 1px solid #e0e0e0;
        /* Ensure consistent row height */
        height: 60px;
        position: relative;
    }
    
    .result-table tbody tr:last-child {
        border-bottom: none;
    }
    
    .result-table tbody tr:nth-of-type(even) {
        background-color: #f9f9f9;
    }
    
    .result-table tbody tr:hover {
        background-color: #f1f7ff;
    }
    
    /* Column Widths - Using fixed pixel values */
    .result-table colgroup col:nth-child(1) { width: 50px; }
    .result-table colgroup col:nth-child(2) { width: 200px; }
    .result-table colgroup col:nth-child(3) { width: auto; }
    .result-table colgroup col:nth-child(4) { width: 100px; }
    
    .result-table thead th:first-child,
    .result-table tbody td:first-child {
        width: 50px !important;
        min-width: 50px !important;
        max-width: 50px !important;
        text-align: center;
    }
    
    .result-table thead th:nth-child(2),
    .result-table tbody td:nth-child(2) {
        width: 200px !important;
        min-width: 200px !important;
        max-width: 200px !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .result-table thead th:nth-child(3),
    .result-table tbody td:nth-child(3) {
        width: auto !important;
        min-width: 300px !important;
    }
    
    .result-table thead th:last-child,
    .result-table tbody td:last-child {
        width: 100px !important;
        min-width: 100px !important;
        max-width: 100px !important;
        text-align: center;
    }
    
    .url-link {
        display: inline-block;
        padding: 6px 12px;
        background-color: #4f8bf9;
        color: white !important;
        text-decoration: none;
        border-radius: 4px;
        font-size: 0.85em;
        transition: all 0.2s;
    }
    
    .url-link:hover {
        background-color: #3a7bf0;
        text-decoration: none;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)



async def search_companies(company_name: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """Search for companies using the GoogleSearchService."""
    try:
        # Initialize the search service
        search_service = GoogleSearchService()
        
        # Call the search_company method
        search_results = await search_service.search_company(company_name, num_results)
        
        # Format results to match the expected format
        results = []
        for result in search_results:
            results.append({
                'title': getattr(result, 'title', 'No title'),
                'link': getattr(result, 'link', '#'),
                'snippet': getattr(result, 'snippet', 'No description available')
            })
        return results
    except Exception as e:
        st.error(f"Error performing search: {str(e)}")
        return []

def display_search_results(company_name: str, results: List[Dict[str, Any]]):
    """Display search results in a tabbed interface."""
    if not results:
        st.warning("No results found. Please try a different search term.")
        return
    
    st.success(f"Found {len(results)} results for '{company_name}'")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📄 Results", "📊 Table View", "🔧 Raw JSON"])
    
    with tab1:
        # Display results in the first tab (card view)
        for i, result in enumerate(results, 1):
            with st.container():
                title = result.get('title', 'No title')
                snippet = result.get('snippet', 'No description available')
                url = result.get('link', '#')
                
                st.markdown(f"""
                    <div class="result-card">
                        <h4 class="title">{html.escape(title)}</h4>
                        <p class="snippet">{html.escape(snippet)}</p>
                        <a href="{html.escape(url)}" target="_blank" class="url">{html.escape(url)}</a>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Add a small gap between results
                st.write("")
    
    with tab2:
        # Display results in table format
        st.markdown("""
        <table class="result-table">
            <colgroup>
                <col style="width: 50px">
                <col style="width: 200px">
                <col style="width: auto">
                <col style="width: 100px">
            </colgroup>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Link</th>
                </tr>
            </thead>
            <tbody>
        """, unsafe_allow_html=True)
        
        for i, result in enumerate(results, 1):
            st.markdown(f"""
                <tr>
                    <td>{i}</td>
                    <td>{html.escape(result.get('title', 'No title'))}</td>
                    <td>{html.escape(result.get('snippet', 'No description'))}</td>
                    <td><a href="{result.get('link', '#')}" target="_blank" class="url-link">Open ↗</a></td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            </tbody>
        </table>
        """, unsafe_allow_html=True)
    
    with tab3:
        # Show raw JSON in the third tab
        st.json(results)

def main():
    """Main function to run the Streamlit app."""
    # Sidebar with app info
    with st.sidebar:
        st.title("🔍 Company Website Finder")
        st.markdown("""
        ### About
        This application helps you find official websites of companies using Google's Custom Search API.
        
        ### How to use
        1. Enter a company name in the search box
        2. Click 'Search' to find the official website
        3. View and visit the search results
        
        """)

    # Main content
    st.title("🌐 Company Website Finder")
    st.markdown("Find the official website of any company with a single search!")

    # Search form
    with st.form("search_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            company_name = st.text_input(
                "Company Name",
                placeholder="Enter company name (e.g., Google, Microsoft)",
                key="company_input"
            )
        
        with col2:
            st.text("\n")  # For vertical alignment
            search_button = st.form_submit_button("Search")
    
    # Handle search
    if search_button and company_name:
        with st.spinner(f"🔍 Searching for {company_name}..."):
            # Use the existing search function
            results = asyncio.run(search_companies(company_name, 5))
            display_search_results(company_name, results)
                
    elif search_button and not company_name:
        st.warning("Please enter a company name to search")

    # Add some space at the bottom
    st.markdown("""
    <div style='margin-top: 100px; text-align: center; color: #666; font-size: 0.9em;'>
        <p>@Company Website Finder v1.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
