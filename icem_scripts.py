# --- Define icem scripts for extrude mesh
import codecs
import re

def import_named_selections(inputfile,wdir):
    
    temp_files = []
    template_string = """
    
    # -------------------------------------
    # ---- ICEM SCRIPT FOR .atr EXPORT ----
    # -------------------------------------
    
    # --- Read .msh
    ic_read_external {C://Program Files/ANSYS Inc/v170/icemcfd/win64_amd/icemcfd/result-interfaces/readfluent.exe} !INPUT! 1 2 0 {}   
    
    ic_geo_new_family PART0
    ic_uns_move_family_elements ORFN PART0
    ic_csystem_display all 0
    ic_csystem_set_current global
    ic_boco_nastran_csystem reset
    ic_uns_diag_reset_degen_min_max
    ic_boco_solver
    ic_boco_solver {ANSYS Fluent}
    ic_solution_set_solver {ANSYS Fluent} 1
    ic_boco_solver {ANSYS Fluent}
    ic_solver_mesh_info {ANSYS Fluent}
    ic_boco_save !FOLDER!/temp.fbc
    ic_boco_save_atr !FOLDER!/temp.atr

    """
    
    script_to_run = template_string.replace('!INPUT!',inputfile)
    script_to_run = script_to_run.replace('!FOLDER!',wdir)
    output = open ('temp.tcl','w')
    output.write(script_to_run)
    output.close()
    temp_files.extend(['temp.fbc','temp.atr','temp.fbc_old','temp.tcl'])
    
    return temp_files

def get_names_from_fbc(inputfile):
    named_selections = []
    fp = codecs.open(inputfile,encoding='utf-8')
    for line in fp:
        if line:
            if not re.match(r'#', line):
                named_selections.append(line.rstrip().replace('"',''))
    named_selections = list(filter(None,named_selections))
    return named_selections
    
    
    
    

