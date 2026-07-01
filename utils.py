"""
Utility functions untuk BSB Schedule Solver.
Fungsi-fungsi helper umum yang tidak memiliki dependensi kompleks.
"""

import time
from contextlib import contextmanager
from typing import Generator, Any

@contextmanager
def timer(block_name: str) -> Generator[None, None, None]:
    """
    Context manager untuk mengukur waktu eksekusi blok kode.
    
    Args:
        block_name (str): Nama proses yang sedang diukur.
    """
    start_time = time.perf_counter()
    print(f"[*] Menjalankan: {block_name}...")
    try:
        yield
    finally:
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        print(f"[✓] {block_name} selesai dalam {elapsed:.4f} detik.")

def safe_get(dictionary: dict, key: Any, default: Any = None) -> Any:
    """
    Helper aman untuk mengambil value dictionary tanpa KeyError.
    """
    return dictionary.get(key, default)
    
