#!/usr/bin/env python3
import sys
import json
import argparse
import difflib
from pathlib import Path

def check_loop(history_file, max_repeats=3, similarity_threshold=0.8):
    """
    Detecta loops/repetições em histórico de execuções.
    Retorna True se detectar loop, False caso contrário.
    """
    if not Path(history_file).exists():
        return False
    
    with open(history_file) as f:
        lines = f.readlines()
    
    if len(lines) < max_repeats:
        return False
    
    # Verifica últimas N linhas
    recent = lines[-max_repeats:]
    
    # Compara similaridade entre linhas consecutivas
    for i in range(len(recent) - 1):
        similarity = difflib.SequenceMatcher(None, recent[i], recent[i+1]).ratio()
        if similarity >= similarity_threshold:
            print(f"⚠️  LOOP DETECTADO: Similaridade {similarity:.2%} entre execuções", file=sys.stderr)
            return True
    
    return False

def main():
    parser = argparse.ArgumentParser(description="Detecta loops em histórico de execuções")
    parser.add_argument("--history", default=".ci/history.json", help="Arquivo de histórico")
    parser.add_argument("--max-repeats", type=int, default=3, help="Número de repetições antes de alertar")
    parser.add_argument("--threshold", type=float, default=0.8, help="Limiar de similaridade (0-1)")
    
    args = parser.parse_args()
    
    if check_loop(args.history, args.max_repeats, args.threshold):
        print("❌ Loop detectado! Abortando para evitar execução infinita.", file=sys.stderr)
        sys.exit(1)
    else:
        print("✅ Nenhum loop detectado.")
        sys.exit(0)

if __name__ == "__main__":
    main()
