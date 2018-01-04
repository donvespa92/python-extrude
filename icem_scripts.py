# --- Define icem scripts for extrude mesh
import codecs
import re
import math
import os
from os.path import splitext

def import_named_selections(inputfile,wdir):
    
    fn,ext = splitext(inputfile)
    ext = ext.replace('.','')
    temp_files = []
    template_string = """
    
    # -------------------------------------
    # ---- ICEM SCRIPT FOR .atr EXPORT ----
    # -------------------------------------
    set mesh_type "!MESH_TYPE!"
    
    if { $mesh_type eq "msh" } {
        ic_read_external {C://Program Files/ANSYS Inc/v170/icemcfd/win64_amd/icemcfd/result-interfaces/readfluent.exe} !INPUT! 1 2 0 {}       
    } elseif { $mesh_type eq "uns" } {
        ic_uns_load !INPUT! 3 0 {} 2
    }
    
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
    script_to_run = script_to_run.replace('!MESH_TYPE!',ext)
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
    
def calc_params(inputdata):
    length = inputdata['length']
    ratio = inputdata['ratio']
    spacing = inputdata['spacing']
    layers = math.log(1-(length*(1-ratio))/spacing)/math.log(ratio)
    layers = math.ceil(layers)
    return layers

def export_stl(inputfile):
    
    temp_script = """
    
    set mesh_type "!MESH_TYPE!"
    set import_path !IMPORT_PATH!
    set export_path !EXPORT_PATH!
    
    if { $mesh_type eq "msh" } {
        ic_read_external {C://Program Files/ANSYS Inc/v172/icemcfd/win64_amd/icemcfd/result-interfaces/readfluent.exe} $import_path 1 2 0 {}
    } elseif { $mesh_type eq "uns" } {
        ic_uns_load !IMPORT_PATH! 3 0 {} 2
    }
    
    ic_geo_new_family PART0
    ic_uns_move_family_elements ORFN PART0
    
    # --- Set solver to .stl
    ic_undo_group_begin
    ic_boco_solver STL
    ic_solver_mesh_info STL
    ic_undo_group_end
    ic_boco_solver
    ic_boco_solver STL
    ic_solution_set_solver STL 1
    
    # --- Save project
    ic_boco_save $export_path/ansys.fbc
    ic_boco_save_atr $export_path/ansys.atr
    ic_chdir $export_path
    ic_delete_empty_parts
    ic_empty_tetin
    ic_uns_check_duplicate_numbers
    ic_save_unstruct project1.uns 1 {} {} {}
    ic_uns_set_modified 1
    ic_cart_is_loaded
    ic_save_project_file $export_path/project1.prj {array\ set\ file_name\ \{ {    catia_dir .} {    parts_dir .} {    domain_loaded 0} {    cart_file_loaded 0} {    cart_file {}} {    domain_saved project1.uns} {    archive {}} {    med_replay {}} {    topology_dir .} {    ugparts_dir .} {    icons {{$env(ICEM_ACN)/lib/ai_env/icons} {$env(ICEM_ACN)/lib/va/EZCAD/icons} {$env(ICEM_ACN)/lib/icons} {$env(ICEM_ACN)/lib/va/CABIN/icons}}} {    tetin {}} {    family_boco ansys.fbc} {    iges_dir .} {    solver_params_loaded 0} {    attributes_loaded 0} {    project_lock {}} {    attributes ansys.atr} {    domain project1.uns} {    domains_dir .} {    settings_loaded 0} {    settings project1.prj} {    blocking {}} {    hexa_replay {}} {    transfer_dir .} {    mesh_dir .} {    family_topo {}} {    gemsparts_dir .} {    family_boco_loaded 0} {    tetin_loaded 0} {    project_dir .} {    topo_mulcad_out {}} {    solver_params {}} \} array\ set\ options\ \{ {    expert 1} {    remote_path {}} {    tree_disp_quad 2} {    tree_disp_pyra 0} {    evaluate_diagnostic 0} {    histo_show_default 1} {    select_toggle_corners 0} {    remove_all 0} {    keep_existing_file_names 0} {    record_journal 0} {    edit_wait 0} {    face_mode all} {    select_mode all} {    med_save_emergency_tetin 1} {    user_name darazsb} {    diag_which all} {    uns_warn_if_display 500000} {    bubble_delay 1000} {    external_num 1} {    tree_disp_tri 2} {    apply_all 0} {    default_solver {ANSYS CFX}} {    temporary_directory {}} {    flood_select_angle 0} {    home_after_load 1} {    project_active 0} {    histo_color_by_quality_default 1} {    undo_logging 1} {    tree_disp_hexa 0} {    histo_solid_default 1} {    host_name econ-128} {    xhidden_full 1} {    replay_internal_editor 1} {    editor {}} {    mouse_color orange} {    clear_undo 1} {    remote_acn {}} {    remote_sh csh} {    tree_disp_penta 0} {    n_processors 1} {    remote_host {}} {    save_to_new 0} {    quality_info Quality} {    tree_disp_node 0} {    med_save_emergency_mesh 1} {    redtext_color red} {    tree_disp_line 0} {    select_edge_mode 0} {    use_dlremote 0} {    max_mesh_map_size 1024} {    show_tris 1} {    remote_user {}} {    enable_idle 0} {    auto_save_views 1} {    max_cad_map_size 512} {    display_origin 0} {    uns_warn_user_if_display 1000000} {    detail_info 0} {    win_java_help 0} {    show_factor 1} {    boundary_mode all} {    clean_up_tmp_files 1} {    auto_fix_uncovered_faces 1} {    med_save_emergency_blocking 1} {    max_binary_tetin 0} {    tree_disp_tetra 0} \} array\ set\ disp_options\ \{ {    uns_dualmesh 0} {    uns_warn_if_display 500000} {    uns_normals_colored 0} {    uns_icons 0} {    uns_locked_elements 0} {    uns_shrink_npos 0} {    uns_node_type None} {    uns_icons_normals_vol 0} {    uns_bcfield 0} {    backup Wire} {    uns_nodes 0} {    uns_only_edges 0} {    uns_surf_bounds 0} {    uns_wide_lines 0} {    uns_vol_bounds 0} {    uns_displ_orient Triad} {    uns_orientation 0} {    uns_directions 0} {    uns_thickness 0} {    uns_shell_diagnostic 0} {    uns_normals 0} {    uns_couplings 0} {    uns_periodicity 0} {    uns_single_surfaces 0} {    uns_midside_nodes 1} {    uns_shrink 100} {    uns_multiple_surfaces 0} {    uns_no_inner 0} {    uns_enums 0} {    uns_disp Wire} {    uns_bcfield_name {}} {    uns_color_by_quality 0} {    uns_changes 0} {    uns_cut_delay_count 1000} \} {set icon_size1 24} {set icon_size2 35} {set thickness_defined 0} {set solver_type 1} {set solver_setup 1} array\ set\ prism_values\ \{ {    n_triangle_smoothing_steps 5} {    min_smoothing_steps 6} {    first_layer_smoothing_steps 1} {    new_volume {}} {    height {}} {    prism_height_limit {}} {    interpolate_heights 0} {    n_tetra_smoothing_steps 10} {    do_checks {}} {    delete_standalone 1} {    ortho_weight 0.50} {    max_aspect_ratio {}} {    ratio_max {}} {    incremental_write 0} {    total_height {}} {    use_prism_v10 0} {    intermediate_write 1} {    delete_base_triangles {}} {    ratio_multiplier {}} {    verbosity_level 1} {    refine_prism_boundary 1} {    max_size_ratio {}} {    triangle_quality {}} {    max_prism_angle 180} {    tetra_smooth_limit 0.3} {    max_jump_factor 5} {    use_existing_quad_layers 0} {    layers 3} {    fillet 0.10} {    into_orphan 0} {    init_dir_from_prev {}} {    blayer_2d 0} {    do_not_allow_sticking {}} {    top_family {}} {    law exponential} {    min_smoothing_val 0.1} {    auto_reduction 0} {    stop_columns 1} {    stair_step 1} {    smoothing_steps 12} {    side_family {}} {    min_prism_quality 0.01} {    ratio 1.2} \} {set aie_current_flavor {}} array\ set\ vid_options\ \{ {    wb_import_mat_points 0} {    wb_NS_to_subset 0} {    wb_import_surface_bodies 1} {    wb_import_cad_att_pre {SDFEA;DDM}} {    wb_import_mix_res_line 0} {    wb_import_tritol 0.001} {    auxiliary 0} {    wb_import_cad_att_trans 1} {    wb_import_mix_res -1} {    wb_import_mix_res_surface 0} {    show_name 0} {    wb_import_solid_bodies 1} {    wb_import_delete_solids 0} {    wb_import_mix_res_solid 0} {    wb_import_save_pmdb {}} {    inherit 1} {    default_part GEOM} {    new_srf_topo 1} {    wb_import_associativity_model_name {}} {    DelPerFlag 0} {    wb_import_line_bodies 0} {    wb_import_save_partfile 0} {    composite_tolerance 1.0} {    wb_NS_to_entity_parts 0} {    wb_import_en_sym_proc 1} {    wb_import_sel_proc 1} {    wb_import_work_points 0} {    wb_import_reference_key 0} {    wb_import_mix_res_point 0} {    wb_import_pluginname {}} {    wb_NS_only 0} {    wb_import_create_solids 0} {    wb_import_refresh_pmdb 0} {    wb_import_sel_pre {}} {    wb_import_scale_geo Default} {    wb_import_load_pmdb {}} {    replace 0} {    wb_import_cad_associativity 0} {    same_pnt_tol 1e-4} {    tdv_axes 1} {    vid_mode 0} {    DelBlkPerFlag 0} \} {set savedTreeVisibility {meshNode 2 mesh_subsetNode 2 meshShellNode 2 meshTriNode 2 meshQuadNode 2 partNode 2 part-FFIF_INLET_BLOCK 2}} {set last_view {rot {-0.0350581868233 0.31257845739 -0.000446611542332 0.949244663955} scale {19683.9140905 19683.9140905 19683.9140905} center {0.00015 -2e-007 6.9e-006} pos {-30.4612649309 52.525286925 0}}} array\ set\ cut_info\ \{ {    active 0} \} array\ set\ hex_option\ \{ {    default_bunching_ratio 2.0} {    floating_grid 0} {    project_to_topo 0} {    n_tetra_smoothing_steps 20} {    sketching_mode 0} {    trfDeg 1} {    wr_hexa7 0} {    smooth_ogrid 0} {    find_worst 1-3} {    hexa_verbose_mode 0} {    old_eparams 0} {    uns_face_mesh_method uniform_quad} {    multigrid_level 0} {    uns_face_mesh one_tri} {    check_blck 0} {    proj_limit 0} {    check_inv 0} {    project_bspline 0} {    hexa_update_mode 1} {    default_bunching_law BiGeometric} {    worse_criterion Quality} \} array\ set\ saved_views\ \{ {    views {}} \}} {ICEM CFD}
    
    # --- Export .stl
    ic_exec {C:/Program Files/ANSYS Inc/v172/icemcfd/win64_amd/icemcfd/output-interfaces/stl} project1.uns ./mesh.stl ascii no_shift
    
    # --- Delete files
    file delete -force -- $export_path/ansys.fbc
    file delete -force -- $export_path/ansys.fbc_old
    file delete -force -- $export_path/ansys.atr
    file delete -force -- $export_path/project1.uns
    file delete -force -- $export_path/project1.prj    
       
    """
    
    dirname = os.getcwd().replace('\\','/')
    fn,ext = splitext(inputfile)
    ext = ext.replace('.','')
    
    script_to_run = temp_script.replace('!MESH_TYPE!',ext)
    script_to_run = script_to_run.replace('!IMPORT_PATH!',inputfile)
    script_to_run = script_to_run.replace('!EXPORT_PATH!',dirname)
    
    output = open ('temp.tcl','w')
    output.write(script_to_run)
    output.close()
    return output
    
def extrude_mesh(inputdata):
        
    temp_script = """
    
    set mesh_type !MESH_TYPE!
    set spacing !SPACING!
    set ratio !RATIO!
    set layers !LAYERS!
    set mesh_file_path !MESH_FILE_PATH!
    set export_folder !EXPORT_FOLDER!
    set project_name !PROJECT_NAME!
    set if_name !IF_NAME!
    set dom_name !DOM_NAME!
    set wl_name !WL_NAME!
    set bc_name !BC_NAME!
    set normal !NORMAL!
    
    # --- File names
    set prj_name [concat $export_folder/$project_name.prj]
    set tin_name [concat $export_folder/$project_name.tin]
    set uns_name [concat $export_folder/$project_name.uns]
    set fbc_name [concat $export_folder/$project_name.fbc]
    set atr_name [concat $export_folder/$project_name.atr]
    set cfx5_name [concat $export_folder/$project_name.cfx5]
       
        
    # --- Import mesh
    if {$mesh_type eq {icem}} {
            ic_uns_load $mesh_file_path 3 0 {} 2
    } else {
            ic_read_external {C://Program Files/ANSYS Inc/v170/icemcfd/win64_amd/icemcfd/result-interfaces/readfluent.exe} $mesh_file_path 1 2 0 {}
    }
    
    # --- Select elements
    ic_uns_create_selection_subset 0
    ic_uns_create_selection_edgelist 1
    ic_uns_subset_configure uns_sel_0 -draw_nodes 1
    ic_uns_subset_visible uns_sel_0 0
    ic_uns_subset_make_families uns_sel_0 $if_name
    ic_uns_uniqify uns_sel_0
    ic_uns_subset_visible uns_sel_0 0
    ic_uns_create_selection_edgelist 0
    ic_uns_subset_create
    ic_uns_subset_visible uns_sub_0 0
    ic_uns_subset_add_families_and_types uns_sub_0 $if_name {TRI_3 QUAD_4}
    ic_uns_subset_add_from uns_sel_0 uns_sub_0
    ic_uns_subset_delete uns_sub_0
    ic_undo_group_begin
    
    # --- Extrude mesh
    ic_geo_new_family $dom_name
    ic_boco_set_part_color $dom_name
    ic_geo_new_family $wl_name
    ic_boco_set_part_color $wl_name
    ic_geo_new_family $bc_name
    ic_boco_set_part_color $bc_name
    ic_extrude map uns_sel_0 numlayers $layers dir $normal space func space_func $spacing*pow($ratio,layer-1) rpoint {0 0 0} rdir {0 0 0} rangle 10.0 volf $dom_name sidef $wl_name topf $bc_name curve {} curvedir 0 twist 0 del_orig 0 del_covered 0 degen_tol 0.00001 trans_rot_vec {0 0 0} spacing_transl_rot 0.0 project 0
    ic_uns_subset_delete uns_sel_0
    ic_delete_empty_parts
    ic_undo_group_end
    
    # --- Save project
    ic_delete_empty_parts 
    ic_empty_tetin 
    ic_uns_check_duplicate_numbers 
    ic_uns_renumber_all_elements 1 1
    ic_save_unstruct $uns_name 1 {} {} {}
    ic_uns_set_modified 1
    ic_boco_solver 
    ic_boco_solver {ANSYS Fluent}
    ic_solution_set_solver {ANSYS Fluent} 1
    ic_boco_solver {ANSYS Fluent}
    ic_solver_mesh_info {ANSYS Fluent}
    ic_boco_save $fbc_name
    ic_boco_save_atr $atr_name
    ic_cart_is_loaded 
    ic_save_project_file $prj_name {array\ set\ file_name\ \{ {    catia_dir .} {    parts_dir .} {    domain_loaded 0} {    cart_file_loaded 0} {    cart_file {}} {    domain_saved $uns_name} {    archive {}} {    med_replay {}} {    topology_dir .} {    ugparts_dir .} {    icons {{$env(ICEM_ACN)/lib/ai_env/icons} {$env(ICEM_ACN)/lib/va/EZCAD/icons} {$env(ICEM_ACN)/lib/icons} {$env(ICEM_ACN)/lib/va/CABIN/icons}}} {    tetin {}} {    family_boco $fbc_name} {    iges_dir .} {    solver_params_loaded 0} {    attributes_loaded 0} {    project_lock {}} {    attributes $atr_name} {    domain $uns_name} {    domains_dir .} {    settings_loaded 0} {    settings $prj_name} {    blocking {}} {    hexa_replay {}} {    transfer_dir .} {    mesh_dir .} {    family_topo {}} {    gemsparts_dir .} {    family_boco_loaded 0} {    tetin_loaded 0} {    project_dir .} {    topo_mulcad_out {}} {    solver_params {}} \} array\ set\ options\ \{ {    expert 1} {    remote_path {}} {    tree_disp_quad 2} {    tree_disp_pyra 0} {    evaluate_diagnostic 0} {    histo_show_default 1} {    select_toggle_corners 0} {    remove_all 0} {    keep_existing_file_names 0} {    record_journal 0} {    edit_wait 0} {    face_mode all} {    select_mode all} {    med_save_emergency_tetin 1} {    user_name bence.darazs} {    diag_which all} {    uns_warn_if_display 500000} {    bubble_delay 1000} {    external_num 1} {    tree_disp_tri 2} {    apply_all 0} {    temporary_directory {}} {    flood_select_angle 0} {    home_after_load 1} {    project_active 0} {    histo_color_by_quality_default 1} {    undo_logging 1} {    tree_disp_hexa 0} {    histo_solid_default 1} {    host_name econ-128} {    xhidden_full 1} {    editor {}} {    mouse_color orange} {    clear_undo 1} {    remote_acn {}} {    remote_sh csh} {    tree_disp_penta 0} {    n_processors 1} {    remote_host {}} {    save_to_new 0} {    quality_info Quality} {    tree_disp_node 0} {    med_save_emergency_mesh 1} {    redtext_color red} {    tree_disp_line 0} {    select_edge_mode 0} {    use_dlremote 0} {    max_mesh_map_size 1024} {    show_tris 1} {    remote_user {}} {    enable_idle 0} {    auto_save_views 1} {    max_cad_map_size 512} {    display_origin 0} {    uns_warn_user_if_display 1000000} {    detail_info 0} {    win_java_help 0} {    show_factor 1} {    boundary_mode all} {    clean_up_tmp_files 1} {    auto_fix_uncovered_faces 1} {    med_save_emergency_blocking 1} {    max_binary_tetin 0} {    tree_disp_tetra 0} \} array\ set\ disp_options\ \{ {    uns_dualmesh 0} {    uns_warn_if_display 500000} {    uns_normals_colored 0} {    uns_icons 0} {    uns_locked_elements 0} {    uns_shrink_npos 0} {    uns_node_type None} {    uns_icons_normals_vol 0} {    uns_bcfield 0} {    backup Wire} {    uns_nodes 0} {    uns_only_edges 0} {    uns_surf_bounds 0} {    uns_wide_lines 0} {    uns_vol_bounds 0} {    uns_displ_orient Triad} {    uns_orientation 0} {    uns_directions 0} {    uns_thickness 0} {    uns_shell_diagnostic 0} {    uns_normals 0} {    uns_couplings 0} {    uns_periodicity 0} {    uns_single_surfaces 0} {    uns_midside_nodes 1} {    uns_shrink 100} {    uns_multiple_surfaces 0} {    uns_no_inner 0} {    uns_enums 0} {    uns_disp Wire} {    uns_bcfield_name {}} {    uns_color_by_quality 0} {    uns_changes 0} {    uns_cut_delay_count 1000} \} {set icon_size1 24} {set icon_size2 35} {set thickness_defined 0} {set solver_type 1} {set solver_setup -1} array\ set\ prism_values\ \{ {    n_triangle_smoothing_steps 5} {    min_smoothing_steps 6} {    first_layer_smoothing_steps 1} {    new_volume {}} {    height {}} {    prism_height_limit {}} {    interpolate_heights 0} {    n_tetra_smoothing_steps 10} {    do_checks {}} {    delete_standalone 1} {    ortho_weight 0.50} {    max_aspect_ratio {}} {    ratio_max {}} {    incremental_write 0} {    total_height {}} {    use_prism_v10 0} {    intermediate_write 1} {    delete_base_triangles {}} {    ratio_multiplier {}} {    verbosity_level 1} {    refine_prism_boundary 1} {    max_size_ratio {}} {    triangle_quality {}} {    max_prism_angle 180} {    tetra_smooth_limit 0.3} {    max_jump_factor 5} {    use_existing_quad_layers 0} {    layers 3} {    fillet 0.10} {    into_orphan 0} {    init_dir_from_prev {}} {    blayer_2d 0} {    do_not_allow_sticking {}} {    top_family {}} {    law exponential} {    min_smoothing_val 0.1} {    auto_reduction 0} {    stop_columns 1} {    stair_step 1} {    smoothing_steps 12} {    side_family {}} {    min_prism_quality 0.01} {    ratio 1.2} \} {set aie_current_flavor {}} array\ set\ vid_options\ \{ {    auxiliary 0} {    show_name 0} {    inherit 1} {    default_part GEOM} {    new_srf_topo 1} {    DelPerFlag 0} {    composite_tolerance 1.0} {    replace 0} {    same_pnt_tol 1e-4} {    tdv_axes 1} {    vid_mode 0} {    DelBlkPerFlag 0} \} array\ set\ map_tetin_sizes\ \{ {    densities 1} {    msurfaces 1} {    ppoint 1} {    thincuts 1} {    tetin {}} {    psurfaces 1} {    mcurves 1} {    mpoint 1} {    doit 0} {    pcurves 1} {    global 1} {    subsets 1} {    family 1} \} array\ set\ import_model_options\ \{ {    from_source 0} {    always_ref_key 0} {    always_convert 0} {    named_sel_only 0} {    always_import 0} {    convert_to Unitless} \} {set savedTreeVisibility {geomNode 0 geom_subsetNode 2 meshNode 1 mesh_subsetNode 2 meshLineNode 2 meshShellNode 2 meshTriNode 2 meshQuadNode 2 meshVolumeNode 0 meshHexaNode 0 meshPentaNode 0 partNode 2 part-BC_COOLER 2 part-FFIF_OUTLET_COOLER_1 2 part-FLD_COOLER 2 part-WL_COOLER 2}} {set last_view {rot {-0.0942626947661 0.195906670687 -0.00465096019544 0.976070432563} scale {1404.44738191 1404.44738191 1404.44738191} center {0 0 0} pos {0.0 0.0 0}}} array\ set\ cut_info\ \{ {    active 0} \} array\ set\ hex_option\ \{ {    default_bunching_ratio 2.0} {    floating_grid 0} {    project_to_topo 0} {    n_tetra_smoothing_steps 20} {    sketching_mode 0} {    trfDeg 1} {    wr_hexa7 0} {    smooth_ogrid 0} {    find_worst 1-3} {    hexa_verbose_mode 0} {    old_eparams 0} {    uns_face_mesh_method uniform_quad} {    multigrid_level 0} {    uns_face_mesh one_tri} {    check_blck 0} {    proj_limit 0} {    check_inv 0} {    project_bspline 0} {    hexa_update_mode 1} {    default_bunching_law BiGeometric} \} array\ set\ saved_views\ \{ {    views {}} \}} {ICEM CFD}
    
    ic_boco_solver {ANSYS CFX}
    ic_solver_mesh_info {ANSYS CFX}
    ic_exec {C:/Program Files/ANSYS Inc/v170/icemcfd/win64_amd/icemcfd/output-interfaces/cfx5} -dom $uns_name -b $fbc_name -ascii -db -internal_faces $cfx5_name

    """

    script_to_run = temp_script.replace('!MESH_TYPE!',inputdata['mesh_type'])    
    script_to_run = script_to_run.replace('!SPACING!',inputdata['spacing'])
    script_to_run = script_to_run.replace('!RATIO!',inputdata['ratio'])
    script_to_run = script_to_run.replace('!LAYERS!',inputdata['layers'])
    script_to_run = script_to_run.replace('!MESH_FILE_PATH!',inputdata['mesh_file_path'])
    script_to_run = script_to_run.replace('!EXPORT_FOLDER!',inputdata['export_folder'])
    script_to_run = script_to_run.replace('!PROJECT_NAME!',inputdata['project_name'])
    script_to_run = script_to_run.replace('!BC_NAME!',inputdata['bc_name'])
    script_to_run = script_to_run.replace('!WL_NAME!',inputdata['wl_name'])
    script_to_run = script_to_run.replace('!IF_NAME!',inputdata['if_name'])
    script_to_run = script_to_run.replace('!DOM_NAME!',inputdata['dom_name'])
    script_to_run = script_to_run.replace('!NORMAL!',inputdata['normal'])
    
    output = open ('temp.tcl','w')
    output.write(script_to_run)
    output.close()
    
    temp_files = [inputdata['export_folder']+'/'+inputdata['project_name']+'.cfx5.log',
                  inputdata['export_folder']+'/'+inputdata['project_name']+'.fbc_old',
                  inputdata['export_folder']+'/'+inputdata['project_name']+'.fbc_dfupdate',
                  inputdata['export_folder']+'/'+inputdata['project_name']+'.uns.bak']
    
    return temp_files
    
        
    
