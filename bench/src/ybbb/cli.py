import time
import subprocess
import argparse
from datasets import load_dataset, concatenate_datasets
from memory_profiler import memory_usage
from tqdm import tqdm
import signal
import os
import re

def yubaba_rename_single(cmd, name: str) -> str:
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = proc.communicate(input=name + "\n", timeout=5)
        
        if proc.returncode != 0:
            return f"Error: Process failed (exit code: {proc.returncode})"
    
        match = re.search(r'今からお前の名前は(.+?)だ。', stdout)
        if match:
            return match.group(1)
        
        lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        return lines[-1] if lines else "Error: No response"
        
    except subprocess.TimeoutExpired:
        proc.kill()
        return "Error: Process timeout"
    except Exception as e:
        return f"Error: {str(e)}"

def run_yubaba_benchmark(cmd=["./yubaba"]):
    print("Loading dataset...")
    ds = load_dataset("tarudesu/gendec-dataset", split="test")

    print(f"Total records: {len(ds)}")

    start_time = time.time()
    renamed = []
    successful_renames = 0
    errors = 0

    for record in tqdm(ds, desc="Processing", total=len(ds)):
        kanji = record.get("Kanji", "").strip()
        if kanji:
            renamed_name = yubaba_rename_single(cmd, kanji)
            if renamed_name.startswith("Error:"):
                errors += 1
                if errors > 50:
                    print(f"Too many errors ({errors}), but continuing...")
                    errors = 0
            else:
                successful_renames += 1
        else:
            renamed_name = "名無し"
            successful_renames += 1
        
        renamed.append(renamed_name)

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"Successfully processed: {successful_renames}")
    print(f"Errors encountered: {errors}")

    return {
        "count": len(renamed),
        "total_records": len(ds),
        "successful_renames": successful_renames,
        "errors": errors,
        "elapsed_time": elapsed,
        "average_time_per_record": elapsed / len(renamed) if renamed else 0,
        "sample_output": renamed[:10]
    }

def test_yubaba_process(cmd):
    print("Testing yubaba process...")
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        test_input = "テスト\n"
        stdout, stderr = proc.communicate(input=test_input, timeout=10)
        
        print(f"Test input: テスト")
        print(f"Test output:\n{stdout.strip()}")
        if stderr:
            print(f"Test stderr: {stderr.strip()}")
        
        return proc.returncode == 0
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run Yubaba benchmark")
    parser.add_argument(
        "cmd",
        nargs="+",
        help="Command to run yubaba (e.g. ./yubaba or julia yubaba.jl)"
    )
    args = parser.parse_args()

    yubaba_command = args.cmd

    print("Starting benchmark...")

    if not test_yubaba_process(yubaba_command):
        print("Yubaba process test failed. Please check your script or command.")
        exit(1)

    print("Process test successful, starting full benchmark...")
    print("Note: This will be slow since we create a new process for each name...")
    print("Consider running with a smaller dataset first by modifying the code.")

    try:
        mem_usage, result = memory_usage(
            (run_yubaba_benchmark, (yubaba_command,)),
            retval=True,
            max_usage=True,
            interval=0.1
        )

        print("\n--- Benchmark Result ---")
        print(f"Total dataset records : {result['total_records']}")
        print(f"Processed records     : {result['count']}")
        print(f"Successful renames    : {result['successful_renames']}")
        print(f"Errors encountered    : {result['errors']}")
        print(f"Total time (sec)      : {result['elapsed_time']:.3f}")
        if result['count'] > 0:
            print(f"Avg time per record   : {result['average_time_per_record']*1000:.3f} ms")
        print(f"Max memory usage (MB) : {mem_usage:.2f}")
        print(f"Sample renamed names  : {result['sample_output']}")
        
    except Exception as e:
        print(f"Benchmark failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
