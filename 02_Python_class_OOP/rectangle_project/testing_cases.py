# --length and --width: not_given, one_valid, both_valid, both_invalid
# --input:            : not_given, dir_many_json, dir_one_json, dir_no_json, json_file, other_file, not_existed
# --output:           : not_given, existed_dir, not_existed_dir, json_file, not_json_file

from itertools import product

import polars as pl

length_width = ['not_given', 'one_valid', 'both_valid', 'both_invalid']
input = ['not_given', 'dir_many_json', 'dir_one_json', 'dir_no_json', 'json_file', 'other_file', 'not_existed']
output = ['not_given', 'not_existed_dir', 'existed_dir', 'json_file', 'not_json_file']

df_testing_cases = pl.DataFrame(
    list(product(length_width, input, output)),
    schema=["Length_Width", "Input_path", "Output_path"]
)

# Show every row and every column in any subsequent print()
pl.Config.set_tbl_rows(-1)   # -1  ➜ unlimited rows
pl.Config.set_tbl_cols(-1)   # -1  ➜ unlimited columns


print(df_testing_cases)
# shape: (140, 3)
# ┌──────────────┬───────────────┬─────────────────┐
# │ Length_Width ┆ Input_path    ┆ Output_path     │   Testing command
# │ ---          ┆ ---           ┆ ---             │   (must be in 02_Python_class_OOP/rectangle_project first,
# │ str          ┆ str           ┆ str             │    use "cd 02_Python_class_OOP/rectangle_project")
# ╞══════════════╪═══════════════╪═════════════════╡
# │ not_given    ┆ not_given     ┆ not_given       │   python rectangle_module.py
# │ not_given    ┆ not_given     ┆ not_existed_dir │   python rectangle_module.py -o result_test
# │ not_given    ┆ not_given     ┆ existed_dir     │   python rectangle_module.py -o data_single
# │ not_given    ┆ not_given     ┆ json_file       │   python rectangle_module.py -o result_test.json
# │ not_given    ┆ not_given     ┆ not_json_file   │   python rectangle_module.py -o result_test.txt
# │ not_given    ┆ dir_many_json ┆ not_given       │   python rectangle_module.py -i data
# │ not_given    ┆ dir_many_json ┆ not_existed_dir │   python rectangle_module.py -i data -o ./result_test
# │ not_given    ┆ dir_many_json ┆ existed_dir     │   python rectangle_module.py -i data -o ./result_test
# │ not_given    ┆ dir_many_json ┆ json_file       │   python rectangle_module.py -i data -o ./result_file.json
# │ not_given    ┆ dir_many_json ┆ not_json_file   │   python rectangle_module.py -i data -o ./result_file.txt
# │ not_given    ┆ dir_one_json  ┆ not_given       │   python rectangle_module.py -i data_single
# │ not_given    ┆ dir_one_json  ┆ not_existed_dir │   python rectangle_module.py -i data_single -o result_test/subdir
# │ not_given    ┆ dir_one_json  ┆ existed_dir     │   python rectangle_module.py -i data_single -o result_test/subdir
# │ not_given    ┆ dir_one_json  ┆ json_file       │   python rectangle_module.py -i data_single -o result_test/subdir.json
# │ not_given    ┆ dir_one_json  ┆ not_json_file   │   python rectangle_module.py -i data_single -o result_test/subdir.txt
# │ not_given    ┆ dir_no_json   ┆ not_given       │   python rectangle_module.py -i ../
# │ not_given    ┆ dir_no_json   ┆ not_existed_dir │   python rectangle_module.py -i ../ -o ./result_test
# │ not_given    ┆ dir_no_json   ┆ existed_dir     │   python rectangle_module.py -i ../ -o ./data_single
# │ not_given    ┆ dir_no_json   ┆ json_file       │   python rectangle_module.py -i ../ -o ./result.json
# │ not_given    ┆ dir_no_json   ┆ not_json_file   │   python rectangle_module.py -i ../ -o ./result.txt
# │ not_given    ┆ json_file     ┆ not_given       │   python rectangle_module.py -i ./data_single/rectangle_single.json
# │ not_given    ┆ json_file     ┆ not_existed_dir │   python rectangle_module.py -i ./data_single/rectangle_single.json -o ./result_test
# │ not_given    ┆ json_file     ┆ existed_dir     │   python rectangle_module.py -i ./data_single/rectangle_single.json -o ./result_test
# │ not_given    ┆ json_file     ┆ json_file       │   python rectangle_module.py -i ./data_single/rectangle_single.json -o ./result_test/result_1.json
# │ not_given    ┆ json_file     ┆ not_json_file   │   python rectangle_module.py -i ./data_single/rectangle_single.json -o ./result_test/result_2.csv
# │ not_given    ┆ other_file    ┆ not_given       │   python rectangle_module.py -i ./rectangle_logs.txt
# │ not_given    ┆ other_file    ┆ not_existed_dir │   python rectangle_module.py -i ./rectangle_logs.txt -o ./result_test
# │ not_given    ┆ other_file    ┆ existed_dir     │   python rectangle_module.py -i ./rectangle_logs.txt -o ./data_single
# │ not_given    ┆ other_file    ┆ json_file       │   python rectangle_module.py -i ./rectangle_logs.txt -o ./result_test.json
# │ not_given    ┆ other_file    ┆ not_json_file   │   python rectangle_module.py -i ./rectangle_logs.txt -o ./result_test.txt
# │ not_given    ┆ not_existed   ┆ not_given       │   python rectangle_module.py -i ./abcxyz
# │ not_given    ┆ not_existed   ┆ not_existed_dir │   python rectangle_module.py -i ./abcxyz -o ./result_test
# │ not_given    ┆ not_existed   ┆ existed_dir     │   python rectangle_module.py -i ./abcxyz -o ./data_single
# │ not_given    ┆ not_existed   ┆ json_file       │   python rectangle_module.py -i ./abcxyz -o ./result_test.json
# │ not_given    ┆ not_existed   ┆ not_json_file   │   python rectangle_module.py -i ./abcxyz -o ./result_test.json
# │ one_valid    ┆ not_given     ┆ not_given       │   python rectangle_module.py -l 2 -w a
# │ one_valid    ┆ not_given     ┆ not_existed_dir │   python rectangle_module.py -l 2 -w a -o result_test
# │ one_valid    ┆ not_given     ┆ existed_dir     │   python rectangle_module.py -l 2 -w a -o data_single
# │ one_valid    ┆ not_given     ┆ json_file       │   python rectangle_module.py -l 2 -w a -o result_test.json
# │ one_valid    ┆ not_given     ┆ not_json_file   │   python rectangle_module.py -l 2 -w a -o result_test.txt
# │ one_valid    ┆ dir_many_json ┆ not_given       │   python rectangle_module.py -l a -w 2 -i ./data
# │ one_valid    ┆ dir_many_json ┆ not_existed_dir │   python rectangle_module.py -l a -w 2 -i ./data -o result_test/subdir
# │ one_valid    ┆ dir_many_json ┆ existed_dir     │   python rectangle_module.py -l a -w 2 -i ./data -o result_test/subdir
# │ one_valid    ┆ dir_many_json ┆ json_file       │   python rectangle_module.py -l a -w 2 -i ./data -o result_test/subdir.json
# │ one_valid    ┆ dir_many_json ┆ not_json_file   │   python rectangle_module.py -l a -w 2 -i ./data -o result_test/subdir.txt
# │ one_valid    ┆ dir_one_json  ┆ not_given       │   python rectangle_module.py -l 2 -w a -i ./data_single/
# │ one_valid    ┆ dir_one_json  ┆ not_existed_dir │   python rectangle_module.py -l 2 -w a -i ./data_single/ -o ./result_test
# │ one_valid    ┆ dir_one_json  ┆ existed_dir     │   python rectangle_module.py -l 2 -w a -i ./data_single/ -o ./result_test
# │ one_valid    ┆ dir_one_json  ┆ json_file       │   python rectangle_module.py -l 2 -w a -i ./data_single/ -o ./result_test.json
# │ one_valid    ┆ dir_one_json  ┆ not_json_file   │   python rectangle_module.py -l 2 -w a -i ./data_single/ -o ./result_test.txt
# │ one_valid    ┆ dir_no_json   ┆ not_given       │   python rectangle_module.py -l a -w 2 -i ../
# │ one_valid    ┆ dir_no_json   ┆ not_existed_dir │   python rectangle_module.py -l a -w 2 -i ../ -o ./result_test
# │ one_valid    ┆ dir_no_json   ┆ existed_dir     │   python rectangle_module.py -l a -w 2 -i ../ -o ./data_single
# │ one_valid    ┆ dir_no_json   ┆ json_file       │   python rectangle_module.py -l a -w 2 -i ../ -o ./result_test.json
# │ one_valid    ┆ dir_no_json   ┆ not_json_file   │   python rectangle_module.py -l a -w 2 -i ../ -o ./result_test.txt
# │ one_valid    ┆ json_file     ┆ not_given       │   python rectangle_module.py -l 2 -w a -i ./data_single/rectangle_single.json
# │ one_valid    ┆ json_file     ┆ not_existed_dir │   python rectangle_module.py -l 2 -w a -i ./data_single/rectangle_single.json -o ./result_test
# │ one_valid    ┆ json_file     ┆ existed_dir     │   python rectangle_module.py -l 2 -w a -i ./data_single/rectangle_single.json -o ./result_test
# │ one_valid    ┆ json_file     ┆ json_file       │   python rectangle_module.py -l 2 -w a -i ./data_single/rectangle_single.json -o ./result_test.json
# │ one_valid    ┆ json_file     ┆ not_json_file   │   python rectangle_module.py -l 2 -w a -i ./data_single/rectangle_single.json -o ./result_test.txt
# │ one_valid    ┆ other_file    ┆ not_given       │   python rectangle_module.py -l a -w 2 -i ./rectangle_logs.txt
# │ one_valid    ┆ other_file    ┆ not_existed_dir │   python rectangle_module.py -l a -w 2 -i ./rectangle_logs.txt -o ./result_test
# │ one_valid    ┆ other_file    ┆ existed_dir     │   python rectangle_module.py -l a -w 2 -i ./rectangle_logs.txt -o ./data_single
# │ one_valid    ┆ other_file    ┆ json_file       │   python rectangle_module.py -l a -w 2 -i ./rectangle_logs.txt -o ./result.json
# │ one_valid    ┆ other_file    ┆ not_json_file   │   python rectangle_module.py -l a -w 2 -i ./rectangle_logs.txt -o ./result.txt
# │ one_valid    ┆ not_existed   ┆ not_given       │   python rectangle_module.py -l 2 -w a -i ./abcxyz
# │ one_valid    ┆ not_existed   ┆ not_existed_dir │   python rectangle_module.py -l 2 -w a -i ./abcxyz -o ./result_test
# │ one_valid    ┆ not_existed   ┆ existed_dir     │   python rectangle_module.py -l 2 -w a -i ./abcxyz -o ./data_single
# │ one_valid    ┆ not_existed   ┆ json_file       │   python rectangle_module.py -l 2 -w a -i ./abcxyz -o ./result_test.json
# │ one_valid    ┆ not_existed   ┆ not_json_file   │   python rectangle_module.py -l 2 -w a -i ./abcxyz -o ./result_test.txt
# │ both_valid   ┆ not_given     ┆ not_given       │   python rectangle_module.py -w 23 -l 55
# │ both_valid   ┆ not_given     ┆ not_existed_dir │   python rectangle_module.py -w 23 -l 55 -o ./result_test
# │ both_valid   ┆ not_given     ┆ existed_dir     │   python rectangle_module.py -w 23 -l 55 -o ./result_test
# │ both_valid   ┆ not_given     ┆ json_file       │   python rectangle_module.py -w 23 -l 55 -o ./result_test.json
# │ both_valid   ┆ not_given     ┆ not_json_file   │   python rectangle_module.py -w 23 -l 55 -o ./result_test.json
# │ both_valid   ┆ dir_many_json ┆ not_given       │   python rectangle_module.py -w 23 -l 55 -i ./data
# │ both_valid   ┆ dir_many_json ┆ not_existed_dir │   python rectangle_module.py -w 23 -l 55 -i ./data -o ./result_test
# │ both_valid   ┆ dir_many_json ┆ existed_dir     │   python rectangle_module.py -w 23 -l 55 -i ./data -o ./result_test
# │ both_valid   ┆ dir_many_json ┆ json_file       │   python rectangle_module.py -w 23 -l 55 -i ./data -o ./result_test.json
# │ both_valid   ┆ dir_many_json ┆ not_json_file   │   python rectangle_module.py -w 23 -l 55 -i ./data -o ./result_test.txt
# │ both_valid   ┆ dir_one_json  ┆ not_given       │   python rectangle_module.py -w 23 -l 55 -i ./data_single/
# │ both_valid   ┆ dir_one_json  ┆ not_existed_dir │   python rectangle_module.py -w 23 -l 55 -i ./data_single/ -o ./result_test
# │ both_valid   ┆ dir_one_json  ┆ existed_dir     │   python rectangle_module.py -w 23 -l 55 -i ./data_single/ -o ./result_test
# │ both_valid   ┆ dir_one_json  ┆ json_file       │   python rectangle_module.py -w 23 -l 55 -i ./data_single/ -o ./result_test.json
# │ both_valid   ┆ dir_one_json  ┆ not_json_file   │   python rectangle_module.py -w 23 -l 55 -i ./data_single/ -o ./result_test.txt
# │ both_valid   ┆ dir_no_json   ┆ not_given       │   python rectangle_module.py -w 23 -l 55 -i ../
# │ both_valid   ┆ dir_no_json   ┆ not_existed_dir │   python rectangle_module.py -w 23 -l 55 -i ../ -o ./result_test
# │ both_valid   ┆ dir_no_json   ┆ existed_dir     │   python rectangle_module.py -w 23 -l 55 -i ../ -o ./result_test
# │ both_valid   ┆ dir_no_json   ┆ json_file       │   python rectangle_module.py -w 23 -l 55 -i ../ -o ./result_test.json
# │ both_valid   ┆ dir_no_json   ┆ not_json_file   │   python rectangle_module.py -w 23 -l 55 -i ../ -o ./result_test.txt
# │ both_valid   ┆ json_file     ┆ not_given       │   python rectangle_module.py -w 23 -l 55 -i ./data_single/rectangle_single.json
# │ both_valid   ┆ json_file     ┆ not_existed_dir │   python rectangle_module.py -w 23 -l 55 -i ./data_single/rectangle_single.json -o ./result_test
# │ both_valid   ┆ json_file     ┆ existed_dir     │   python rectangle_module.py -w 23 -l 55 -i ./data_single/rectangle_single.json -o ./result_test
# │ both_valid   ┆ json_file     ┆ json_file       │   python rectangle_module.py -w 23 -l 55 -i ./data_single/rectangle_single.json -o ./result_test.json
# │ both_valid   ┆ json_file     ┆ not_json_file   │   python rectangle_module.py -w 23 -l 55 -i ./data_single/rectangle_single.json -o ./result_test.txt
# │ both_valid   ┆ other_file    ┆ not_given       │   python rectangle_module.py -w 23 -l 55 -i ./rectangle_logs.txt
# │ both_valid   ┆ other_file    ┆ not_existed_dir │   python rectangle_module.py -w 23 -l 55 -i ./rectangle_logs.txt -o ./result_test
# │ both_valid   ┆ other_file    ┆ existed_dir     │   python rectangle_module.py -w 23 -l 55 -i ./rectangle_logs.txt -o ./result_test
# │ both_valid   ┆ other_file    ┆ json_file       │   python rectangle_module.py -w 23 -l 55 -i ./rectangle_logs.txt -o ./result_test.json
# │ both_valid   ┆ other_file    ┆ not_json_file   │   python rectangle_module.py -w 23 -l 55 -i ./rectangle_logs.txt -o ./result_test.txt
# │ both_valid   ┆ not_existed   ┆ not_given       │   python rectangle_module.py -w 23 -l 55 -i ./abcxyz
# │ both_valid   ┆ not_existed   ┆ not_existed_dir │   python rectangle_module.py -w 23 -l 55 -i ./abcxyz -o ./result_test
# │ both_valid   ┆ not_existed   ┆ existed_dir     │   python rectangle_module.py -w 23 -l 55 -i ./abcxyz -o ./result_test
# │ both_valid   ┆ not_existed   ┆ json_file       │   python rectangle_module.py -w 23 -l 55 -i ./abcxyz -o ./result_test.json
# │ both_valid   ┆ not_existed   ┆ not_json_file   │   python rectangle_module.py -w 23 -l 55 -i ./abcxyz -o ./result_test.txt
# │ both_invalid ┆ not_given     ┆ not_given       │   python rectangle_module.py -l a -w b
# │ both_invalid ┆ not_given     ┆ not_existed_dir │   python rectangle_module.py -l a -w b -o ./result_test
# │ both_invalid ┆ not_given     ┆ existed_dir     │   python rectangle_module.py -l a -w b -o ./data_single
# │ both_invalid ┆ not_given     ┆ json_file       │   python rectangle_module.py -l a -w b -o ./result_test.json
# │ both_invalid ┆ not_given     ┆ not_json_file   │   python rectangle_module.py -l a -w b -o ./result_test.txt
# │ both_invalid ┆ dir_many_json ┆ not_given       │   python rectangle_module.py -l a -w b -i ./data
# │ both_invalid ┆ dir_many_json ┆ not_existed_dir │   python rectangle_module.py -l a -w b -i ./data -o ./result_test
# │ both_invalid ┆ dir_many_json ┆ existed_dir     │   python rectangle_module.py -l a -w b -i ./data -o ./result_test
# │ both_invalid ┆ dir_many_json ┆ json_file       │   python rectangle_module.py -l a -w b -i ./data -o ./result_test.json
# │ both_invalid ┆ dir_many_json ┆ not_json_file   │   python rectangle_module.py -l a -w b -i ./data -o ./result_test.txt
# │ both_invalid ┆ dir_one_json  ┆ not_given       │   python rectangle_module.py -l a -w b -i ./data_single
# │ both_invalid ┆ dir_one_json  ┆ not_existed_dir │   python rectangle_module.py -l a -w b -i ./data_single -o ./result_test
# │ both_invalid ┆ dir_one_json  ┆ existed_dir     │   python rectangle_module.py -l a -w b -i ./data_single -o ./result_test
# │ both_invalid ┆ dir_one_json  ┆ json_file       │   python rectangle_module.py -l a -w b -i ./data_single -o ./result_test.json
# │ both_invalid ┆ dir_one_json  ┆ not_json_file   │   python rectangle_module.py -l a -w b -i ./data_single -o ./result_test.txt
# │ both_invalid ┆ dir_no_json   ┆ not_given       │   python rectangle_module.py -l a -w b -i ../
# │ both_invalid ┆ dir_no_json   ┆ not_existed_dir │   python rectangle_module.py -l a -w b -i ../ -o ./result_test
# │ both_invalid ┆ dir_no_json   ┆ existed_dir     │   python rectangle_module.py -l a -w b -i ../ -o ./data_single
# │ both_invalid ┆ dir_no_json   ┆ json_file       │   python rectangle_module.py -l a -w b -i ../ -o ./result_test.json
# │ both_invalid ┆ dir_no_json   ┆ not_json_file   │   python rectangle_module.py -l a -w b -i ../ -o ./result_test.txt
# │ both_invalid ┆ json_file     ┆ not_given       │   python rectangle_module.py -l a -w b -i ./data_single/rectangle_single.json
# │ both_invalid ┆ json_file     ┆ not_existed_dir │   python rectangle_module.py -l a -w b -i ./data_single/rectangle_single.json -o ./result_test
# │ both_invalid ┆ json_file     ┆ existed_dir     │   python rectangle_module.py -l a -w b -i ./data_single/rectangle_single.json -o ./result_test
# │ both_invalid ┆ json_file     ┆ json_file       │   python rectangle_module.py -l a -w b -i ./data_single/rectangle_single.json -o ./result_test.json
# │ both_invalid ┆ json_file     ┆ not_json_file   │   python rectangle_module.py -l a -w b -i ./data_single/rectangle_single.json -o ./result_test.txt
# │ both_invalid ┆ other_file    ┆ not_given       │   python rectangle_module.py -l a -w b -i ./rectangle_logs.txt
# │ both_invalid ┆ other_file    ┆ not_existed_dir │   python rectangle_module.py -l a -w b -i ./rectangle_logs.txt -o ./result_test
# │ both_invalid ┆ other_file    ┆ existed_dir     │   python rectangle_module.py -l a -w b -i ./rectangle_logs.txt -o ./data_single
# │ both_invalid ┆ other_file    ┆ json_file       │   python rectangle_module.py -l a -w b -i ./rectangle_logs.txt -o ./result_test.json
# │ both_invalid ┆ other_file    ┆ not_json_file   │   python rectangle_module.py -l a -w b -i ./rectangle_logs.txt -o ./result_test.txt
# │ both_invalid ┆ not_existed   ┆ not_given       │   python rectangle_module.py -l a -w b -i ./abcxyz
# │ both_invalid ┆ not_existed   ┆ not_existed_dir │   python rectangle_module.py -l a -w b -i ./abcxyz -o ./result_test
# │ both_invalid ┆ not_existed   ┆ existed_dir     │   python rectangle_module.py -l a -w b -i ./abcxyz -o ./data_single
# │ both_invalid ┆ not_existed   ┆ json_file       │   python rectangle_module.py -l a -w b -i ./abcxyz -o ./result_test.json
# │ both_invalid ┆ not_existed   ┆ not_json_file   │   python rectangle_module.py -l a -w b -i ./abcxyz -o ./result_test.txt
# └──────────────┴───────────────┴─────────────────┘
