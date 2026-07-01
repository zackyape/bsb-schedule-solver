"""
Main Entry Point untuk BSB Schedule Solver V2.1.
Menyatukan seluruh modul (I/O, Optimizer, Validator, Report) menjadi satu alur eksekusi.
"""

import sys
from pathlib import Path
from ortools.sat.python import cp_model

from excel_io import ExcelReader, ExcelWriter
from optimizer import ScheduleOptimizer
from validator import ScheduleValidator
from report import ReportGenerator
from utils import timer


def main() -> None:
    # Konfigurasi Path
    input_file = Path("sample/Rekap_Jaga.xlsx")
    output_file = Path("Jadwal_Final.xlsx")

    print("=" * 60)
    print(" BSB SCHEDULE SOLVER V2.1 ".center(60, "="))
    print("=" * 60)

    # Cek ketersediaan file template Excel
    if not input_file.exists():
        print(f"[!] Error: File template '{input_file}' tidak ditemukan.")
        print("    Pastikan folder 'sample/' ada dan berisi 'Rekap_Jaga.xlsx'.")
        sys.exit(1)

    try:
        # 1. Read Excel
        with timer("Membaca Template Excel"):
            workbook_data = ExcelReader.read_template(input_file)
            print(f"    -> Ditemukan {len(workbook_data.people)} personel dan {len(workbook_data.schedules)} hari.")

        # 2. Optimize
        with timer("Menjalankan CP-SAT Optimizer"):
            optimizer = ScheduleOptimizer(data=workbook_data, max_time_seconds=60.0)
            solver_result = optimizer.solve()

        # Menerjemahkan status kode solver menjadi string yang mudah dibaca
        status_name = {
            cp_model.UNKNOWN: "UNKNOWN",
            cp_model.MODEL_INVALID: "MODEL_INVALID",
            cp_model.FEASIBLE: "FEASIBLE",
            cp_model.INFEASIBLE: "INFEASIBLE",
            cp_model.OPTIMAL: "OPTIMAL"
        }.get(solver_result.status, "UNKNOWN")

        print(f"    -> Status Solver: {status_name}")
        print(f"    -> Objective Value (Total Penalti Soft Rules): {solver_result.objective_value}")

        if solver_result.status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print("[!] Jadwal gagal dibuat. Solver tidak dapat menemukan solusi yang memenuhi seluruh Hard Constraints.")
            sys.exit(1)

        # 3. Validate
        with timer("Memvalidasi Integritas Jadwal"):
            validator = ScheduleValidator(data=workbook_data)
            validation_result = validator.validate(solver_result)

            if validation_result.is_valid:
                print("    -> Validasi Sukses: 100% Jadwal mematuhi aturan (Hard Rules).")
            else:
                print("    -> [!] Peringatan: Terdapat ketidaksesuaian aturan:")
                for issue in validation_result.issues:
                    print(f"       - {issue.rule_name} | {issue.person} | Hari ke-{issue.day_index}: {issue.description}")

        # 4. Generate Report
        with timer("Membuat Laporan & Statistik"):
            ReportGenerator.generate(solver_result, validation_result, workbook_data)
            print("    -> report.txt dan statistics.xlsx berhasil dibuat.")

        # 5. Write Excel Output
        with timer("Menyimpan Jadwal Final ke Excel"):
            ExcelWriter.write_schedule(
                template_path=input_file,
                output_path=output_file,
                solver_result=solver_result,
                data=workbook_data
            )
            
        print("=" * 60)
        print(f"[✓] SUKSES! Jadwal berhasil diselesaikan dan disimpan di:\n    => {output_file.absolute()}")
        print("=" * 60)

    except Exception as e:
        print(f"\n[!] Terjadi kesalahan kritis pada sistem: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
    
