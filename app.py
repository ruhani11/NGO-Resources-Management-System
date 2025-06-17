import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from db_config import get_connection

# Page configuration
st.set_page_config(
    page_title="NGO Management Hub",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #17a2b8);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #28a745, #20c997);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def init_connection():
    return get_connection()

def get_db_cursor():
    conn = init_connection()
    return conn, conn.cursor()

# Helper functions
def get_volunteer_stats():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT COUNT(*) as total, SUM(CASE WHEN Availability = 1 THEN 1 ELSE 0 END) as available FROM Volunteer")
    result = cursor.fetchone()
    cursor.close()
    total = int(result[0]) if result[0] else 0
    available = int(result[1]) if result[1] else 0
    return total, available

def get_donation_stats():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT COUNT(*) as total, SUM(Quantity) as total_items FROM Donation")
    result = cursor.fetchone()
    cursor.close()
    total = int(result[0]) if result[0] else 0
    total_items = int(result[1]) if result[1] else 0
    return total, total_items

def get_recent_donations():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT DonorName, ResourceType, Quantity, DonationDate FROM Donation ORDER BY DonationDate DESC LIMIT 5")
    result = cursor.fetchall()
    cursor.close()
    return result

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤝 NGO Volunteer & Donation Management Hub</h1>
    <p>Empowering communities through organized volunteer coordination and resource management</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation with icons
st.sidebar.markdown("## 📋 Navigation")
menu_options = {
    "🏠 Dashboard": "dashboard",
    "👥 Add Volunteer": "add_volunteer", 
    "💝 Add Donation": "add_donation",
    "📊 View Volunteers": "view_volunteers",
    "📈 View Donations": "view_donations",
    "📦 Inventory": "inventory"
}

choice = st.sidebar.selectbox("Choose an option:", list(menu_options.keys()))
selected_page = menu_options[choice]

# Dashboard
if selected_page == "dashboard":
    st.markdown("## 📊 Dashboard Overview")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    total_volunteers, available_volunteers = get_volunteer_stats()
    total_donations, total_items = get_donation_stats()
    
    with col1:
        st.metric(
            label="👥 Total Volunteers",
            value=total_volunteers,
            delta=f"{available_volunteers} available"
        )
    
    with col2:
        st.metric(
            label="💝 Total Donations",
            value=total_donations,
            delta="This month"
        )
    
    with col3:
        st.metric(
            label="📦 Items Donated",
            value=int(total_items) if total_items else 0,
            delta="All time"
        )
    
    with col4:
        availability_rate = (available_volunteers / total_volunteers * 100) if total_volunteers > 0 else 0
        st.metric(
            label="📈 Availability Rate",
            value=f"{availability_rate:.1f}%",
            delta="Active volunteers"
        )
    
    # Recent activity
    st.markdown("## 🕒 Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🆕 Latest Donations")
        recent_donations = get_recent_donations()
        if recent_donations:
            df = pd.DataFrame(recent_donations, columns=['Donor', 'Resource', 'Quantity', 'Date'])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No recent donations to display")
    
    with col2:
        st.markdown("### 📊 Donation Trends")
        conn, cursor = get_db_cursor()
        cursor.execute("""
            SELECT ResourceType, SUM(Quantity) as total 
            FROM Donation 
            GROUP BY ResourceType 
            ORDER BY total DESC 
            LIMIT 5
        """)
        trend_data = cursor.fetchall()
        cursor.close()
        
        if trend_data:
            df_trend = pd.DataFrame(trend_data, columns=['Resource Type', 'Total Quantity'])
            fig = px.pie(df_trend, values='Total Quantity', names='Resource Type', 
                        title="Top Donated Resources")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No donation data available for trends")

# Add Volunteer
elif selected_page == "add_volunteer":
    st.markdown("## 👥 Register New Volunteer")
    
    with st.form("volunteer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter volunteer's full name")
            email = st.text_input("Email Address *", placeholder="volunteer@email.com")
            phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
        
        with col2:
            skills = st.text_area("Skills & Expertise", 
                                placeholder="e.g., Teaching, Medical, IT, Event Management")
            available = st.checkbox("Currently Available for Assignments", value=True)
            emergency_contact = st.text_input("Emergency Contact", 
                                            placeholder="Name and phone number")
        
        submit_volunteer = st.form_submit_button("🎯 Register Volunteer", use_container_width=True)
        
        if submit_volunteer:
            if name and email:
                try:
                    conn, cursor = get_db_cursor()
                    cursor.execute("""
                        INSERT INTO Volunteer (Name, Email, Phone, Skills, Availability) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (name, email, phone, skills, available))
                    conn.commit()
                    cursor.close()
                    
                    st.success(f"✅ {name} has been successfully registered as a volunteer!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error registering volunteer: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all required fields (marked with *)")

# Add Donation
elif selected_page == "add_donation":
    st.markdown("## 💝 Log New Donation")
    
    with st.form("donation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            donor = st.text_input("Donor Name *", placeholder="Individual or Organization name")
            resource = st.selectbox("Resource Type *", 
                                  ["Food Items", "Clothing", "Medical Supplies", "Books", 
                                   "Electronics", "Furniture", "Toys", "Other"])
            if resource == "Other":
                resource = st.text_input("Specify Resource Type", placeholder="Enter custom resource type")
        
        with col2:
            quantity = st.number_input("Quantity *", min_value=1, value=1)
            unit = st.selectbox("Unit", ["Items", "Boxes", "Bags", "Kilograms", "Liters", "Sets"])
            notes = st.text_area("Additional Notes", 
                                placeholder="Any special instructions or conditions")
        
        submit_donation = st.form_submit_button("📦 Record Donation", use_container_width=True)
        
        if submit_donation:
            if donor and resource and quantity:
                try:
                    conn, cursor = get_db_cursor()
                    
                    # Insert donation
                    cursor.execute("""
                        INSERT INTO Donation (DonorName, ResourceType, Quantity, DonationDate) 
                        VALUES (%s, %s, %s, CURDATE())
                    """, (donor, resource, quantity))
                    
                    # Update inventory if exists
                    cursor.execute("""
                        UPDATE Inventory 
                        SET QuantityAvailable = QuantityAvailable + %s 
                        WHERE ItemName = %s
                    """, (quantity, resource))
                    
                    # If no existing inventory item, create one
                    if cursor.rowcount == 0:
                        cursor.execute("""
                            INSERT INTO Inventory (ItemName, QuantityAvailable) 
                            VALUES (%s, %s)
                        """, (resource, quantity))
                    
                    conn.commit()
                    cursor.close()
                    
                    st.success(f"✅ Donation from {donor} recorded successfully!")
                    st.info(f"📦 {quantity} {unit.lower()} of {resource} added to inventory")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error recording donation: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all required fields (marked with *)")

# View Volunteers
elif selected_page == "view_volunteers":
    st.markdown("## 👥 Volunteer Directory")
    
    try:
        conn, cursor = get_db_cursor()
        
        # First, get the column names to handle different table structures
        cursor.execute("DESCRIBE Volunteer")
        columns_info = cursor.fetchall()
        column_names = [col[0] for col in columns_info]
        
        # Determine the primary key column name
        primary_key_col = None
        if 'ID' in column_names:
            primary_key_col = 'ID'
        elif 'VolunteerID' in column_names:
            primary_key_col = 'VolunteerID'
        elif 'volunteer_id' in column_names:
            primary_key_col = 'volunteer_id'
        else:
            # Use the first column as primary key
            primary_key_col = column_names[0]
        
        cursor.execute("SELECT * FROM Volunteer ORDER BY Name")
        volunteers = cursor.fetchall()
        cursor.close()
        
        if volunteers:
            # Convert to DataFrame with proper column names
            df = pd.DataFrame(volunteers, columns=column_names)
            
            # Handle availability column mapping if it exists
            if 'Availability' in df.columns:
                df['Available'] = df['Availability'].map({1: '✅ Yes', 0: '❌ No'})
                display_columns = [col for col in df.columns if col not in [primary_key_col, 'Availability']]
            else:
                display_columns = [col for col in df.columns if col != primary_key_col]
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                if 'Available' in df.columns:
                    availability_filter = st.selectbox("Filter by Availability", 
                                                     ["All", "Available Only", "Unavailable Only"])
                else:
                    availability_filter = "All"
            with col2:
                search_term = st.text_input("Search by name or skills", placeholder="Type to search...")
            
            # Apply filters
            filtered_df = df.copy()
            if availability_filter == "Available Only" and 'Available' in df.columns:
                filtered_df = filtered_df[filtered_df['Available'] == '✅ Yes']
            elif availability_filter == "Unavailable Only" and 'Available' in df.columns:
                filtered_df = filtered_df[filtered_df['Available'] == '❌ No']
            
            if search_term:
                # Search in Name column and Skills column if they exist
                mask = pd.Series([False] * len(filtered_df))
                if 'Name' in filtered_df.columns:
                    mask |= filtered_df['Name'].str.contains(search_term, case=False, na=False)
                if 'Skills' in filtered_df.columns:
                    mask |= filtered_df['Skills'].str.contains(search_term, case=False, na=False)
                filtered_df = filtered_df[mask]
            
            st.markdown(f"**Showing {len(filtered_df)} of {len(df)} volunteers**")
            
            # Volunteer management actions
            st.markdown("### 🔧 Volunteer Management")
            
            # Delete volunteer section
            with st.expander("🗑️ Delete Volunteer", expanded=False):
                st.warning("⚠️ **Warning:** Deleting a volunteer will permanently remove all their information from the database.")
                
                # Create a dropdown with volunteer names for selection
                if 'Name' in df.columns and 'Email' in df.columns:
                    volunteer_options = [f"{row['Name']} ({row['Email']})" for _, row in df.iterrows()]
                elif 'Name' in df.columns:
                    volunteer_options = [f"{row['Name']}" for _, row in df.iterrows()]
                else:
                    volunteer_options = [f"Volunteer {row[primary_key_col]}" for _, row in df.iterrows()]
                
                volunteer_ids = df[primary_key_col].tolist()
                volunteer_names = df['Name'].tolist() if 'Name' in df.columns else [f"Volunteer {id}" for id in volunteer_ids]
                
                selected_volunteer = st.selectbox(
                    "Select volunteer to delete:",
                    ["Select a volunteer..."] + volunteer_options
                )
                
                if selected_volunteer != "Select a volunteer...":
                    selected_index = volunteer_options.index(selected_volunteer)
                    selected_id = volunteer_ids[selected_index]
                    selected_name = volunteer_names[selected_index]
                    
                    st.info(f"📋 Selected volunteer: **{selected_name}**")
                    
                    # Confirmation checkbox
                    confirm_delete = st.checkbox(f"I confirm that I want to delete {selected_name}")
                    
                    if confirm_delete:
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("🗑️ Delete Volunteer", type="primary"):
                                try:
                                    conn, cursor = get_db_cursor()
                                    cursor.execute(f"DELETE FROM Volunteer WHERE {primary_key_col} = %s", (selected_id,))
                                    conn.commit()
                                    cursor.close()
                                    
                                    st.success(f"✅ {selected_name} has been successfully deleted!")
                                    st.balloons()
                                    st.rerun()  # Refresh the page to show updated data
                                    
                                except Exception as e:
                                    st.error(f"❌ Error deleting volunteer: {str(e)}")
                        
                        with col2:
                            if st.button("❌ Cancel"):
                                st.rerun()
            
            # Update volunteer availability section (only if Availability column exists)
            if 'Available' in df.columns:
                with st.expander("✏️ Update Volunteer Availability", expanded=False):
                    st.info("💡 Quickly update volunteer availability status")
                    
                    volunteer_update_options = [f"{row['Name']} - {row['Available']}" for _, row in df.iterrows() if 'Name' in df.columns]
                    selected_volunteer_update = st.selectbox(
                        "Select volunteer to update:",
                        ["Select a volunteer..."] + volunteer_update_options,
                        key="update_volunteer"
                    )
                    
                    if selected_volunteer_update != "Select a volunteer...":
                        selected_index = volunteer_update_options.index(selected_volunteer_update)
                        selected_id = volunteer_ids[selected_index]
                        selected_name = volunteer_names[selected_index]
                        current_status = df.iloc[selected_index]['Available']
                        
                        new_status = st.radio(
                            f"Update availability for {selected_name}:",
                            ["✅ Available", "❌ Not Available"],
                            index=0 if current_status == '✅ Yes' else 1
                        )
                        
                        if st.button("💾 Update Availability"):
                            try:
                                new_availability = 1 if new_status == "✅ Available" else 0
                                availability_column = 'Availability' if 'Availability' in column_names else 'Available'
                                conn, cursor = get_db_cursor()
                                cursor.execute(f"UPDATE Volunteer SET {availability_column} = %s WHERE {primary_key_col} = %s", 
                                             (new_availability, selected_id))
                                conn.commit()
                                cursor.close()
                                
                                st.success(f"✅ {selected_name}'s availability updated to {new_status}")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Error updating volunteer: {str(e)}")
            
            # Display volunteers table
            st.markdown("### 📋 Volunteer List")
            display_df = filtered_df[display_columns] if display_columns else filtered_df
            st.dataframe(display_df, use_container_width=True)
            
            # Volunteer statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'Available' in df.columns:
                    available_count = len(df[df['Available'] == '✅ Yes'])
                    st.metric("Available Volunteers", int(available_count))
                else:
                    st.metric("Total Volunteers", int(len(df)))
            with col2:
                if 'Available' in df.columns:
                    unavailable_count = len(df[df['Available'] == '❌ No'])
                    st.metric("Unavailable Volunteers", int(unavailable_count))
                else:
                    st.metric("Active Records", int(len(filtered_df)))
            with col3:
                st.metric("Total Volunteers", int(len(df)))
            
            # Debug info (you can remove this later)
            with st.expander("🔍 Debug Info", expanded=False):
                st.write("**Table Columns:**", column_names)
                st.write("**Primary Key Column:**", primary_key_col)
                st.write("**Sample Data:**")
                st.dataframe(df.head(2))
                
        else:
            st.info("📝 No volunteers registered yet. Start by adding some volunteers!")
            
    except Exception as e:
        st.error(f"❌ Error loading volunteers: {str(e)}")
        st.write("**Error Details:**", str(e))

# View Donations
elif selected_page == "view_donations":
    st.markdown("## 📈 Donation History")
    
    try:
        conn, cursor = get_db_cursor()
        cursor.execute("SELECT * FROM Donation ORDER BY DonationDate DESC")
        donations = cursor.fetchall()
        cursor.close()
        
        if donations:
            df = pd.DataFrame(donations, columns=['ID', 'Donor', 'Resource Type', 'Quantity', 'Date'])
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Donations", int(len(df)))
            with col2:
                st.metric("Total Items", int(df['Quantity'].sum()))
            with col3:
                st.metric("Unique Donors", int(df['Donor'].nunique()))
            with col4:
                st.metric("Resource Types", int(df['Resource Type'].nunique()))
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                resource_filter = st.selectbox("Filter by Resource Type", 
                                             ["All"] + list(df['Resource Type'].unique()))
            with col2:
                donor_search = st.text_input("Search by Donor", placeholder="Type donor name...")
            with col3:
                date_range = st.date_input("Filter by Date Range", value=[], max_value=datetime.now().date())
            
            # Apply filters
            filtered_df = df.copy()
            if resource_filter != "All":
                filtered_df = filtered_df[filtered_df['Resource Type'] == resource_filter]
            if donor_search:
                filtered_df = filtered_df[filtered_df['Donor'].str.contains(donor_search, case=False)]
            if len(date_range) == 2:
                filtered_df = filtered_df[
                    (pd.to_datetime(filtered_df['Date']).dt.date >= date_range[0]) & 
                    (pd.to_datetime(filtered_df['Date']).dt.date <= date_range[1])
                ]
            
            st.markdown(f"**Showing {len(filtered_df)} of {len(df)} donations**")
            st.dataframe(filtered_df.drop('ID', axis=1), use_container_width=True)
            
            # Visualizations
            if len(filtered_df) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Donations by resource type
                    resource_counts = filtered_df.groupby('Resource Type')['Quantity'].sum().reset_index()
                    fig1 = px.bar(resource_counts, x='Resource Type', y='Quantity',
                                 title="Donations by Resource Type")
                    fig1.update_layout(height=400)
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Donations over time
                    daily_donations = filtered_df.groupby('Date')['Quantity'].sum().reset_index()
                    fig2 = px.line(daily_donations, x='Date', y='Quantity',
                                  title="Donation Trends Over Time")
                    fig2.update_layout(height=400)
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("📦 No donations recorded yet. Start by logging some donations!")
            
    except Exception as e:
        st.error(f"❌ Error loading donations: {str(e)}")

# Inventory
elif selected_page == "inventory":
    st.markdown("## 📦 Inventory Management")
    
    try:
        conn, cursor = get_db_cursor()
        cursor.execute("SELECT * FROM Inventory ORDER BY ItemName")
        inventory = cursor.fetchall()
        cursor.close()
        
        if inventory:
            df = pd.DataFrame(inventory, columns=['ID', 'Item Name', 'Quantity Available'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Items Types", int(len(df)))
            with col2:
                st.metric("Total Items in Stock", int(df['Quantity Available'].sum()))
            
            # Low stock alerts
            low_stock = df[df['Quantity Available'] < 10]
            if not low_stock.empty:
                st.warning("⚠️ Low Stock Alert!")
                st.dataframe(low_stock.drop('ID', axis=1), use_container_width=True)
            
            st.markdown("### Current Inventory")
            st.dataframe(df.drop('ID', axis=1), use_container_width=True)
            
            # Inventory chart
            fig = px.bar(df, x='Item Name', y='Quantity Available',
                        title="Current Inventory Levels")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("📦 No inventory items found. Items will appear here as donations are recorded.")
            
    except Exception as e:
        st.error(f"❌ Error loading inventory: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🤝 NGO Management Hub | Making a difference, one volunteer and donation at a time</p>
    <p>Need help? Contact your system administrator</p>
</div>
""", unsafe_allow_html=True)