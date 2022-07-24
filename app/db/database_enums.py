from enum import Enum

class VoucherStatus(Enum):
    RESERVED = 1
    FINAL = 2
    COMPLETED = 3
    CANCELLED = 4

class VendorStatus(Enum):
    NEW = 1
    DRAFT = 2
    ACTIVE = 3
    INACTIVE = 4
    SUSPENDED = 5

class TenderCommitteeStatus(Enum):
    APPROVAL_1 = 1
    APPROVAL_2 = 2
    COMPLETED = 3
    CANCELLED = 4

class PQTransactionStatus(Enum):
    SUBMIT = 1
    CANCELLED = 2
    REQUEST_REVIEW = 3
    BUDGET_OWNER_APPROVAL = 4
    PREPARE_RFQ = 5
    FINALIZE_QUOTATION = 6
    SET_DOA_AND_UPDATE_PRICE = 7
    RFQ_APPROVAL = 8
    DOA_APPROVAL = 9
