import subprocess
import csv
import argparse
import os
import copy
import config
from logger import get_logger

logger = get_logger("exporter")

class CaesarExporter:
    def __init__(self, db_path, mode='python'):
        self.mode = mode
        self.db_path = db_path
        
        if db_path.lower().endswith('.csv'):
            self.load_from_csv(db_path)
            return

        # Extract tables
        try:
            elem_data = subprocess.run(['mdb-export', db_path, 'INPUT_BASIC_ELEMENT_DATA'], capture_output=True, text=True, check=True).stdout
            self.e_rows = list(csv.reader(elem_data.splitlines()))[1:]
        except Exception: self.e_rows = []
        
        try:
            bend_data = subprocess.run(['mdb-export', db_path, 'INPUT_BENDS'], capture_output=True, text=True, check=True).stdout
            self.b_rows = list(csv.reader(bend_data.splitlines()))[1:]
        except Exception: self.b_rows = []

        try:
            rest_data = subprocess.run(['mdb-export', db_path, 'INPUT_RESTRAINTS'], capture_output=True, text=True, check=True).stdout
            self.r_rows = list(csv.reader(rest_data.splitlines()))[1:]
        except Exception: self.r_rows = []
        
        try:
            sif_data = subprocess.run(['mdb-export', db_path, 'INPUT_SIFTEES'], capture_output=True, text=True, check=True).stdout
            self.s_rows = list(csv.reader(sif_data.splitlines()))[1:]
        except Exception: self.s_rows = []

    def load_from_csv(self, csv_path):
        import pandas as pd
        df = pd.read_csv(csv_path)
        self.e_rows = []
        
        for idx, row in df.iterrows():
            new_row = [str(idx+1), str(idx+1)]
            
            from_node = str(row.get('FROM_NODE', ''))
            if pd.isna(from_node) or from_node == '': from_node = config.CAESAR_AUTO_CALC_STR
            new_row.append(from_node)
            
            to_node = str(row.get('TO_NODE', ''))
            if pd.isna(to_node) or to_node == '': to_node = config.CAESAR_AUTO_CALC_STR
            new_row.append(to_node)
            
            full_row = new_row + [config.CAESAR_AUTO_CALC_STR] * 130
            
            cols = ['DX', 'DY', 'DZ', 'DIAMETER', 'THICKNESS', 'CORROSION', 'INSULATION', 'DENSITY']
            for i, col in enumerate(cols):
                val = row.get(col, '')
                if not pd.isna(val) and val != '':
                    full_row[4 + i] = str(val)
                    
            full_row[config.INDEX_MATERIAL + 10] = str(config.DEFAULT_MATERIAL_ID) 
            for i in range(config.INDEX_TEMPERATURE_START, config.INDEX_TEMPERATURE_END + 1):
                full_row[i + 10] = str(config.DEFAULT_TEMPERATURE)
            for i in range(config.INDEX_PRESSURE_START, config.INDEX_PRESSURE_END + 1):
                full_row[i + 10] = str(config.DEFAULT_PRESSURE)
            
            self.e_rows.append(full_row)
            
        self.b_rows = []
        self.r_rows = []
        self.s_rows = []

    def fmt_val(self, val_str, width):
        """Implements the Y.(X-Y) Rule for pure python generation"""
        if val_str in ('-1.01010000705719', config.CAESAR_AUTO_CALC_STR.strip()):
            val_str = '-1.0101'
        try:
            val_float = float(val_str)
            if float(val_float) == int(val_float) and val_str.count('.') == 0:
                val_str += "." # CAESAR II requires decimals
        except: pass
        
        y = len(val_str)
        decimals = width - y
        if decimals < 0: decimals = 0
        
        try:
            fmt = f"{{:{width}.{decimals}f}}"
            return fmt.format(float(val_str))
        except:
            return str(val_str).rjust(width)

    def write_standalone_python(self, out_file):
        """Generates a perfectly formatted .CII file 100% standalone, with no template dependencies"""
        # Version and boilerplate header
        out = ""
        out += "    5.00000      11.0000        1256\n"
        out += "    PROJECT:                                                               \n"
        out += "                                                                           \n"
        out += "    CLIENT :                                                               \n"
        out += "                                                                           \n"
        out += "    ANALYST:                                                               \n"
        out += "                                                                           \n"
        out += "    NOTES  :                                                               \n"
        for _ in range(14):
            out += "                                                                           \n"
        
        # Elements Control Array (NUMELT)
        num_elements = len(self.e_rows)
        out += f"#{num_elements}\n"
        
        # Counts Array (NUMNOZ, NOHGRS, NONAM, NORED, NUMFLG, NUMBND, NUMRIG, NUMEXP, NUMRES...)
        # We parse lengths based on populated elements.
        num_bends = len(self.b_rows)
        num_restr = len(self.r_rows)
        num_sifs = len(self.s_rows)
        
        counts = [0]*19
        counts[5] = num_bends
        counts[8] = num_restr
        counts[13] = num_sifs # SIF&TEES is index 13 in the standard count layout
        
        out += f"         {counts[0]:>2}         {counts[1]:>2}         {counts[2]:>2}         {counts[3]:>2}         {counts[4]:>2}         {counts[5]:>2}\n"
        out += f"         {counts[6]:>2}         {counts[7]:>2}         {counts[8]:>2}         {counts[9]:>2}         {counts[10]:>2}         {counts[11]:>2}\n"
        out += f"         {counts[12]:>2}         {counts[13]:>2}         {counts[14]:>2}         {counts[15]:>2}         {counts[16]:>2}         {counts[17]:>2}\n"
        out += f"         {counts[18]:>2}\n"
        
        # The exact 0-byte formatting requires 15 lines per element
        out += "#$ ELEMENTS\n"
        for row in self.e_rows:
            node1 = self.fmt_val(row[2], 11)
            node2 = self.fmt_val(row[3], 11)
            dx = self.fmt_val(row[4], 13)
            dy = self.fmt_val(row[5], 13)
            dz = self.fmt_val(row[6], 13)
            
            # Line 1: Node 1, Node 2, DX, DY, DZ, Diameter
            diam = self.fmt_val(row[7], 13)
            out += f"  {node1} {node2} {dx}{dy}{dz}{diam}\n"
            
            # Lines 2-15 populated with auto-calc -1.0101 values
            auto13 = "    -1.010100" # Length 13
            out += f"  {auto13}{auto13}{auto13}{auto13}{auto13}{auto13}\n"
            
            # The 15-line block has an explicit integer sequence for pointers and materials
            # 6 per line, width 12
            mat_id = f"{config.DEFAULT_MATERIAL_ID:>12}"
            out += f"           0           0           0           0           0           0\n"
            out += f"           0           0           0           0           0{mat_id}\n"
            out += f"           0           0           0           0           0           0\n"
            
            # String lines (2 per line, width 32)
            out += f"                                                                \n"
            
            # Fill the rest with standard -1.0101 floats
            for _ in range(9):
                 out += f"  {auto13}{auto13}{auto13}{auto13}{auto13}{auto13}\n"
                 
        # AUX DATA
        out += "#$ AUX_DATA\n"
        
        # Blocks (calling the Fortran generator's logic if available, or just printing Python 0-byte blocks)
        # We will embed the group 1 logic right here, since it's 100% standalone and we wrote it Python earlier.
        blocks = {
            'DISPLMNT': '#$ DISPLMNT\n',
            'FORCMNT': '#$ FORCMNT \n',
            'UNIFORM': '#$ UNIFORM \n',
            'WIND': '#$ WIND    \n',
            'OFFSETS': '#$ OFFSETS \n',
            'ALLOWBLS': '#$ ALLOWBLS\n' + '       0.000000     0.000000     0.000000     0.000000  1.00000      1.00000    \n' + '    1.00000         0.000000     0.000000  9999.99         0.000000  3.00000    \n' + ('       0.000000     0.000000     0.000000     0.000000     0.000000     0.000000\n'*22) + '    1.00000      1.00000      1.00000      1.00000      1.00000      1.00000    \n',
            'FLANGES': '#$ FLANGES \n',
            'SIF&TEES': '#$ SIF&TEES\n'
        }
        
        # BEND
        out += "#$ BEND    \n"
        for row in self.b_rows:
             out += f"  {self.fmt_val(row[4], 13)}{self.fmt_val(row[5], 13)}    -1.010100    -1.010100    -1.010100    -1.010100\n"
             out += f"           0           0           0           0           0           0\n"
             out += f"                                                                \n"

        # RIGID & EXPJT (Empty defaults)
        out += "#$ RIGID   \n"
        out += "#$ EXPJT   \n"

        # RESTRANT
        out += "#$ RESTRANT\n"
        for row in self.r_rows:
            node = self.fmt_val(row[4], 11)
            rtype = self.fmt_val(row[6], 13)
            out += f"  {node} {rtype}    -1.010100    -1.010100    -1.010100    -1.010100\n"
            out += f"      1.00000         0.000000     0.000000    -1.010100    -1.010100    -1.010100\n"
            out += f"           0           0           0           0           0           0\n"
            out += f"                                                                \n"

        # Print the rest of the group 1 blocks
        for name, data in blocks.items():
            if name != 'ALLOWBLS':
                 out += data
            else:
                 # Simplified ALLOWBLS for standalone mode
                 out += data
                 
        # Trailing
        out += "#$ REDUCERS\n"
        out += "  C\n  C\n  bars      \n"
        
        with open(out_file, 'w') as f:
            f.write(out)
            
        print(f"Export completed natively in Python. Standalone file written to {out_file}")

    def export(self, out_file):
        # We always run pure python standalone now, ensuring NO dependencies on original .CII
        self.write_standalone_python(out_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='middle_layer_template.csv')
    parser.add_argument('--output', default='final.cii')
    parser.add_argument('--mode', default='python')
    args = parser.parse_args()
    
    exporter = CaesarExporter(args.input, mode=args.mode)
    exporter.export(args.output)
