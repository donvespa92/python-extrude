import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
from tkinter import messagebox
import os
from os.path import splitext
import icem_scripts as ic

class MainApplication:
    def __init__(self,master):
        self.font = Font(family="Arial", size=12)
        self.wdir = os.getcwd().replace('\\','/') 
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.cmd_exit)
        self.mainframe = tk.Frame(self.master)
        self.entrylist = [] 
        self.ns_import = False
             
        self.gui_set_paths()
        self.gui_set_names()
        self.gui_set_mesh_params()
        self.gui_set_chkbuttons()
        self.gui_set_buttons()
        self.gui_set_grid()
    
    def cmd_exit(self):
        self.cmd_delete_temp()
        self.master.destroy()
    
    def gui_set_paths(self):
        self.frame_paths = tk.Frame(self.mainframe,bd=2,relief='groove')
        self.entry_mesh = tk.Entry(
                self.frame_paths,
                width=50,
                font=self.font)
        self.label_mesh = tk.Label(
                self.frame_paths,
                text='Mesh',
                font=self.font)
        self.entry_output_folder = tk.Entry(
                self.frame_paths,
                width=50,
                font=self.font)
        self.label_output_folder = tk.Label(
                self.frame_paths,
                text='Output folder',font=self.font) 
        self.button_import_mesh = tk.Button(
                self.frame_paths,
                text='Select',
                font=self.font,
                command=self.cmd_import_mesh)
        self.button_output_folder = tk.Button(
                self.frame_paths,
                text='Select',
                font=self.font,
                command=self.cmd_output_folder)
        
        self.entrylist.append(self.entry_mesh)
        self.entrylist.append(self.entry_output_folder)
    
    def gui_set_names(self):
        self.frame_names = tk.Frame(self.mainframe,bd=2,relief='groove')
        self.entry_prj_name = tk.Entry(
                self.frame_names,
                width=50,
                font=self.font)
        self.label_prj_name = tk.Label(
                self.frame_names,
                text='Project name',
                font=self.font)
        self.entry_base_name = tk.Entry(
                self.frame_names,
                width=50,
                font=self.font)
        self.label_base_name = tk.Label(
                self.frame_names,
                text='Base name',
                font=self.font)
        
        self.entry_base_name.insert('end','base-name-for-wall-and-domain-name')
        self.entrylist.append(self.entry_prj_name)
        self.entrylist.append(self.entry_base_name)
    
    def gui_set_optionmenu(self):
        self.frame_om = tk.Frame(self.mainframe,bd=2,relief='groove',padx=5, pady=5)
        self.label_optionmenu = tk.Label(
                self.frame_om,
                text='Named selections',
                font=self.font)
        self.variable = tk.StringVar(self.frame_om)
        self.variable.set(self.named_selections[0])
        self.optionmenu_named_sel = tk.OptionMenu(
                self.frame_om,
                self.variable,*self.named_selections)
        self.optionmenu_named_sel.config(font=self.font)
        self.frame_om.grid(row=1,column=0,sticky='NSEW',padx=5, pady=5)
        self.label_optionmenu.grid(row=2,column=0,sticky='E')
        self.optionmenu_named_sel.grid(row=2,column=1,sticky='WE')
        
        
    def gui_set_chkbuttons(self):
        self.var_cfx5 = tk.IntVar()
        self.var_open_mesh = tk.IntVar()
        
        self.frame_chkbuttons = tk.Frame(self.mainframe,bd=2,relief='groove')
        self.chkbutton_cfx5 = tk.Checkbutton(
                self.frame_chkbuttons,
                text='Keep only .cfx5',
                font=self.font,
                variable=self.var_cfx5)
        self.chkbutton_open_mesh = tk.Checkbutton(
                self.frame_chkbuttons,
                text='Open mesh',
                font=self.font,
                variable=self.var_open_mesh)
        
        self.chkbutton_cfx5.select()
    
    def gui_set_buttons(self):
        self.frame_buttons = tk.Frame(self.mainframe,relief='flat')
        self.button_extrude = tk.Button(
                self.frame_buttons,
                text='Extrude',
                font=self.font,
                height=2,
                command=self.cmd_extrude)
        self.button_help = tk.Button(
                self.frame_buttons,
                text='Help',
                font=self.font,
                height=2,
                command=self.cmd_help)
            
    def gui_set_mesh_params(self):
        self.frame_params = tk.Frame(self.mainframe,bd=2,relief='groove')
        self.label_spacing = tk.Label(
                self.frame_params,
                text='Spacing',
                font=self.font)
        self.entry_spacing = tk.Entry(
                self.frame_params,
                width=30,
                font=self.font)
        self.label_ratio = tk.Label(
                self.frame_params,
                text='Ratio',
                font=self.font)
        self.entry_ratio = tk.Entry(
                self.frame_params,
                width=30,
                font=self.font)
        self.label_length = tk.Label(
                self.frame_params,
                text='Length',
                font=self.font)
        self.entry_length = tk.Entry(
                self.frame_params,
                width=30,
                font=self.font)
        
        self.entrylist.append(self.entry_spacing)
        self.entrylist.append(self.entry_ratio)
        self.entrylist.append(self.entry_length)
        
        self.entry_spacing.insert('end','0.00075')
        self.entry_ratio.insert('end','1.03')
        
    def gui_set_grid(self):   
        self.mainframe.grid(row=0,column=0,sticky = 'NSEW',padx=5, pady=5)
        #self.master.columnconfigure(0,weight=1,minsize=500)
        #self.mainframe.columnconfigure(0,weight=1,minsize=500)
        
        # --- Paths
        self.frame_paths.grid(row=0,column=0,sticky = 'NSEW',padx=5, pady=5)
        self.label_mesh.grid(row=0,column=0,sticky = 'E')
        self.entry_mesh.grid(row=0,column=1,sticky = 'WE',padx=5, pady=2)
        self.button_import_mesh.grid(row=0,column=2,sticky = 'WE',padx=5, pady=2)
        self.label_output_folder.grid(row=1,column=0,sticky = 'E')
        self.entry_output_folder.grid(row=1,column=1,sticky = 'WE',padx=5, pady=2)
        self.button_output_folder.grid(row=1,column=2,sticky = 'WE',padx=5, pady=2)
                
        # --- Names
        self.frame_names.grid(row=2,column=0,sticky = 'NSEW',padx=5, pady=5)
        self.label_prj_name.grid(row=0,column=0,sticky = 'E')
        self.entry_prj_name.grid(row=0,column=1,sticky = 'WE',padx=5, pady=2)
        self.label_base_name.grid(row=1,column=0,sticky = 'E')
        self.entry_base_name.grid(row=1,column=1,sticky = 'WE',padx=5, pady=2)
        
        # --- Mesh Params
        self.frame_params.grid(row=3,column=0,sticky = 'NSEW',padx=5, pady=5)
        self.label_spacing.grid(row=0,column=0,sticky = 'E')
        self.entry_spacing.grid(row=0,column=1,sticky = 'WE',padx=5, pady=2)
        self.label_ratio.grid(row=1,column=0,sticky = 'E')
        self.entry_ratio.grid(row=1,column=1,sticky = 'W',padx=5, pady=2)
        self.label_length.grid(row=2,column=0,sticky = 'E')
        self.entry_length.grid(row=2,column=1,sticky = 'W',padx=5, pady=2)
        
        # --- Checkbuttons
        self.frame_chkbuttons.grid(row=4,column=0,sticky = 'NSEW',padx=5, pady=5)
        self.chkbutton_cfx5.grid(row=0,column=0,sticky = 'W',padx=5, pady=2)
        self.chkbutton_open_mesh.grid(row=1,column=0,sticky = 'W',padx=5, pady=2)
        
        # --- Buttons
        self.frame_buttons.grid(row=5,column=0,sticky = 'NSEW',padx=5, pady=5)
        self.button_extrude.pack(fill='both')
        #self.button_help.grid(row=1,column=1,sticky = 'WE',padx=5, pady=2)
        
    def cmd_import_mesh(self):
        temp = tk.filedialog.askopenfilename(
                title='Choose a mesh file',
                filetypes=(              
                        ("FLUENT mesh", "*.msh"),
                        ("ICEM mesh", "*.uns"),
                        ("All files", "*.*") ) )

        if temp:
            self.mesh_file_path = temp
            self.mesh_file_name = os.path.basename(self.mesh_file_path)
            self.mesh_file_dir_name = os.path.dirname(self.mesh_file_path)
            self.mesh_file_type = splitext(self.mesh_file_path)[1]
            self.entry_mesh.delete(0,'end')
            self.entry_mesh.insert(0,self.mesh_file_path)
            self.output_folder = self.mesh_file_dir_name
            self.entry_output_folder.delete(0,'end')
            self.entry_output_folder.insert(0,self.mesh_file_dir_name)
            
            self.temp_files = ic.import_named_selections(self.mesh_file_path,self.wdir)       
            os.system('icemcfd -batch -script temp.tcl')
            self.named_selections = ic.get_names_from_fbc('temp.fbc')
            self.gui_set_optionmenu()
            self.ns_import = True
            self.entry_prj_name.delete(0,'end')
            self.entry_prj_name.insert(0,self.mesh_file_name.split('.')[0])            
            self.cmd_get_normal()
            self.temp_files.append(self.wdir+'/mesh.stl')
    
        if self.temp_files:
            self.cmd_delete_temp()
    
    def cmd_output_folder(self):
        temp = tk.filedialog.askdirectory(initialdir='.',title='Choose a folder')
        if temp:
            self.output_folder = temp
            self.entry_output_folder.delete(0,'end')
            self.entry_output_folder.insert(0,self.output_folder)
    
    def cmd_extrude(self):
        self.do_checks()
        
        if (self.check == True):       
            # --- Set params for extrude
            ratio = float(self.entry_ratio.get())
            length = float(self.entry_length.get())
            spacing = float(self.entry_spacing.get())
            layers = ic.calc_params({'ratio':ratio,'length':length,'spacing':spacing})
            
            if (self.mesh_file_type == '.msh'):
                mesh_type = 'fluent'
            else:
                mesh_type = 'icem'
            
            d_input = {'mesh_type': mesh_type,
                       'spacing': str(spacing),
                       'ratio': str(ratio),
                       'layers': str(layers),
                       'mesh_file_path': self.mesh_file_path,
                       'export_folder': self.output_folder,
                       'project_name': self.entry_prj_name.get(),
                       'wl_name': 'wl_'+self.entry_base_name.get(),
                       'dom_name': 'fld_'+self.entry_base_name.get(),
                       'bc_name': 'bc_'+self.entry_base_name.get(),
                       'if_name': self.variable.get(),
                       'normal': '{'+str((' '.join(self.normal)))+'}', 
                       }
            
            for key in d_input:
                print (' # --- '+ key +': '+str(d_input[key]))
        
            self.temp_files.extend(ic.extrude_mesh(d_input))
            self.temp_files.extend(['temp.tcl'])
            self.temp_files.extend([
                    d_input['export_folder']+'/'+d_input['project_name']+'.prj',
                    d_input['export_folder']+'/'+d_input['project_name']+'.uns',
                    d_input['export_folder']+'/'+d_input['project_name']+'.fbc',
                    d_input['export_folder']+'/'+d_input['project_name']+'.atr'])
            
            os.system('icemcfd -batch -script temp.tcl')
                       
            if self.var_open_mesh.get() == 1:
                os.system(d_input['export_folder']+'/'+d_input['project_name']+'.uns')
            
            self.cmd_delete_temp()
                 
        else: return (42)
    
    def cmd_get_normal(self):
        script_to_run = ic.export_stl(self.mesh_file_path)
        os.system('icemcfd -batch -script temp.tcl')
        os.remove('temp.tcl')
        
        # --- Open .stl and get face normal
        self.normal = []
        with open('mesh.stl') as fp:
            for line in fp:
                if ('facet normal' in line):
                    line = line.strip()
                    line = line.replace('facet normal ','')
                    self.normal = line.split(' ')
                    break
        
    def cmd_help(self):
        return
           
        
    def cmd_delete_temp(self):
        if self.temp_files:
            for file in self.temp_files:
                if os.path.exists(file):
                    os.remove(file)
                     
    def do_checks(self):
        self.check = True
        for entry in self.entrylist:
            if not entry.get():
                messagebox.showerror("Error","Fill all entries!")
                self.check = False
                return
                break    
        
        if self.ns_import == False:
            self.check = False
            messagebox.showerror("Error","No named selections are imported!")
            return

        for entry in [self.entry_length,self.entry_ratio,self.entry_spacing]:  
            try:
                float(entry.get())
                return True
            except ValueError:
                messagebox.showerror("Error","Params are not numeric!")
                self.check = False
                return False
               
def main():
    root = tk.Tk()
    root.title('Extrude mesh')
    MainApplication(root)
    root.resizable(width=False, height=False)
    root.mainloop()
   
if __name__ == '__main__':
    main()
