
    
    # -------------------------------------
    # ---- ICEM SCRIPT FOR .atr EXPORT ----
    # -------------------------------------
    
    # --- Read .msh
    ic_read_external {C://Program Files/ANSYS Inc/v170/icemcfd/win64_amd/icemcfd/result-interfaces/readfluent.exe} D:/TMP/test.msh 1 2 0 {}   
    
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
    ic_boco_save D:/TMP/python/tkinter/python-extrude/temp.fbc
    ic_boco_save_atr D:/TMP/python/tkinter/python-extrude/temp.atr

    