import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Patient Monitoring Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state for patients
if 'patients' not in st.session_state:
    st.session_state.patients = [
        {
            "id": 1,
            "name": "Sarah Johnson",
            "age": 72,
            "room": "204B",
            "heart_rate": 82,
            "blood_pressure": "128/85",
            "temperature": 98.6,
            "last_fall": datetime.now() - timedelta(hours=2),
            "battery_status": 85,
            "connection_status": "Connected",
            "alerts": [
                {"type": "Fall", "time": datetime.now() - timedelta(hours=2), "read": False},
                {"type": "Low Battery", "time": datetime.now() - timedelta(days=1), "read": True}
            ]
        },
        {
            "id": 2,
            "name": "Robert Chen",
            "age": 68,
            "room": "115A",
            "heart_rate": 74,
            "blood_pressure": "135/80",
            "temperature": 99.1,
            "last_fall": None,
            "battery_status": 23,
            "connection_status": "Disconnected",
            "alerts": [
                {"type": "Battery Critical", "time": datetime.now() - timedelta(minutes=10), "read": False},
                {"type": "Connection Lost", "time": datetime.now() - timedelta(minutes=10), "read": False}
            ]
        }
    ]

# Initialize selected patient if not already set
if 'selected_patient_index' not in st.session_state:
    st.session_state.selected_patient_index = 0

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

# Function to add a new patient
def add_new_patient(name, age, room):
    if name and age and room:
        new_id = max([p["id"] for p in st.session_state.patients]) + 1
        new_patient = {
            "id": new_id,
            "name": name,
            "age": int(age),
            "room": room,
            "heart_rate": 75,
            "blood_pressure": "120/80",
            "temperature": 98.6,
            "last_fall": None,
            "battery_status": 100,
            "connection_status": "Connected",
            "alerts": []
        }
        st.session_state.patients.append(new_patient)
        return True
    return False

# Function to mark alert as read
def mark_alert_as_read(patient_index, alert_index):
    st.session_state.patients[patient_index]["alerts"][alert_index]["read"] = True

# Header
st.title("🏥 Patient Monitoring Dashboard")

# Create layout with columns
left_col, right_col = st.columns([1, 3])

# Patient sidebar (left column)
with left_col:
    st.subheader("Patients")
    
    # Add new patient section
    with st.expander("➕ Add New Patient"):
        new_name = st.text_input("Patient Name")
        new_age = st.number_input("Age", min_value=1, max_value=120, step=1)
        new_room = st.text_input("Room Number")
        if st.button("Add Patient"):
            if add_new_patient(new_name, new_age, new_room):
                st.success("Patient added successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please fill all fields")
    
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
            st.rerun()

# Main content area (right column)
with right_col:
    # Get the selected patient
    current_patient = st.session_state.patients[st.session_state.selected_patient_index]
    
    # Patient info header
    st.header(f"Patient: {current_patient['name']}")
    
    # Quick info row
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.metric("Age", current_patient["age"])
    with info_col2:
        st.metric("Room", current_patient["room"])
    with info_col3:
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

# Simulate real-time updates (in a real app, this would be handled by backend services)
if st.sidebar.button("Simulate Alert"):
    patient_index = st.session_state.selected_patient_index
    new_alert = {
        "type": "Simulated Alert",
        "time": datetime.now(),
        "read": False
    }
    st.session_state.patients[patient_index]["alerts"].insert(0, new_alert)
    st.success("New alert generated!")
    time.sleep(1)
    st.rerun()