from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class BarcodeType(str, Enum):
    EAN8 = 'ean8'
    EAN13 = 'ean13'
    UPC = 'upc'
    CODE128 = 'code128'
    QRCODE = 'qrcode'
    DATAMATRIX = 'datamatrix'
    OTHER = 'other'


@dataclass
class ItemBarcode:
    code: str
    barcode_type: BarcodeType = BarcodeType.EAN13
    is_main: bool = False
    created_at: datetime = field(default_factory=datetime.now)
