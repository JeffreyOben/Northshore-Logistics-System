# Northshore Logistics System

A database-driven logistics management system developed for **Northshore Logistics Ltd** as part of the CPS4004 Database Systems assessment. The system uses **Python**, **Tkinter**, and **SQLite** to centralise logistics operations including shipment tracking, inventory control, fleet management, facility records, user access control, reporting, analytics, and security auditing.

---

## Project Overview

Northshore Logistics Ltd operates across warehouses and delivery hubs, managing shipments, drivers, vehicles, inventory, and customer delivery information. The purpose of this system is to replace paper-based logs, disconnected spreadsheets, and manual processes with a centralised database application.

The application provides a secure and user-friendly interface for managing operational data while improving visibility, reducing data entry errors, and supporting management decision-making through reports and analytics.

---

## Key Features

### Authentication and User Access

- User login system
- Account creation/sign-up
- Password hashing for secure authentication
- Role-based access control
- Supported roles: Admin, Manager, Staff, Driver

### Dashboard

- Professional sidebar navigation
- Live operational metric cards
- Total shipments overview
- Pending delivery count
- Low stock alerts
- Available fleet count
- Analytics charts
- Activity stream based on audit logs
- Automatic dashboard refresh

### Shipment Hub

- Add, update, delete, search, and view shipment records
- Track order number, sender, receiver, address, assigned driver, route, costs, surcharge, and payment status
- Supports delivery status monitoring
- Sensitive receiver address data is encrypted

### Inventory Control

- Add, update, delete, search, and view inventory records
- Track warehouse ID, item name, stock quantity, reorder level, and location
- Low stock warning logic
- Supports stock monitoring across facilities

### Fleet Management

- Vehicle management
- Driver management
- Vehicle availability tracking
- Driver shift and route history tracking
- Supports operational planning and delivery coordination

### Facility Control

- Manage warehouse and hub records
- Add and view facility information
- Supports multi-location logistics operations

### Operational Reports

- Generate shipment reports
- Generate inventory reports
- Generate vehicle reports
- Generate driver reports
- Generate full system summary reports
- Export reports as CSV
- Export reports as PDF

### User Registry

- View registered users
- Manage user roles
- Promote users to manager
- Reset users to staff role

### Security Audit

- Logs user activity
- Tracks login events
- Stores username, action, and timestamp
- Supports accountability and system monitoring

---

## Technologies Used

- Python 3
- Tkinter for graphical user interface
- SQLite for local database storage
- Git and GitHub for version control
- Hashing for password security
- Basic encryption for sensitive data fields

---

## Project Structure

```text
Northshore_Logistics_System/
│
├── app.py
├── auth.py
├── audit.py
├── database.py
├── security.py
├── README.md
│
├── gui/
│   ├── __init__.py
│   ├── dashboard_frame.py
│   ├── login_frame.py
│   ├── shipment_frame.py
│   ├── inventory_frame.py
│   ├── vehicle_frame.py
│   ├── driver_frame.py
│   ├── reports_frame.py
│   ├── facility_frame.py
│   ├── user_registry_frame.py
│   ├── security_audit_frame.py
│   └── theme.py
│
└── northshore.db
