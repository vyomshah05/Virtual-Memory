# Virtual Memory Manager
## How to Run

This program simulates a virtual memory system with optional demand paging.

### Command Format

`python main.py <init_file> <va_file> <output_file> <demand_paging>`

### Arguments

<init_file> — Initialization file

<va_file> — Virtual address input file

<output_file> — Output file to write results

<demand_paging> — true or false

### Example Runs
Without Demand Paging

`python main.py tests/init-no-dp.txt tests/input-no-dp.txt tests/output-no-dp.txt false`

With Demand Paging

`python main.py tests/init-dp.txt tests/input-dp.txt tests/output-dp.txt true`

## Notes

Use true to enable demand paging.

Use false to disable demand paging.

Output will be written to the specified output file.

Requires Python 3.
