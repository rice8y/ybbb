# YBBB

**YBBB** (**Y**u**B**a**B**a **B**enchmark)

```bash
uv tool install -e git+https://github.com/rice8y/ybbb.git
```

## Example

```bash
$ ybbb ./src/llvm_ir/yubaba       
Starting benchmark...
Testing yubaba process...
Test input: テスト
Test output:
契約書だよ。そこに名前を書きな。
フン。テストというのかい。贅沢な名だねぇ。
今からお前の名前はスだ。いいかい、スだよ。分かったら返事をするんだ、ス!!
Process test successful, starting full benchmark...
Note: This will be slow since we create a new process for each name...
Consider running with a smaller dataset first by modifying the code.
Loading dataset...
Total records: 12828
Processing: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 12828/12828 [00:24<00:00, 518.61it/s]
Successfully processed: 12828
Errors encountered: 0

--- Benchmark Result ---
Total dataset records : 12828
Processed records     : 12828
Successful renames    : 12828
Errors encountered    : 0
Total time (sec)      : 24.736
Avg time per record   : 1.928 ms
Max memory usage (MB) : 128.61
Sample renamed names  : ['大', '門', '竹', '宍', '塩', '菊', '西', '白', '赤', '南']
```