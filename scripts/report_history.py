"""Бұрынғы тәжірибе PDF-ін жаңа рәсімдеу нұсқасымен шатастырмай тексеру."""
from pathlib import Path
import hashlib
import subprocess

BASELINE='b3655fec340990bf37cdf002c7c84c817b87561a'

def historical_pdf_matches(repo:Path,name:str,expected_sha256:str)->bool:
    current=repo/'reports'/name
    if current.is_file() and hashlib.sha256(current.read_bytes()).hexdigest()==expected_sha256:
        return True
    result=subprocess.run(['git','show',BASELINE+':reports/'+name],cwd=repo,capture_output=True)
    if result.returncode:
        raise RuntimeError('Тарихи PDF Git ішінде қолжетімсіз. Толық тарихы бар көшірме қажет; тексеру өткізілген жоқ.')
    return hashlib.sha256(result.stdout).hexdigest()==expected_sha256
