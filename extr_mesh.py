import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
import os
import icem_scripts

class MainApplication:
    def __init__(self,master):
        self.font = Font(family="Arial", size=12)
        self.wdir = os.getcwd().replace('\\','/') 
        self.master = master
        self.mainframe = tk.Frame(self.master)
        self.entrylist = [] 
         
        self.gui_set_paths()
        self.gui_set_mesh_params()
        self.gui_set_buttons()
        self.gui_set_grid()
        
    
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
        self.frame_om.grid(row=1,column=0,sticky='NSEW')
        self.label_optionmenu.grid(row=2,column=0,sticky='E')
        self.optionmenu_named_sel.grid(row=2,column=1,sticky='WE')
        

    def gui_set_buttons(self):
        self.frame_buttons = tk.Frame(self.mainframe,bd=2,relief='groove')
        self.button_extrude = tk.Button(
                self.frame_buttons,
                text='Extrude',
                font=self.font,
                command=self.cmd_extrude)
        self.button_help = tk.Button(
                self.frame_buttons,
                text='Help',
                font=self.font,
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
        
    def gui_set_grid(self):   
        self.mainframe.pack(fill='both')
        # --- Paths
        self.frame_paths.grid(row=0,column=0,sticky = 'NSEW',padx=5, pady=5)
        self.label_mesh.grid(row=0,column=0,sticky = 'E')
        self.entry_mesh.grid(row=0,column=1,sticky = 'WE',padx=5, pady=2)
        self.button_import_mesh.grid(row=0,column=2,sticky = 'WE',padx=5, pady=2)
        self.label_output_folder.grid(row=1,column=0,sticky = 'E')
        self.entry_output_folder.grid(row=1,column=1,sticky = 'WE',padx=5, pady=2)
        self.button_output_folder.grid(row=1,column=2,sticky = 'WE',padx=5, pady=2)
        
        # --- Mesh Params
        self.frame_params.grid(row=2,column=0,sticky = 'NSEW',padx=5, pady=5)
        self.label_spacing.grid(row=0,column=0,sticky = 'E')
        self.entry_spacing.grid(row=0,column=1,sticky = 'WE',padx=5, pady=2)
        self.label_ratio.grid(row=1,column=0,sticky = 'E')
        self.entry_ratio.grid(row=1,column=1,sticky = 'W',padx=5, pady=2)
        self.label_length.grid(row=2,column=0,sticky = 'E')
        self.entry_length.grid(row=2,column=1,sticky = 'W',padx=5, pady=2)

        # --- Buttons
        self.frame_buttons.grid(row=3,column=0,sticky = 'NSEW',padx=5, pady=5)
        self.button_extrude.grid(row=0,column=1,sticky = 'WE',padx=5, pady=2)
        self.button_help.grid(row=1,column=1,sticky = 'WE',padx=5, pady=2)
        
    def cmd_import_mesh(self):
        self.mesh_file_path = tk.filedialog.askopenfilename(
                title='Choose a mesh file',
                filetypes=(              
                        ("FLUENT mesh", "*.msh"),
                        ("ICEM mesh", "*.uns"),
                        ("All files", "*.*") ) )
        self.mesh_file_name = os.path.basename(self.mesh_file_path)
        self.mesh_file_dir_name = os.path.dirname(self.mesh_file_path)
        self.entry_mesh.delete(0,'end')
        self.entry_mesh.insert(0,self.mesh_file_path)
        
        if self.mesh_file_path:
            self.temp_files = icem_scripts.import_named_selections(self.mesh_file_path,self.wdir)       
            os.system('icemcfd -batch -script temp.tcl')
            self.named_selections = icem_scripts.get_names_from_fbc('temp.fbc')
            self.gui_set_optionmenu()
            
        if self.temp_files:
            self.cmd_delete_temp()
    
    def cmd_output_folder(self):
        self.output_folder = tk.filedialog.askdirectory(
                initialdir='.',
                title='Choose a folder')
        self.entry_output_folder.delete(0,'end')
        self.entry_output_folder.insert(0,self.output_folder)
    
    def cmd_extrude(self):
        self.cmd_check_entries()
    
    def cmd_help(self):
        return
    
    def cmd_check_entries(self):
        for entry in self.entrylist:
            if not entry.get():
                print ('Fill all entries!')
                break
     
    def cmd_delete_temp(self):
        if self.temp_files:
            for file in self.temp_files:
                if file.path.is_file():
                    os.remove(file)
        
    
def main():
    root = tk.Tk()
    root.title('Extrude mesh')
    ExtrudeApp = MainApplication(root)
    root.mainloop()
   
if __name__ == '__main__':
    main()
