# UVM Environment Generator

A small Python script that generates a complete UVM testbench skeleton from a single input: the project name.

## What it does

`gen_uvm.py` asks for a project name, then creates a folder `<name>_uvm` containing every file of a standard UVM environment, with all class, file, and interface names prefixed by the project name.

For example, entering `alu` produces `alu_driver`, `alu_monitor`, `alu_env`, `alu_if`, and so on.

## Requirements

- Python 3 (no extra libraries, only the built-in `os` module is used)

## Usage

1. Open a terminal in the folder that contains `gen_uvm.py`.
2. Run:

   ```
   python gen_uvm.py
   ```

   On Windows, use `py gen_uvm.py` if `python` is not recognized.
3. Type the project name when prompted:

   ```
   Enter the project name: alu
   ```
4. The generated files appear in `alu_uvm/`.

## Generated files

For a project named `<name>`:

| File | Purpose |
|------|---------|
| `<name>_seq_item.sv` | Sequence item (transaction) |
| `<name>_sequence.sv` | Sequence that generates transactions |
| `<name>_sequencer.sv` | Sequencer |
| `<name>_driver.sv` | Driver, drives the interface |
| `<name>_monitor.sv` | Monitor, samples the interface and broadcasts transactions |
| `<name>_coverage.sv` | Functional coverage collector |
| `<name>_scoreboard.sv` | Scoreboard, checks results |
| `<name>_agent.sv` | Agent (driver + sequencer + monitor) |
| `<name>_env.sv` | Environment (agent + scoreboard + coverage) |
| `<name>_test.sv` | Test, runs the sequence |
| `<name>_if.sv` | Interface with clock and DUT modport |
| `<name>_pkg.sv` | Package that includes all the classes |
| `<name>_tb_top.sv` | Top module: clock, interface, DUT, `run_test` |

## Testbench structure

```
tb_top
 └── <name>_test
      └── <name>_env
           ├── <name>_agent
           │    ├── <name>_sequencer
           │    ├── <name>_driver
           │    └── <name>_monitor ──┬──> <name>_scoreboard
           │                         └──> <name>_coverage
           └── (sequence <name>_sequence runs on the sequencer)
```

## What you still need to fill in

The generated code is a skeleton. After generating, complete these parts:

- **Sequence item:** add your randomizable fields and update `convert2string`.
- **Interface:** declare the signals and fill in the `dut` modport.
- **Driver:** drive the interface signals inside `run_phase`.
- **Monitor:** sample the interface, fill a transaction, and call `mon_ap.write(trn)`.
- **Scoreboard:** compare against your reference model and update `pass_count` / `error_count`.
- **Coverage:** add coverpoints to the covergroup.
- **Top module:** instantiate your DUT, connect it to the interface, and add the reset.

## Compile order

Compile the interface and package before the top module:

```
<name>_if.sv
<name>_pkg.sv
<name>_tb_top.sv
```

The other files are pulled in by the package through `` `include ``, so they do not need to be compiled separately. Use `+UVM_TESTNAME=<name>_test` to select the test if needed.

## How it works

Each file is stored in `gen_uvm.py` as a template string where `@@` marks the project name. The script replaces `@@` with the name you enter, in both the file names and the file contents, then writes the files into the output folder.

To change the generated code, edit the templates in `gen_uvm.py`. To add a new file, add a template and a new entry in the `files` dictionary.
