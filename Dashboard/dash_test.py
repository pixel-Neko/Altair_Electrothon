import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import re  # For validating phone numbers

# Set page configuration
st.set_page_config(
    page_title="Patient Monitoring Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state for patients with expanded profile information
if 'patients' not in st.session_state:
    st.session_state.patients = [
        {
            "id": 1,
            "name": "Sarah Johnson",
            "age": 72,
            "gender": "Female",
            "room": "204B",
            "heart_rate": 82,
            "blood_pressure": "128/85",
            "temperature": 98.6,
            "last_fall": datetime.now() - timedelta(hours=2),
            "battery_status": 85,
            "connection_status": "Connected",
            "emergency_contact": "555-123-4567",
            "medical_conditions": ["Hypertension", "Osteoporosis"],
            "medications": ["Lisinopril 10mg", "Calcium 500mg", "Vitamin D"],
            "address": "123 Main St, Apt 4B, Springfield, IL 62704",
            "device_id": "WD-72859",
            "alerts": [
                {"type": "Fall", "time": datetime.now() - timedelta(hours=2), "read": False},
                {"type": "Low Battery", "time": datetime.now() - timedelta(days=1), "read": True}
            ]
        },
        {
            "id": 2,
            "name": "Robert Chen",
            "age": 68,
            "gender": "Male",
            "room": "115A",
            "heart_rate": 74,
            "blood_pressure": "135/80",
            "temperature": 99.1,
            "last_fall": None,
            "battery_status": 23,
            "connection_status": "Disconnected",
            "emergency_contact": "555-987-6543",
            "medical_conditions": ["Type 2 Diabetes", "COPD"],
            "medications": ["Metformin 500mg", "Albuterol"],
            "address": "456 Oak Ave, Springfield, IL 62701",
            "device_id": "WD-63421",
            "alerts": [
                {"type": "Battery Critical", "time": datetime.now() - timedelta(minutes=10), "read": False},
                {"type": "Connection Lost", "time": datetime.now() - timedelta(minutes=10), "read": False}
            ]
        }
    ]

# Initialize selected patient if not already set
if 'selected_patient_index' not in st.session_state:
    st.session_state.selected_patient_index = 0

# Initialize view state
if 'current_view' not in st.session_state:
    st.session_state.current_view = "dashboard"  # Options: "dashboard", "profile"

# Function to format time difference
def format_time_diff(time_value):
    if time_value is None:
        return "None"
    
    now = datetime.now()
    diff = now - time_value
    
    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds // 3600 > 0:
        return f"{diff.seconds // 3600} hours ago"
    elif diff.seconds // 60 > 0:
        return f"{diff.seconds // 60} minutes ago"
    else:
        return "Just now"

# Function to add a new patient with all profile fields
def add_new_patient(name, age, gender, room, emergency_contact, medical_conditions, medications, address, device_id):
    if name and age:  # Basic validation
        new_id = max([p["id"] for p in st.session_state.patients]) + 1 if st.session_state.patients else 1
        
        # Convert string lists to actual lists
        if isinstance(medical_conditions, str):
            medical_conditions = [item.strip() for item in medical_conditions.split(',') if item.strip()]
        if isinstance(medications, str):
            medications = [item.strip() for item in medications.split(',') if item.strip()]
            
        new_patient = {
            "id": new_id,
            "name": name,
            "age": int(age),
            "gender": gender,
            "room": room,
            "heart_rate": 75,
            "blood_pressure": "120/80",
            "temperature": 98.6,
            "last_fall": None,
            "battery_status": 100,
            "connection_status": "Connected",
            "emergency_contact": emergency_contact,
            "medical_conditions": medical_conditions,
            "medications": medications,
            "address": address,
            "device_id": device_id,
            "alerts": []
        }
        st.session_state.patients.append(new_patient)
        return True
    return False

# Function to update patient profile
def update_patient_profile(patient_index, name, age, gender, room, emergency_contact, medical_conditions, medications, address, device_id):
    if name and age:  # Basic validation
        patient = st.session_state.patients[patient_index]
        
        # Convert string lists to actual lists
        if isinstance(medical_conditions, str):
            medical_conditions = [item.strip() for item in medical_conditions.split(',') if item.strip()]
        if isinstance(medications, str):
            medications = [item.strip() for item in medications.split(',') if item.strip()]
        
        # Update the patient information
        patient["name"] = name
        patient["age"] = int(age)
        patient["gender"] = gender
        patient["room"] = room
        patient["emergency_contact"] = emergency_contact
        patient["medical_conditions"] = medical_conditions
        patient["medications"] = medications
        patient["address"] = address
        patient["device_id"] = device_id
        
        # Update the patient in the session state
        st.session_state.patients[patient_index] = patient
        return True
    return False

# Function to mark alert as read
def mark_alert_as_read(patient_index, alert_index):
    st.session_state.patients[patient_index]["alerts"][alert_index]["read"] = True

# Function to validate phone number
def is_valid_phone(phone):
    # Simple pattern matching for US phone numbers
    pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$|^\(\d{3}\)\s*\d{3}-\d{4}$|^\d{10}$')
    return bool(pattern.match(phone) if phone else True)  # True if empty

# Header
st.title("🏥 Patient Monitoring Dashboard")

# Navigation
nav_col1, nav_col2 = st.columns([3, 1])
with nav_col1:
    st.write("")  # Empty space for alignment
with nav_col2:
    if st.session_state.current_view == "dashboard":
        if st.button("📝 Edit Patient Profile", use_container_width=True):
            st.session_state.current_view = "profile"
    else:
        if st.button("📊 Return to Dashboard", use_container_width=True):
            st.session_state.current_view = "dashboard"

# Create layout with columns for both views
left_col, right_col = st.columns([1, 3])

# Patient sidebar (left column) - Common to both views
with left_col:
    st.subheader("Patients")
    
    # Add new patient button
    if st.button("➕ Add New Patient", use_container_width=True):
        st.session_state.current_view = "profile"
        st.session_state.is_new_patient = True
        # Create a temporary empty slot at the end
        temp_index = len(st.session_state.patients)
        st.session_state.selected_patient_index = temp_index
        st.rerun()
    
    # Patient selection
    for i, patient in enumerate(st.session_state.patients):
        # Count unread alerts
        unread_alerts = sum(1 for alert in patient["alerts"] if not alert["read"])
        alert_indicator = f" 🔴 ({unread_alerts})" if unread_alerts > 0 else ""
        
        # Patient button with alert indicator
        if st.button(f"{patient['name']} - Room {patient['room']}{alert_indicator}", key=f"patient_{i}", 
                    use_container_width=True,
                    type="primary" if i == st.session_state.selected_patient_index else "secondary"):
            st.session_state.selected_patient_index = i
            st.session_state.is_new_patient = False
            st.rerun()

# Main content area (right column)
with right_col:
    # Handle new patient case
    is_new_patient = getattr(st.session_state, 'is_new_patient', False)
    
    # Make sure selected_patient_index is valid
    if is_new_patient:
        current_patient = {
            "id": len(st.session_state.patients) + 1,
            "name": "",
            "age": 0,
            "gender": "Other",
            "room": "",
            "heart_rate": 75,
            "blood_pressure": "120/80",
            "temperature": 98.6,
            "last_fall": None,
            "battery_status": 100,
            "connection_status": "Connected",
            "emergency_contact": "",
            "medical_conditions": [],
            "medications": [],
            "address": "",
            "device_id": "",
            "alerts": []
        }
    else:
        if st.session_state.selected_patient_index >= len(st.session_state.patients):
            st.session_state.selected_patient_index = 0
        current_patient = st.session_state.patients[st.session_state.selected_patient_index]

    # PROFILE VIEW
    if st.session_state.current_view == "profile":
        st.header("📋 Patient Profile Setup" + (" (New Patient)" if is_new_patient else ""))
        
        # Create the profile form
        with st.form("patient_profile_form"):
            # Basic Information Section
            st.subheader("Basic Information")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                name = st.text_input("Full Name*", value=current_patient["name"])
            with col2:
                age = st.number_input("Age*", min_value=1, max_value=120, value=current_patient["age"] if current_patient["age"] > 0 else 65)
            with col3:
                gender = st.selectbox("Gender", 
                                    options=["Male", "Female", "Other", "Prefer not to say"],
                                    index=["Male", "Female", "Other", "Prefer not to say"].index(current_patient["gender"]) if current_patient["gender"] in ["Male", "Female", "Other", "Prefer not to say"] else 2)
            
            room = st.text_input("Room Number", value=current_patient["room"])
            
            # Contact Information Section
            st.subheader("Contact Information")
            emergency_contact = st.text_input("Emergency Contact (Phone Number)*", 
                                            value=current_patient["emergency_contact"],
                                            help="Format: 555-123-4567")
            
            address = st.text_area("Address", 
                                value=current_patient["address"],
                                help="Full address including street, city, state, and zip code",
                                height=100)
                        
            # Medical Information Section
            st.subheader("Medical Information")
            
            # Convert list to string for text input if needed
            medical_conditions_str = ", ".join(current_patient["medical_conditions"]) if isinstance(current_patient["medical_conditions"], list) else current_patient["medical_conditions"] or ""
            medications_str = ", ".join(current_patient["medications"]) if isinstance(current_patient["medications"], list) else current_patient["medications"] or ""
            
            medical_conditions = st.text_area("Medical Conditions*", 
                                            value=medical_conditions_str,
                                            help="Enter medical conditions separated by commas (e.g., Diabetes, Hypertension)",
                                            height=100)
            
            medications = st.text_area("Medications", 
                                    value=medications_str,
                                    help="Enter medications separated by commas (e.g., Metformin 500mg, Lisinopril 10mg)",
                                    height=100)
            
            # Device Information Section
            st.subheader("Wearable Device Information")
            device_id = st.text_input("Wearable Device ID*", 
                                    value=current_patient["device_id"],
                                    help="Enter the unique ID of the patient's wearable device")
            
            # Form submission
            submit_button = st.form_submit_button("Save Profile")
            
            if submit_button:
                # Validate inputs
                if not name or not age:
                    st.error("Name and Age are required fields.")
                elif not is_valid_phone(emergency_contact):
                    st.error("Please enter a valid phone number (e.g., 555-123-4567).")
                elif not medical_conditions:
                    st.error("Please enter at least one medical condition.")
                elif not device_id:
                    st.error("Wearable Device ID is required.")
                else:
                    # Save the profile
                    if is_new_patient:
                        if add_new_patient(name, age, gender, room, emergency_contact, medical_conditions, medications, address, device_id):
                            st.success("New patient profile created successfully!")
                            st.session_state.is_new_patient = False
                            st.session_state.selected_patient_index = len(st.session_state.patients) - 1
                            st.session_state.current_view = "dashboard"
                            time.sleep(1)
                            st.rerun()
                    else:
                        if update_patient_profile(st.session_state.selected_patient_index, name, age, gender, room, emergency_contact, medical_conditions, medications, address, device_id):
                            st.success("Patient profile updated successfully!")
                            st.session_state.current_view = "dashboard"
                            time.sleep(1)
                            st.rerun()

    # DASHBOARD VIEW
    else:  # st.session_state.current_view == "dashboard"
        # Patient info header
        st.header(f"Patient: {current_patient['name']}")
        
        # Quick info row
        info_col1, info_col2, info_col3, info_col4 = st.columns(4)
        with info_col1:
            st.metric("Age", current_patient["age"])
        with info_col2:
            st.metric("Gender", current_patient["gender"])
        with info_col3:
            st.metric("Room", current_patient["room"])
        with info_col4:
            # Format last fall time
            last_fall_text = format_time_diff(current_patient["last_fall"])
            if current_patient["last_fall"] is not None:
                st.metric("Last Fall", last_fall_text, delta="Alert", delta_color="inverse")
            else:
                st.metric("Last Fall", "None")
        
        # Quick Alert Section
        st.subheader("⚠️ Quick Alerts")
        alert_col1, alert_col2, alert_col3 = st.columns(3)
        
        with alert_col1:
            # Battery status with color coding
            battery_status = current_patient["battery_status"]
            battery_color = "green"
            if battery_status <= 20:
                battery_color = "red"
            elif battery_status <= 50:
                battery_color = "orange"
                
            st.markdown(f"""
            <div style="border:1px solid #ddd; padding:10px; border-radius:5px;">
                <h4>Battery Status</h4>
                <div style="display:flex; align-items:center;">
                    <div style="width:70%; background-color:#eee; height:20px; border-radius:10px; margin-right:10px;">
                        <div style="width:{battery_status}%; background-color:{battery_color}; height:20px; border-radius:10px;"></div>
                    </div>
                    <span>{battery_status}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with alert_col2:
            # Connection status
            connection_status = current_patient["connection_status"]
            status_color = "green" if connection_status == "Connected" else "red"
            status_icon = "✅" if connection_status == "Connected" else "❌"
            
            st.markdown(f"""
            <div style="border:1px solid #ddd; padding:10px; border-radius:5px;">
                <h4>Connection Status</h4>
                <div style="display:flex; align-items:center;">
                    <span style="color:{status_color}; font-size:1.5em; margin-right:10px;">{status_icon}</span>
                    <span style="color:{status_color}; font-weight:bold;">{connection_status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with alert_col3:
            # Recent alerts count
            unread_alerts = sum(1 for alert in current_patient["alerts"] if not alert["read"])
            alert_color = "red" if unread_alerts > 0 else "green"
            alert_text = f"{unread_alerts} unread" if unread_alerts > 0 else "No unread alerts"
            
            st.markdown(f"""
            <div style="border:1px solid #ddd; padding:10px; border-radius:5px;">
                <h4>Alerts</h4>
                <div style="display:flex; align-items:center;">
                    <span style="color:{alert_color}; font-size:1.5em; margin-right:10px;">{'🔔' if unread_alerts > 0 else '✓'}</span>
                    <span style="color:{alert_color}; font-weight:bold;">{alert_text}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Patient Profile Summary
        st.subheader("👤 Patient Profile Summary")
        
        profile_col1, profile_col2 = st.columns(2)
        
        with profile_col1:
            st.markdown("**Emergency Contact:** " + current_patient["emergency_contact"])
            st.markdown("**Device ID:** " + current_patient["device_id"])
            
            # Address with expandable section
            with st.expander("View Address"):
                st.write(current_patient["address"] if current_patient["address"] else "No address provided")
        
        with profile_col2:
            # Medical conditions with expandable section
            with st.expander("Medical Conditions"):
                if current_patient["medical_conditions"]:
                    for condition in current_patient["medical_conditions"]:
                        st.markdown(f"• {condition}")
                else:
                    st.write("No medical conditions recorded")
            
            # Medications with expandable section
            with st.expander("Medications"):
                if current_patient["medications"]:
                    for medication in current_patient["medications"]:
                        st.markdown(f"• {medication}")
                else:
                    st.write("No medications recorded")
        
        # Status Overview Section
        st.subheader("📊 Patient Status Overview")
        
        # Vitals in 3 columns
        vital_col1, vital_col2, vital_col3 = st.columns(3)
        
        with vital_col1:
            # Heart rate with gauge
            heart_rate = current_patient["heart_rate"]
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=heart_rate,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Heart Rate (BPM)"},
                gauge={
                    'axis': {'range': [None, 150]},
                    'bar': {'color': "red"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightgray"},
                        {'range': [60, 100], 'color': "lightgreen"},
                        {'range': [100, 150], 'color': "lightyellow"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': heart_rate
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
        with vital_col2:
            # Blood pressure
            bp_parts = current_patient["blood_pressure"].split('/')
            systolic, diastolic = int(bp_parts[0]), int(bp_parts[1])
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['Systolic', 'Diastolic'],
                y=[systolic, diastolic],
                text=[systolic, diastolic],
                textposition='auto',
                marker_color=['royalblue', 'lightblue']
            ))
            
            fig.update_layout(
                title_text='Blood Pressure (mmHg)',
                height=200,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with vital_col3:
            # Temperature
            temp = current_patient["temperature"]
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=temp,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Temperature (°F)"},
                delta={'reference': 98.6, 'position': "bottom"},
                gauge={
                    'axis': {'range': [97, 103]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [97, 99], 'color': "lightcyan"},
                        {'range': [99, 100.5], 'color': "lightyellow"},
                        {'range': [100.5, 103], 'color': "salmon"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': temp
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        # Alerts Section
        st.subheader("🚨 Alerts")
        
        if not current_patient["alerts"]:
            st.info("No alerts for this patient")
        else:
            # Create a DataFrame for the alerts
            alert_data = []
            for i, alert in enumerate(current_patient["alerts"]):
                alert_data.append({
                    "Alert Type": alert["type"],
                    "Time": format_time_diff(alert["time"]),
                    "Status": "Read" if alert["read"] else "Unread",
                    "index": i  # Store the index for the mark as read function
                })
            
            alert_df = pd.DataFrame(alert_data)
            
            # Display alerts with mark as read button
            for i, row in alert_df.iterrows():
                alert_status = "🔴 Unread" if row["Status"] == "Unread" else "✅ Read"
                with st.expander(f"{row['Alert Type']} - {row['Time']} - {alert_status}"):
                    st.write(f"Alert: {row['Alert Type']}")
                    st.write(f"Time: {row['Time']}")
                    st.write(f"Status: {row['Status']}")
                    
                    if row["Status"] == "Unread":
                        if st.button("Mark as Read", key=f"mark_read_{i}"):
                            mark_alert_as_read(st.session_state.selected_patient_index, row["index"])
                            st.success("Marked as read!")
                            time.sleep(1)
                            st.rerun()
        
        # Mock vitals history chart
        st.subheader("📈 Vitals History (Last 24 Hours)")
        
        # Generate mock data for demonstration
        hours = list(range(24, 0, -1))
        heart_rates = [current_patient["heart_rate"] + np.random.randint(-10, 10) for _ in range(24)]
        
        # Ensure values are within reasonable range
        heart_rates = [max(60, min(hr, 100)) for hr in heart_rates]
        
        # Create DataFrame for the chart
        history_data = pd.DataFrame({
            "Hours Ago": hours,
            "Heart Rate": heart_rates
        })
        
        # Plot the data
        fig = px.line(history_data, x="Hours Ago", y="Heart Rate", 
                     title="Heart Rate Trend",
                     markers=True)
        
        fig.update_layout(xaxis_title="Hours Ago", yaxis_title="Heart Rate (BPM)")
        st.plotly_chart(fig, use_container_width=True)

# Add a footer
st.markdown("---")
st.markdown("© 2025 Patient Monitoring System | Refreshes automatically")

# Simulation controls in sidebar
st.sidebar.title("Simulation Controls")
if st.sidebar.button("Simulate Alert"):
    if not is_new_patient and st.session_state.selected_patient_index < len(st.session_state.patients):
        patient_index = st.session_state.selected_patient_index
        new_alert = {
            "type": "Simulated Alert",
            "time": datetime.now(),
            "read": False
        }
        st.session_state.patients[patient_index]["alerts"].insert(0, new_alert)
        st.sidebar.success("New alert generated!")
        time.sleep(1)
        st.rerun()