"""
Configuration settings for BSB Schedule Solver V2.1.
Mengatur label, nilai sel, dan penalti untuk soft constraints.
"""

# Tipe label tugas (Jaga Atas, Jaga Bawah, Jaga AA)
LABELS = ["A", "B", "C"]

# Penanda sel di Excel
EMPTY_CELL_MARKER = "1"
EXCLUDE_MARKER = ""  # Sel kosong berarti tidak jaga

# Parameter Soft Constraints (Penalty Weights)
# Sesuaikan bobot ini untuk mengatur prioritas optimizer
PENALTY_WEEKLY_C = 10         # Penalti jika C dalam seminggu tidak seimbang
PENALTY_BALANCE = 5           # Penalti jika total shift antar personel jomplang
PENALTY_SPREAD_C = 8          # Penalti jika jarak antar shift C terlalu dekat
PENALTY_PREFERRED_PATTERN = 2 # Penalti untuk pola yang kurang ideal

# Konfigurasi Excel
HEADER_ROW_INDEX = 1
START_COLUMN_INDEX = 2  # Kolom B dst untuk hari
