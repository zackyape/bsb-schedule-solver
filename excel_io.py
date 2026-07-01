"""
Excel I/O Module untuk BSB Schedule Solver V2.1.
Menangani pembacaan template Excel dan penulisan hasil solver menggunakan openpyxl.
"""

from pathlib import Path
import openpyxl

from config import HEADER_ROW_INDEX, START_COLUMN_INDEX, EMPTY_CELL_MARKER, LABELS
from models import Person, DaySchedule, Assignment, WorkbookData, SolverResult


class ExcelReader:
    """Kelas untuk membaca template Excel dan mengubahnya menjadi WorkbookData."""

    @staticmethod
    def read_template(file_path: str | Path) -> WorkbookData:
        """
        Membaca file template Excel berdasarkan struktur kolom tetap.

        Asumsi:
            - Kolom A = Nama Personel
            - Kolom B dst = Hari / Tanggal
            - Sel bernilai 'A'/'B'/'C' = Terkunci (Locked)
            - Sel bernilai '1' = Kosong dan boleh diisi Solver (Empty)

        Args:
            file_path (str | Path): Path menuju file Excel template.

        Returns:
            WorkbookData: Struktur data lengkap yang siap diproses oleh Optimizer.
        """
        # Menggunakan data_only=True agar membaca nilai akhir, bukan formula
        wb = openpyxl.load_workbook(file_path, data_only=True)
        sheet = wb.active

        people: list[Person] = []
        schedules: list[DaySchedule] = []
        assignments: list[Assignment] = []
        row_lookup: dict[str, int] = {}
        day_lookup: dict[int, int] = {}

        # 1. Membaca Header Hari (Mulai dari Kolom B ke kanan)
        col_idx = START_COLUMN_INDEX
        day_counter = 0
        while True:
            cell_value = sheet.cell(row=HEADER_ROW_INDEX, column=col_idx).value
            if cell_value is None:
                break
            
            day_str = str(cell_value).strip()
            schedules.append(DaySchedule(day_index=day_counter, date_str=day_str))
            day_lookup[col_idx] = day_counter
            col_idx += 1
            day_counter += 1

        # 2. Membaca Baris Personel dan Kondisi Awal Sel (Mulai dari Baris di bawah Header)
        row_idx = HEADER_ROW_INDEX + 1
        while True:
            person_name_cell = sheet.cell(row=row_idx, column=1).value
            if person_name_cell is None:
                break
            
            person_name = str(person_name_cell).strip()
            
            # Otomatis deteksi jika personel merupakan tim ECOM berdasarkan nama
            is_ecom = "ECOM" in person_name.upper()
            
            people.append(Person(name=person_name, is_ecom=is_ecom))
            row_lookup[person_name] = row_idx

            # Membaca isi sel untuk setiap hari pada personel tersebut
            for col_idx, day_idx in day_lookup.items():
                cell_value = sheet.cell(row=row_idx, column=col_idx).value
                val_str = str(cell_value).strip() if cell_value is not None else ""

                # Jika sel berisi A, B, atau C, tandai sebagai LOCKED
                is_locked = val_str in LABELS

                assignments.append(Assignment(
                    person_name=person_name,
                    day_index=day_idx,
                    label=val_str,
                    is_locked=is_locked
                ))

            row_idx += 1

        return WorkbookData(
            people=people,
            schedules=schedules,
            assignments=assignments,
            row_lookup=row_lookup,
            day_lookup=day_lookup
        )


class ExcelWriter:
    """Kelas untuk menulis hasil optimasi SolverResult kembali ke file Excel baru."""

    @staticmethod
    def write_schedule(
        template_path: str | Path, 
        output_path: str | Path, 
        solver_result: SolverResult, 
        data: WorkbookData
    ) -> None:
        """
        Membuat file Excel baru dari template, lalu mengisi sel bernilai '1' 
        dengan hasil optimal dari solver.

        Args:
            template_path (str | Path): Path ke file template asli.
            output_path (str | Path): Path tempat menyimpan file Excel hasil akhir.
            solver_result (SolverResult): Objek penampung hasil akhir dari CP-SAT solver.
            data (WorkbookData): Objek data workbook awal untuk kebutuhan lookup koordinat.
        """
        # Load tanpa data_only agar formula bawaan (seperti total atau statistik di template) tidak hilang
        wb = openpyxl.load_workbook(template_path)
        sheet = wb.active

        # Balik day_lookup dari {col_idx: day_idx} menjadi {day_idx: col_idx} untuk mempermudah penulisan
        inv_day_lookup = {v: k for k, v in data.day_lookup.items()}

        for person_name, days in solver_result.assignments.items():
            row_idx = data.row_lookup.get(person_name)
            if not row_idx:
                continue

            for day_idx, assigned_label in days.items():
                col_idx = inv_day_lookup.get(day_idx)
                if not col_idx:
                    continue

                # Lakukan pengecekan ganda di template asli untuk memastikan keamanan data
                current_cell_val = str(sheet.cell(row=row_idx, column=col_idx).value).strip()
                
                # Sesuai aturan SDD: Hanya mengisi sel yang bernilai "1"
                if current_cell_val == EMPTY_CELL_MARKER:
                    sheet.cell(row=row_idx, column=col_idx).value = assigned_label

        wb.save(output_path)
        
