Open ERP System :- Odoo 13E Version 

Installation 
============
Install the Application => Apps -> ShareVault (Technical Name: sharevault)

SV-49: New Fields in Contact object - "Opt Out" and "Source ID"    

Version - 13.0.1.0.1
=======================
Added below fields in Contacts:
Opt Out - should be a True False flag field
Source ID - Text field

Version - 13.0.1.0.2
================
New Commit add it just for Adding changes in the odoo.sh.

Version - 13.0.1.0.3 and 13.0.1.0.4 and 13.0.1.0.5
=======================
change to define Xpath for new added field because Error displayed in the odoo.sh.

Version - 13.0.1.0.6
================
[SV-53] hided fields based on company type

Version - 13.0.1.0.7
================
SV-49: Modify display name to “Email Opt Out” instead of just “Opt Out”.

Version - 13.0.1.0.8
================
Update base_automation dependency for resolve error in odoo.sh

Version - 13.0.1.0.11
================
[SV-46] Industry / Sub Industry / Accounting Industry.

Version - 13.0.1.0.13
================
SV-66: add new fields to Sharevault Module

Version - 13.0.1.0.14
================
SV-63 getting this error on the import (modified the existing fields)

Version - 13.0.1.0.15
================
SV-68 Create new Fields in Sharevault in for Companies.

Version - 13.0.1.0.16
================
moved fields from company to contacts view
new field added Zoom Company ID.

Version - 13.0.1.0.17
================
SV-63 modify the sharevault fields and added unique constrain raise for domain and company name.

Version - 13.0.1.0.18
================
SV-68 make the field “Zoom Company ID” a char field instead of an integer field

Version - 13.0.1.0.19
================
SV-75 Sharevault Smart Button: filtered the sharevault data in contact smart button.

SV-79 Update ShareVault Display Card: modified the kanban view and top header name of sharevault.

Version - 13.0.1.0.20
================
SV-75 Added smartbutton for contact type company

SV-76 Update Tab Name and display only for Individual type contacts

SV-77 Dispay Contact Type field only for Companies

Version - 13.0.1.0.21
=====================
SV-80 Company and Individual Contact Types - View Updates

Version - 13.0.1.0.22
=====================
SV-80 Change the label Contact Type to Company Type and make invisible the email and mobile for contact type company.

Version - 13.0.1.0.23
=====================
SV-80 Change the page name ShareVaults and moved the imported phone field from additional info to main screen.

Version - 13.0.1.0.24
=====================
SV-102 Company and Contact Record view changes

Version - 13.0.1.0.25
=====================
- SV-102 (Out put label hide in Company records)
- SV-102 (Account Status label hide in Individual records)

Version - 13.0.1.0.25
=====================
-SV-108: (partner_id field added in sharevault.sharevault for resolve error in dashboard.)

Version - 13.0.1.0.27
=====================
SV-140: Migrate Vendors

Version - 13.0.1.0.28
=====================
SV-132: Persona Rules Engine

Version - 13.0.1.0.31
=====================
Modify the company and owner domain in sharevault view

Version - 13.0.1.0.32
====================
SV-148: Accounting - Accounting Industry Changes

Version - 13.0.1.0.33
=====================
SV-151: Add (domain) next to Company

Version - 13.0.1.0.34 &35
=========================
SV-152: Add new sharevault Type and Parent field

Version - 13.0.1.0.36
=====================
SV-156: invoice changes and contact record change

Version - 13.0.1.0.37
=====================
SV-151: Add (domain) next to Company

Version - 13.0.1.0.38
=====================
SV-170: Change in Odoo Forms

Version - 13.0.1.0.39
=====================
SV-198: Modified ShareVault Selection fields as per value.

Version - 13.0.1.0.40
=====================
SV-172: added values in MQL Type field

Version - 13.0.1.0.41
=====================
SV-209: add timezone field to partner record