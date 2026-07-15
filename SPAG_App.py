import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="SPAG Portal", layout="wide")

# --- SIMULATED DATABASE ---
# In a real app, this connects to an SQLite or Cloud Database
if "db" not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=[
        "Status", "Name", "Age", "Profession", "Region", "Skills", "Education"
    ])

# --- NAVIGATION SIDEBAR ---
page = sidebar = st.sidebar.radio("Navigate", ["Registration Form", "Admin Dashboard"])

# ==========================================
# 1. REGISTRATION FORM
# ==========================================
if page == "Registration Form":
    st.title("SALAAM POLICE ADVOCACY GROUP (SPAG)")
    st.subheader("Official Online Registration Portal")
    
    with st.form("reg_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            status = st.radio("Application Type", ["New Applicant", "Existing Member"])
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=15, max_value=100, value=25)
            education = st.selectbox("Educational Status", ["High School", "Vocational", "College Graduate", "Post-Graduate"])
            phone = st.text_input("Contact Number")
            email = st.text_input("Email Address")
            
        with col2:
            region = st.selectbox("Region", ["Region I", "Region II", "Region III", "NCR", "BARMM", "Region XII"]) # Expand list as needed
            address = st.text_area("Complete Address")
            profession = st.text_input("Profession / Occupation")
            club = st.text_input("Club / Affiliation Belonged To")
            skills = st.text_input("Interests, Talents, & Skills (Comma separated)")
            
        st.write("---")
        st.subheader("Required Document Uploads")
        photo = st.file_uploader("Upload 2x2 Photo", type=["jpg", "png", "jpeg"])
        pnp_clearance = st.file_uploader("Upload PNP Clearance", type=["jpg", "png", "pdf"])
        
        submit = st.form_submit_button("Submit Application")
        
        if submit:
            if name and email: # Basic validation
                new_data = {
                    "Status": status, "Name": name, "Age": age, 
                    "Profession": profession, "Region": region, 
                    "Skills": skills, "Education": education
                }
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
                st.success("Application submitted successfully!")
            else:
                st.error("Please fill in required fields (Name and Email).")

# ==========================================
# 2. ADMIN DASHBOARD
# ==========================================
elif page == "Admin Dashboard":
    st.title("SPAG Admin Dashboard")
    
    # Simple Password Protection
    password = st.text_input("Enter Admin Password", type="password")
    if password == "SPAG_Admin_2026": # Change to your secure password
        st.success("Access Granted")
        
        df = st.session_state.db
        
        if df.empty:
            st.info("No registration data available yet.")
        else:
            # --- METRICS & STATS ---
            st.subheader("📊 Membership Statistics")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Applicants", len(df))
            c2.metric("New Applicants", len(df[df['Status'] == 'New Applicant']))
            c3.metric("Existing Members", len(df[df['Status'] == 'Existing Member']))
            
            # Charts
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.write("**Members by Profession**")
                prof_counts = df['Profession'].value_counts()
                st.bar_chart(prof_counts)
                
            with col_chart2:
                st.write("**Members by Region**")
                region_counts = df['Region'].value_counts()
                st.pydisplay = st.pie_chart if hasattr(st, "pie_chart") else st.bar_chart(region_counts) # Fallback visualization
            
            # --- DATA TABLE & EXPORT ---
            st.write("---")
            st.subheader("📋 Registered Members Master List")
            st.dataframe(df)
            
            # Download Data Feature
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Data as CSV (Excel Compatible)",
                data=csv,
                file_name="SPAG_Members_Export.csv",
                mime="text/csv"
            )
            st.info("💡 To print, simply use your browser's print function (Ctrl+P / Cmd+P) while viewing this dashboard.")
    elif password:
        st.error("Incorrect Password.")