from app.db.database_enums import VoucherStatus, TenderCommitteeStatus

request_type = {
    'TC': 'Tender Committee',
    'VM': 'Vendor Management'
}

initial_role_approval = {
    'VM': 'Procurement Manager',
    'TC': 'Procurement Manager',

    'PQ': 'Procurement Officer',
    'LT': 'Procurement Officer',
    'DA': 'Procurement Officer',

    'CA': 'Procurement Officer',
    'CR': 'Procurement Officer',
    'ST': 'Procurement Officer',
    'SX': 'Procurement Officer',
}


role_checker = {
    'VM': 'Procurement Manager',
    'TC': 'Procurement Manager',
    'TC_1': 'Procurement Manager',
    'TC_2': 'Director',
}

procurement_category = ['PQ', 'LT', 'DA']
expense_category = ['CA', 'EX', 'ST', 'SX']
direct_purchase = ['PD']

status_vendor = ['Waiting Approval', 'Maker Revision', 'Completed']
status_tender = ['Approval procurement manager', 'Approval director', 'Maker Revision', 'Completed']

initial_status_vouchers = VoucherStatus.RESERVED.name
initial_status_tender_committee = TenderCommitteeStatus.APPROVAL_1.name

request_type_trans = {
    'user_memo': ['PQ', 'LT'],
    'justification_memo': ['DA'],
    'approval_options': ['PD', 'SX'],
    'invoice_details': ['PD'],
    'vendor_recommendation': ['PQ', 'LT', 'DA', 'PD'],
    'payment_information': ['EX', 'CA', 'ST', 'SX'],
    'allocation': ['PQ', 'LT', 'DA', 'PD']
}
