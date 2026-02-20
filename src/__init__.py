"""
CRM Analytics Package
RFM ve CLTV analizi için fonksiyonlar
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Ana fonksiyonları import et
from .flo_rfm_analysis import create_rfm_segments, data_preparation
from .flo_cltv_prediction import create_cltv_prediction

__all__ = [
    'create_rfm_segments',
    'data_preparation',
    'create_cltv_prediction'
]
