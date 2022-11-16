import config
import departmentdata as college
import tscoreutility as tsc
import dirutility as dutil
import reportutility as rutil

import os
import subprocess
import sqlite3
import pathlib
import shutil
# import logging
import threading
import traceback
import tkinter as tk
# import webbrowser

from datetime import datetime
from tkinter import ttk
from tkinter import filedialog, messagebox
from pprint import pprint

import openpyxl
from dateutil import parser

# globals are {curItemId, button_generate, order}
# 1 is ascending order and 0 is descending order
inputs : list = []
order       = 1
debug_setting = config.DEBUG_MODE
FIELD_SIZE  = 50
PX, PY      = (10, 10)
FONT        = ('', 16)
DATERANGE   = tuple(range(1, 32))
MONTHRANGE  = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                'Sep', 'Oct', 'Nov', 'Dec')
YEARRANGE   = tuple(range(datetime.now().year, 1999, -1))
MIXED       = "MIXED"
COMBINED    = "COMBINED"


def setup_logging(file: str, enc: str = 'ascii'):#, level=logging.WARNING):
    """
    https://docs.python.org/3/howto/logging.html
    https://docs.python.org/3/library/codecs.html#module-codecs
    """
    dutil.create_safe_dir(config.LOGDIR)
    logging.basicConfig(filename=file, #encoding=enc, errors='xmlcharrefreplace',
        level=level, format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p')


def log_error(msg: str, *msgs: str):
    dutil.create_safe_dir(config.LOGDIR)
    LOGEXT  = r".log.txt"
    LOGEXT  = r".log"
    filename = pathlib.Path(datetime.now().strftime("%Y%m%d") + LOGEXT)
    # Check if file with today's date exists
    logfile = config.LOGDIR / filename
    # If it does not, create it.
    if not logfile.exists():
        logfile.touch()
    # open file in append mode
    with logfile.open(mode='a', encoding='utf-8', errors='xmlcharrefreplace') as handler:
        # print msg to the file-handler
        # print(datetime.now().strftime('%d/%m/%Y %I:%M:%S %p - '), 
        #     file=handler, end='')
        handler.write(datetime.now().strftime('%d/%m/%Y %I:%M:%S %p'))
        handler.write(' - ERROR - ')
        # handler.write(msg + '\n')
        print(msg, file=handler, end='\n')
        for m in msgs:
            # handler.write(m + '\n')
            print(m, file=handler, end='\n')



def enableButtons(a=None):
    # global button_generate, curItemId
    # global curItemId
    curItemId = ''
    print("type is ", type(tree.selection()), 
        "items are", tree.selection())
    # print("focused", [tree.focus(i) for i in range(len(tree.selection()))])
    tot_selected_items = len(tree.selection())
    if tot_selected_items > 0:
        # curItemId = tree.focus()
        curItemId = tree.selection()[0]
    print("event is", a, "and Item ID is", curItemId, 
        type(curItemId), len(curItemId))
    button_generate['state'] = tk.NORMAL
    item : list = tree.item(curItemId)['values']
    # print("tree:", tree.focus())
    print(item, "its length is", len(item))
    # if len(item) > 0:
    

    if tot_selected_items > 0:
        button_delete['state'] = tk.NORMAL
        button_view['state']    = tk.NORMAL
        if tot_selected_items == 1:
            filename         = pathlib.Path(item[-2]).stem
            uploadedfilename = pathlib.Path(item[-3]).name
            ogfilename.set(f'({uploadedfilename})')
            # if pathlib.Path(f'./data/reports/{filename}').is_dir():
            if (pathlib.Path(f'{config.REPORTSFOL}')/filename).is_dir():
                button_generate['text'] = "REGENERATE REPORTS"
                button_delete['text']  = "DELETE SURVEY"
                button_downall['state'] = tk.NORMAL
                button_viewsum['state'] = tk.NORMAL
                button_savecopy['state'] = tk.NORMAL
            else:
                button_generate['text'] = "GENERATE REPORTS"
                button_downall['state'] = tk.DISABLED
                button_view['state'] = tk.DISABLED
                button_viewsum['state'] = tk.DISABLED
                button_savecopy['state'] = tk.DISABLED
        else:
            uploadedfiles = []
            for itemId in tree.selection():
                filepath            = tree.item(itemId)['values'][-3]
                uploadedfilename    = pathlib.Path(filepath).name
                uploadedfiles.append(uploadedfilename)
            filelist = ", ".join(uploadedfiles)
            ogfilename.set(f'({filelist[:80]}' + ( "...)" 
                if len(filelist) >= 80 else ")" ))
            button_generate['text'] = "GENERATE ALL"
            button_delete['text']  = "DELETE ALL"
            button_downall['state'] = tk.DISABLED
            button_viewsum['state'] = tk.DISABLED
            button_savecopy['state'] = tk.DISABLED
    else:
        disableButtons()


def disableButtons(event=None):
    global curItemId
    button_generate.configure(state=tk.DISABLED, text="GENERATE REPORTS")
    button_downall.configure(state=tk.DISABLED, text="DOWNLOAD REPORTS")
    button_delete.configure(state=tk.DISABLED, text="DELETE SURVEY")
    button_view.configure(state=tk.DISABLED, text="VIEW REPORTS")
    button_viewsum.configure(state=tk.DISABLED)
    button_savecopy.configure(state=tk.DISABLED)
    ogfilename.set('')

    for item in tree.selection():
        tree.selection_remove(item)
    # curItemId = tree.focus()
    curItemId = ''
    print("disableButtons event:", tree.item(curItemId))


# Useless
def enterDate(event=None):
    # input_datetime.delete(0, tk.END)
    # input_datetime.insert(0, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    pass


def enterTime(event=None):
    return datetime.now().strftime("%H:%M:%S")
    pass


def Perform_File_Operations(data_sheet: str, survey_id: int, survey_name: str):
    # FILE = 'cas-copy.xlsx'
    # rootwindow.configure(cursor='wait')
    # rootwindow.config(cursor='watch')
    rootwindow.update_idletasks()
    # fname = "./data/raw/" + data_sheet
    fname = os.path.join(config.RAWFOL, data_sheet)
    if (data_sheet.endswith(('.xlsx', '.xlsm', '.xls'))):
        data = tsc.Parse_Excel_To_List(fname)
    elif (data_sheet.endswith('.csv')):
        data = tsc.Parse_Csv_To_List(fname)
    else:
        # If given unrecognized file format
        print("unrecognized file")
        return 0
    tscdata, studata, allquestions, rawscores = tsc.Tscores_And_Students_ImpData(data)
    print("INFO: parsed data")
    
    if (debug_setting):
        oldtscdata = tscdata[:]
        del tscdata
        tscdata = oldtscdata[:1]
        tscdata.append([71] * len(tscdata[0]))
    # pprint(studata) 
    # graphs = {'abcd': 'abcd1.png', 'nmn': 'nmn2.png', 'vxz': 'vxz3.png', 'efg': 'efg4.png', 'fgh': 'fgh5.png', 'hui': 'hui6.png', 'tkiof': 'tkiof7.png'}
    
    graphs = tsc.Plot_Graphs(tscdata, studata)
    # print(graphs)
        
    reportsdir = dutil.create_report_folder(data_sheet)
    codednames = rutil.generate_codenames_list(studata)
    # codednames = rutil.generate_codenames_list(studata, pick_department.get())
    print(f'{codednames=}')
    rutil.Create_Summary(reportsdir, tscdata, studata, codednames, 
                        allquestions , rawscores, survey_name)
    rutil.Create_All_Reports(reportsdir, tscdata, studata, graphs, 
                        survey_id, codednames)
    # rootwindow.config(cursor='')
    return 1


def center_window(window, width=300, height=200):
    # get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


def Create_Busy_Frame(parentwindow):
    # bsframe = tk.Tk(parentwindow)
    bsframe = tk.Toplevel(parentwindow)
    # bsframe.geometry("100x100+350+350")
    center_window(bsframe, 300, 100)
    bsframe.title("Wait...")
    label = tk.Label(bsframe, text="Generating reports...", anchor='center')
    # label.grid(column=0, row=0, sticky=tk.E + tk.W + tk.N + tk.S)
    label.pack(anchor='center', fill='both', expand=1)
    return bsframe
    pass


def Threaded_Generate_Action():
    print("thread crafting")
    treeobj = tree
    selected = [_ for _ in tree.selection()]
    try:
        t = threading.Thread(target=Generate_Action, args=[treeobj, selected])
        t.start()
    except Exception as e:
        print(traceback.format_exc())
        log_error(e, traceback.format_exc())


def Generate_Action(tree: tk.ttk.Treeview, treeselection: list):
    
    busyframe = Create_Busy_Frame(rootwindow)
    busyframe.update()
    busyframe.grab_set()
    rootwindow.withdraw()

    # SQLite objects created in a thread can only be used in that same thread
    try:
        con1 = sqlite3.connect(config.DB)
        cur = con1.cursor()
        # print("Slected items length = ", len(tree.selection()))
        print("Slected items length = ", len(treeselection))
        print("Type of tk.tree", type(tree))
        for treeItemId in treeselection:
            # print( treedata := tree.item(tree.focus())['values'] )
            print( treedata := tree.item(treeItemId)['values'] )
            item_id = int(treedata[-1])
            survey_name = treedata[0]
            # print(item_id)
            fname = cur.execute("""SELECT file FROM tblSurveySheets WHERE id=?""", 
                                (str(item_id),) ).fetchone()[0]
                                # (str((item_id).fetchone()[0]), ))
            # con.close()
            # fname = "./data/raw/" + fname
            print(fname)
            print()
            # try:
            print("Success? \t",
                Perform_File_Operations(fname, item_id, survey_name))
    except Exception as e:
        # logging.error(traceback.format_exc())
        # log_error(traceback.format_exc())
        # log_error(str(e))
        log_error(e, traceback.format_exc())
        print("ERRORRRR: ", e)
        messagebox.showerror("Error", "Unable to generate reports.")
        raise e
    finally:
        con1.close()
        busyframe.grab_release()
        rootwindow.deiconify()
        busyframe.destroy()
        messagebox.showinfo("Done", "Reports generated!")
        disableButtons()


def Copy_All_Reports():
    """
        Ask directory
        os.copy private directory to given dir path
    """
    dest    = filedialog.askdirectory(parent=rootwindow,
                                 initialdir='/',
                                 title="Please select a folder:")
    data    = tree.item(tree.focus())['values']
    file    = pathlib.Path(data[-2]).stem

    # if(pathlib.is_dir(directory:=f'./data/reports/{file}')):
    # if pathlib.Path(directory:=f'./data/reports/{file}').is_dir():
    if pathlib.Path(directory:=os.path.join(config.REPORTSFOL, file)).is_dir():
        for file in os.listdir(directory):
            # srcpath = os.path.join(directory, file)
            srcpath = pathlib.Path(directory) / pathlib.Path(file)
            file = pathlib.Path(file)
            # srcfile = pathlib.Path(directory) / file
            
            if (pathlib.Path(dest) / file).exists():
                count = 1
                while (pathlib.Path(dest) / (file.stem + f" ({count})" + file.suffix)).exists():
                    count += 1
                shutil.copy2(srcpath, (pathlib.Path(dest) / (file.stem + f" ({count})" + file.suffix)))
            else:
                shutil.copy2(srcpath, dest)
                # shutil.copy2(srcfile, dest)
        
        dest = dest.translate({ord('/'):'\\'})
        print("Download finished!")
        print(dest)
        # messagebox.showinfo("Download complete!", "Download complete!!")
        answer = messagebox.askyesno("Download complete", 
                    "Would you like to open the folder?")
        if (answer == True):
            # subprocess.Popen(f"explorer.exe \"{dest}\"", shell=True)
            subprocess.run(["explorer", dest])


def clearInputs():
    input_filepath.configure(state='normal')
    input_surveyname.delete(0, tk.END)
    input_filepath.delete(0, tk.END)
    input_time.delete(0, tk.END)
    input_filepath.configure(state='readonly')


def Upload_Action():
    global inputs
    
    date = f"{pick_day.get()} {pick_month.get()} {pick_year.get()} {timevalue.get()}"

    if debug_setting:
        # given_timestamp = parser.parse(input_datetime.get() or "01/01/2022")
        given_timestamp = parser.parse(date or "01/01/2022")
        rawfilename  = input_filepath.get() or 'cas-sample-score-sheet.xlsx'
    else:
        rawfilename  = input_filepath.get()
        if rawfilename.strip() == '':
            messagebox.showerror("Error", "Choose a file before uploading!")
            return
        try:
            # given_timestamp = parser.parse("00:00")
            # given_timestamp = parser.parse(input_datetime.get())            
            print(date)
            given_timestamp = parser.parse(date)
        #except parser.ParserError:
        except Exception:
            messagebox.showerror("Error", 
                "Given datetime format is not correct!\n" +\
                "Example: 01/03/22 3:30pm")
            return

    # rawfilename = '' 
    # rawfilename = dutil.upload_raw_file(input_filepath.get()) # with extension
    # print(f'{ogfilename.get()=}')
    filename = pathlib.Path(rawfilename).stem
    inputs = [
        input_surveyname.get().strip() or filename,
        given_timestamp,
        pick_institute.get().strip(), 
        pick_department.get().strip(),
        # This second rawfilename will be modified in Upload_Report() 
        # function, so we need two of these
        rawfilename,
        rawfilename, 
        datetime.now()
    ]
    
    Upload_Report(inputs)
    updateView()
    clearInputs()
    print(inputs)


def Upload_Report(data: list):

    dutil.create_raw_folder()
    cryptic_filename = dutil.upload_to_raw_folder(data[-2])
    data[-2] = cryptic_filename

    con1 = con or sqlite3.connect(config.DB)
    cur = con1.cursor()
    cur.execute("""INSERT INTO 
        tblSurveySheets(survey_name, survey_time, institute, department, 
        ogfile_path, file, upload_time) VALUES(?,?,?,?,?,?,?)""", data)
        # tblSurveySheets()
    rows = cur.fetchall()    
    print("rows: ", rows)
    con1.commit()
    # con.close()


def Change_Sort_Order(event=None):
    global order
    order = not order
    button_order.configure(text = f"{'^' if order else 'v'}")
    updateView()
    disableButtons()


def Clear_Filter(event=None):
    input_filter.delete(0, tk.END)
    updateView()


def updateView(event=None):
    global order
    filtertxt = input_filter.get()
    filtertxt = f"%{filtertxt}%"
    # Since both sortorder and order variables do not get data from text-field
    # so string interpolation with them is secure.
    sortorder = str(comboBoxMap[pick_order.get()])
    # order     = 'ASC' if 

    # To remove all items from table
    for item in tree.get_children():
       tree.delete(item)

    # con1 = sqlite3.connect(config.DB)
    print(con)
    con1 = con or sqlite3.connect(config.DB)
    cur1 = con1.cursor()
    cur1.execute("""SELECT * FROM tblSurveySheets WHERE survey_name LIKE ? 
        or institute LIKE ? or department LIKE ? COLLATE NOCASE ORDER BY """ +
        F"{sortorder} {'ASC' if order==1 else 'DESC'}", (filtertxt,)*3)
    # cur1.execute("""SELECT * FROM tblSurveySheets ORDER BY ? DESC""",
    #         (sortorder,))
    # cur1.execute("""SELECT * FROM tblSurveySheets ORDER BY department""")
    # cur1.execute("SELECT * FROM tblSurveySheets ORDER BY ? DESC", ('survey_name',))
    rows = cur1.fetchall()

    for row in rows:
        # print("current:", row, row[1:3])
        # name = f"({row[3] if row[3]!='' else 'N/a'}{'-'+str(row[4]) 
        # if row[4]!='' else ''}) {row[1]}"
        displayname = f"({row[3] if row[3] not in ('', '...') else 'Unspecified'}" + \
                    f"{' '+str(row[4]) if row[4]!='' else ''}) {row[1]}"
        giventime   = parser.parse(row[2])
        uploadtime  = parser.parse(row[-1])
        ogpath      = row[-3]
        filename    = row[-2]
        primaryid   = int(row[0])
        giventime   = giventime.strftime("%d-%m-%Y %H:%M")
        uploadtime  = uploadtime.strftime("%d-%m-%Y %H:%M")
        tree.insert("", tk.END, values=(displayname, giventime, uploadtime,
                                        ogpath, filename, primaryid))
    # con1.close()

    if debug_setting:
        print("updating... ")
        # pprint(rows)
        # print("...... Rows", uploadtime)
        # print("......", sortorder)
        print("..updated!")


def Download_Selected_Reports(treeobject, pdfdir, parentwindow):
    files = []
    for itemid in treeobject.selection():
        print(treeobject.item(itemid)['values'][-1])
        files.append( treeobject.item(itemid)['values'][-1] )
    dest = filedialog.askdirectory(parent=parentwindow,
                                    initialdir='/',
                                    title="Please select a folder:")
    # srcdir = pathlib.Path(f'./data/reports/{pdfdir}')
    srcdir = pathlib.Path(config.REPORTSFOL) / pdfdir
    print(srcdir)
    if srcdir.is_dir():
        for file in files:
            if (srcfile := pathlib.Path(srcdir)/file).exists():
                shutil.copy2(srcfile, dest)
        print("Download finished!")
        print(dest)
        # messagebox.showinfo("Download complete!", "Download complete!!")
        answer = messagebox.askyesno("Download complete", 
                    "Would you like to open the folder?")
        if (answer == True):
            # subprocess.Popen(f"explorer.exe \"{dest}\"", shell=True)
            dest = dest.translate({ord('/'):'\\'})
            subprocess.run(["explorer", dest])
    else:
        messagebox.showerror("Not found", "Files do not exist.")


def View_Reports():
    """ for all items in tree.selection():
            Create child frame
            Add treeview and 'Download selected' button in frame
            Fetch details for selected report from tblSurveyReports using pk from tblSurveySheets
            Append details to student details treeview
    """
    # DONE: TODO: Add a button to View Summary sheet
    # REJECTED PROPOSAL: TODO: Add a button to Download Summary sheet

    TIP = "Use mousewheel to scroll vertically, and use MouseWheel with SHIFT key to scoll horizontally." + \
        "\n" + "Hold CTRL and Left-click to select items.\n" +\
        "Use SHIFT+Leftclick to select multiple items in sequence." +\
        "\n\n" + "Note: If files in selected folder have same name as download files then these files will overwrite them."
        # "\n\n" + "*If downloaded files have same name as file in destination folder then those files will be overwritten."
    FIELD_ID    = ('cname', 'totpa', 'sname', 'semail', 'mobile', 'age',
        'gender', 'stream', 'year', 'filename')
    FIELDS_NAME = ('Codename', 'Tot. Problem Areas', 'Student name', 
        'Email', 'Mobile number', 'Age', 'Gender', 'Department', 
        'Year', 'FILE')
    SHOW_COLS = tuple(range(len(FIELD_ID) - 1))
    
    def openFile(treeobj, item: list):
        folder_name = pathlib.Path(item[-2]).stem

        # print("execute subprocess to open pdf", "({})".format(folder_name))
        # subprocess.Popen(
        # 'start ./data/reports/' + folder_name + '/' + tree_studentsinfo.item(
        #     tree_studentsinfo.selection()[0]
        # )['values'][-1], shell=True )
        print(folder_name, treeobj.focus(), treeobj.selection())
        for itemId in treeobj.selection():
            pdf_file = treeobj.item(itemId)['values'][-1]
            # pdf_file = "generated-report-sample-1.pdf"

            # pdf_path = '"{}"'.format(str(pathlib.Path(config.REPORTSFOL) / folder_name / pdf_file))

            pdf_path = '{}'.format(str(pathlib.Path(config.REPORTSFOL) / folder_name / pdf_file))
            # pdf_path = r"C:\Users\kusha\Documents\Acrocare project files\\" + pdf_file

            # print("Path", '"{}"'.format(
            #     str(pathlib.Path(config.REPORTSFOL) / folder_name / pdf_file)))
            # subprocess.Popen('start "{}"'.format(
            # subprocess.Popen('"{}"'.format(
            #     str(pathlib.Path(config.REPORTSFOL) / folder_name / pdf_file)), 
                # shell=True)
            print(f"{pdf_path=}")
            subprocess.Popen([pdf_path], shell=True)
            # subprocess.run([pdf_path], shell=True)
            # subprocess.call([pdf_path], shell=True)
    
    def updateStudentView(treeobj, surveyid, filtertxt=""):
        con1 = con or sqlite3.connect(config.DB)
        cur = con1.cursor()
        filtertxt = '%'+filtertxt+'%'
        cur.execute("""SELECT student_codename, tot_problem_areas, 
            student_name, email, mobile_number, age, gender, stream, 
            year, report_file FROM tblSurveyReports WHERE survey_id = ?
            and (student_codename LIKE ? or tot_problem_areas LIKE ?  
                or student_name LIKE ? or stream LIKE ? COLLATE NOCASE)
            -- student_name LIKE ? or student_codename LIKE ? or
            -- institute LIKE ? or stream LIKE ? COLLATE NOCASE """ , 
            (surveyid,) + (filtertxt,)*4 + ())
        # cur.execute("""SELECT student_name
            # FROM tblSurveyReports WHERE survey_id = ?""", (surveyid,))
        rows = cur.fetchall()
        print("fetched rows:", rows)

        
        for item in treeobj.get_children():
            treeobj.delete(item)

        for row in rows:
            print("STUDENT INFO", row)
            PA_INDEX = 1
            # total_pa = len(row[PA_INDEX].split(',')) if row[PA_INDEX].strip() != '' else 0
            # print("PA DATA ", row[2].split(','), len(row[2].split(',')))
            # tree.insert("", tk.END, values=[str(i) for i in row])
            # treeobj.insert("", tk.END, values=[*row])
            # treeobj.insert("", tk.END, values=tuple(row))
            # treeobj.insert("", tk.END, values=(*row[:PA_INDEX], total_pa, *row[PA_INDEX+1:]))
            treeobj.insert("", tk.END, values=row)
        # treeobj.bind('<<TreeviewOpen>>', lambda e: openFile(treeobj))

    for treeItemId in tree.selection():
        item = tree.item(treeItemId)['values']
        surveyid = item[-1]

        con1 = con or sqlite3.connect(config.DB)
        cur = con1.cursor()
        cur.execute("""SELECT file FROM tblSurveySheets WHERE id = ?""", 
            (surveyid,))
        reportsdir = pathlib.Path( cur.fetchone()[0] ).stem


        # reportsframe = tk.Toplevel()
        reportsframe = tk.Toplevel(rootwindow)
        BUTTON_WIDTH = 25
        tree_studentsinfo = ttk.Treeview(reportsframe, columns=FIELD_ID,
                                show='headings', displaycolumns=SHOW_COLS)
        label_info = tk.Label(reportsframe, text=TIP, justify=tk.LEFT, 
                            anchor='w')
        frame_filefilter = tk.Frame(reportsframe)
        label_filefilter = tk.Label(frame_filefilter, text="Filter")
        input_filefilter = tk.Entry(frame_filefilter)
        button_downselected = tk.Button(reportsframe, anchor='center', 
            text="Download selected reports", width=BUTTON_WIDTH, 
            command=lambda: Download_Selected_Reports(tree_studentsinfo, 
                reportsdir, reportsframe)
            )
        button_openselected = tk.Button(reportsframe, anchor='center', 
            text="Open selected reports", width=BUTTON_WIDTH, 
            command=lambda: openFile(tree_studentsinfo, item)
            )
        
        for fid, ftitle in zip(FIELD_ID, FIELDS_NAME):
            # tree_studentsinfo.heading(fid, text=ftitle, anchor='center')
            tree_studentsinfo.heading(fid, text=ftitle, anchor='w')
            tree_studentsinfo.column(fid, stretch=True, minwidth=30, anchor='w')
        for fid in FIELD_ID[:2]:
            tree_studentsinfo.column(fid, stretch=False, width=150)
        for fid in FIELD_ID[-5:]:
            tree_studentsinfo.column(fid, stretch=False, width=100)

        # tree_studentsinfo.grid(column=0, row=0, sticky=tk.N+tk.W+tk.E+tk.S)
        # tree_studentsinfo.pack(side='left')
        # button_downselected.pack(side='right', anchor='n')
        # tree_studentsinfo.column('email', width=400)
        tree_studentsinfo.pack(expand=1, fill='both')
        label_info.pack(side='left', anchor='w', ipadx=PX)
        input_filefilter.pack(side='right', anchor='n')
        label_filefilter.pack(side='right', anchor='n')
        frame_filefilter.pack(side='top', anchor='e', pady=PY, padx=PX)
        button_openselected.pack(side='top', anchor='e', pady=PY, padx=PX)
        button_downselected.pack(side='top', anchor='e', pady=PY, padx=PX)

        updateStudentView(tree_studentsinfo, surveyid)

        # tree_studentsinfo.bind('<Double-1>', lambda e: subprocess.run(
        #     'start', './data/reports/' + foldername + tree_studentsinfo.item(
        #         tree_studentsinfo.selection()[0]
        #     )['values'][-1] ))
                        # tree_studentsinfo.focus()

        # tree_studentsinfo.bind('<<TreeviewOpen>>', lambda e: openFile(tree_studentsinfo, item))
        tree_studentsinfo.bind('<Double-1>', lambda e: openFile(tree_studentsinfo, item))
        # tree_studentsinfo.bind('<Button-1>', lambda e: print(tree_studentsinfo.item(tree_studentsinfo.focus())))
        input_filefilter.bind('<KeyRelease>', lambda e: updateStudentView(
            tree_studentsinfo, surveyid, filtertxt=input_filefilter.get()))


def Delete_Reports():
    """ for all items in tree.selection():
            fetch file name from either treeview or config.DB
            if folder(reports/file-name).exists
                empty it then delete it
            try:
                delete folder(raw)/filename
            finally:
                remove item from treeview as well
            delete row from config.DB table tblSurveySheets

            delete from config.DB as well
    """
    selected_items = tree.selection()
    answer = messagebox.askyesno("Confirm deletion?", "Do you want to delete this survey and associated reports?")
    print(answer)
    if answer == True:
        # print(tree.selection())
        print(selected_items)
        # for itemid in tree.selection():
        for itemid in selected_items:
            surveyid = tree.item(itemid)['values'][-1]
            con1 = con or sqlite3.connect(config.DB)
            cur = con1.cursor()
            cur.execute("""SELECT file from tblSurveySheets WHERE id=?""", 
                (surveyid,))
            filename = pathlib.Path(cur.fetchone()[0])
            # if (targetdir:=pathlib.Path(f'./data/reports/{filename.stem}')).is_dir():
            if (targetdir:=pathlib.Path(config.REPORTSFOL)/filename.stem).is_dir():
                # RMDIR -S DIR
                # shutil.rmtree(f'./data/reports/{filename.stem}')
                shutil.rmtree(targetdir)
                pass
            # if (targetfile:=pathlib.Path(f'./data/raw/{filename}')).exists():
            if (targetfile:=pathlib.Path(config.RAWFOL)/filename).exists():
                # DEL filename
                targetfile.unlink()
                pass
            cur.execute("""DELETE FROM tblSurveySheets WHERE id=?""",
                (surveyid,))
            con1.commit()
            tree.delete(itemid)
            print("Deletion done!")


def Browse_Files() -> str:

    input_filetypes = [
        ('Excel files', '*.xlsx *.xlsm *.xls'),
        ('CSV files', '*.csv'),
        ('All files', '*.*'),
    ]

    filename = filedialog.askopenfilename(parent=rootwindow,
                                        initialdir=os.getcwd(),
                                        title="Please select a file:",
                                        filetypes=input_filetypes)

    input_filepath.configure(state=tk.NORMAL)
    input_filepath.delete(0, tk.END)
    input_filepath.insert(0, filename)
    input_filepath.configure(state='readonly')
    return filename


def openSubprocess(e=None):
    print(itemId := tree.selection()[0])
    data : list = tree.item(itemId)['values']
    file : str  = data[-2]
    # sts = subprocess.Popen(f"\"{os.getcwd()}\\data\\raw\\{file}\"", shell=True)
    sts = subprocess.Popen(f"\"{config.RAWFOL}\\{file}\"", shell=True)
    # print("type(sts)", type(sts))
    return sts


def Open_Associated_Summary():
    treeItemId  = tree.focus()
    treestorage = tree.item(treeItemId)['values']
    survey_name = treestorage[0]
    outputfol   = pathlib.Path(treestorage[-2]).stem
    reportspath = pathlib.Path(config.REPORTSFOL) / outputfol
    if (reportspath.exists()):
        summary_sheet_path = reportspath / rutil.getsummaryname(survey_name)
        print(f'{summary_sheet_path=}')
        print(str(summary_sheet_path)) 
        # subprocess.run(['start', 'excel.exe',f'"{str(summary_sheet_path)}"'], shell=True)
        subprocess.Popen(f'start excel.exe "{str(summary_sheet_path)}"', shell=True)


def Copy_Summary():
    dest    = filedialog.askdirectory(parent=rootwindow,
                                initialdir='/',
                                title="Please select a folder:")
    treedata        = tree.item(tree.focus())['values']
    selecteditemid  = tree.focus()
    outputfol       = pathlib.Path(treedata[-2]).stem
    survey_name     = treedata[0]
    reportspath     = pathlib.Path(config.REPORTSFOL) / outputfol
    if pathlib.Path(directory:=os.path.join(config.REPORTSFOL, outputfol)).is_dir():
        file        = rutil.getsummaryname(survey_name)
        srcpath     = pathlib.Path(directory) / file
        destpath    = pathlib.Path(dest) / file
        # srcfile = pathlib.Path(directory) / file
        
        # if (pathlib.Path(dest) / file).exists():
        if destpath.exists():
            # print("Exists", pathlib.Path(dest) / file, end=" ")
            # print("Exists", (pathlib.Path(dest) / file).exists())
            # print("Exists", destpath.exists(), destpath)
            count = 1
            while (pathlib.Path(dest) / (file.stem + f" ({count})" + file.suffix)).exists():
                count += 1
            shutil.copy2(srcpath, (pathlib.Path(dest) / (file.stem + f" ({count})" + file.suffix)))
        else:
            shutil.copy2(srcpath, dest)
            # shutil.copy2(srcfile, dest)
        
        dest = dest.translate({ord('/'):'\\'})
        print("Summary sheet copies to desination!")
        print(dest)
        # messagebox.showinfo("Download complete!", "Download complete!!")
        answer = messagebox.askyesno("Download complete", 
                    "Would you like to open the folder?")
        if (answer == True):
            # subprocess.Popen(f"explorer.exe \"{dest}\"", shell=True)
            subprocess.run(["explorer", dest])


def updateDeptBox(e=None):
    insti = pick_institute.get()
    pick_department['values']=college.INST_DEPT_MAP.get(insti, (COMBINED, ))
    pick_department.current(0)


def openinfowindow(parentwindow):
    FALLBACK_INFO = """
Developed by:

* Ashutosh Dubey\t\t(IMCA 2021 batch)
* Durva Shinde\t\t(IMCA 2021 batch)
* Kushagra Mehrotra\t(IMCA 2019 batch) 
\t\t\t\t
Student at Acropolis FCA department under guidance of \t\t
Prof. Nitin Kulkarni.

For help and assistance email at: 
kushagramehrotra.ca19@acropolis.in
"""
    infowindow = tk.Toplevel(parentwindow)
    info = FALLBACK_INFO
    label_contributors = tk.Label(infowindow, text=info, justify='left')
    label_contributors.pack(ipadx=PX)
    


def createFooter(parentwindow):
    INFO_DEPT       = """Made by students at FCA department"""
    label_madeby    = tk.Label(parentwindow, text=INFO_DEPT)
    button_info     = tk.Button(parentwindow, text="?", 
                        command=lambda: openinfowindow(parentwindow))

    button_info.pack(side='right', ipadx=PX)
    label_madeby.pack(side='right', padx=PX)

    return button_info, label_madeby


if __name__ == '__main__':
    """
    TODOs
    TODO: File path should look like "C/users/kusha/Docu...cas-copy.xlsx", also replace foward slash with backslash
    TODO: Add v-scrollbar to treeview
    TODO: Add auto-hide H-scrollbar to treeview
    TODO: (IN THE END) Convert this into an asynchronous program
    TODO: possible pdf-generation speed-up can be achieved by replacing images in pdf with html content

    DONE:   TODO: (BUG) Fix cursor doesn't revert to normal when Generate call finishes.
    DONE:   TODO: Replace input_datetime with new dropdown input everywhere.
    DONE:   TODO: Create a date and time drop-down widgets in a separate frame
    DONE:   TODO: Add radio button widget for ascending and descending order
    DONE:   TODO: When reports are generating freeze the main window and create a progress bar pop up
    DONE:   TODO: (ref. reportutility.py) Delete records when 'regenerating reports' and then insert
    DONE:   TODO: provide recommendations according to problem areas
    DONE:   TODO: Code incomplete functions. ie. View_Reports and Delete_Reports
 
    """

    # setup_logging(file=config.LOGFILE, enc='utf-8')

    # SQL interface
    if not os.path.exists(config.DBLOC):
        os.mkdir(config.DBLOC)
    con = sqlite3.connect(config.DB)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()
    # cur.execute("""DROP TABLE IF EXISTS tblSurveySheets""")
    # cur.execute("""DROP TABLE IF EXISTS tblSurveyReports;""")
    cur.execute("""CREATE TABLE IF NOT EXISTS tblSurveySheets(
        id INTEGER PRIMARY KEY,
        survey_name VARCHAR,
        survey_time TIMESTAMP,
        institute VARCHAR,
        department VARCHAR,
        ogfile_path VARCHAR,
        file VARCHAR,
        upload_time TIMESTAMP)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tblSurveyReports(
        id INTEGER PRIMARY KEY,
        survey_id INT REFERENCES tblSurveySheets(id) ON DELETE CASCADE,
        student_codename VARCHAR,
        student_name VARCHAR,
        email VARCHAR,
        guardian_name VARCHAR,
        age INT,
        gender CHAR(10),
        mobile_number CHAR(15),
        institute CHAR(10),
        stream CHAR(20),
        year CHAR(10),
        monthly_family_income VARCHAR,
        tot_problem_areas INT,
        problem_areas VARCHAR,
        report_file VARCHAR
        )""")

    # GUI (Tkinter) interface
    rootwindow = tk.Tk()
    rootwindow.title("Acrocare")
    rootwindow.resizable(False, False)

    # frame_datetime = ttk.LabelFrame(rootwindow, text="Select date of survey*")
    frame_datetime = tk.Frame(rootwindow, width=FIELD_SIZE)

    # institute_values = ('AITR', 'AIMSR', 'AIPER', 'AFMR', 'FCA', 'AIL', 'AID')
    institute_values = college.institutes
    department_value = college.INST_DEPT_MAP.get(institute_values[0], (COMBINED,))
    sort_keys = ('Upload Time (Default)', 'Survey Name', 'Survey Time',
                        'Institute', 'Department')
    db_fields   = ('upload_time', 'survey_name', 'survey_time', 
                        'institute', 'department')
    comboBoxMap = dict(zip(sort_keys, db_fields))
    timevalue   = tk.StringVar()
    timevalue.set('')

    label_filepath  = tk.Label(rootwindow, text="Browse input file*", 
                            anchor='w')
    label_surveyname= tk.Label(rootwindow, text="Survey name", anchor='w')
    # label_datetime  = tk.Label(frame_datetime, 
    #                    text="Enter date and giventime of survey", anchor='w')
    label_date      = ttk.LabelFrame(frame_datetime, 
                        text="Pick date of survey:*", width=FIELD_SIZE//2)
    label_time      = ttk.LabelFrame(frame_datetime, 
                        text="Time of survey (optional):")
    label_institute = tk.Label(rootwindow, text="Institute", anchor='w')
    label_department= tk.Label(rootwindow, text="Department", anchor='w')

    input_filepath  = tk.Entry(rootwindow, width=FIELD_SIZE)
    input_surveyname= tk.Entry(rootwindow, width=FIELD_SIZE)
    # input_datetime  = tk.Entry(frame_datetime, width=FIELD_SIZE)
    pick_day        = ttk.Combobox(label_date, values=DATERANGE, 
        state='readonly', width='3')
    pick_month      = ttk.Combobox(label_date, values=MONTHRANGE, 
        state='readonly', width='4')
    pick_year       = ttk.Combobox(label_date, values=YEARRANGE, 
        state='readonly', width='5')
    input_time      = tk.Entry(label_time, textvariable=timevalue)
    pick_institute  = ttk.Combobox(rootwindow, width=FIELD_SIZE-3,
        text="Institute", values=institute_values, state='readonly')
    # input_department= tk.Entry(rootwindow, width=FIELD_SIZE)
    pick_department = ttk.Combobox(rootwindow, width=FIELD_SIZE-3, 
        text="Department", values=department_value, state='readonly')
    
    button_browse   = tk.Button(rootwindow,
                        text = "Browse",
                        command = Browse_Files)

    button_upload = tk.Button(rootwindow, 
                        text = 'Upload form',
                        command=Upload_Action) 

    # txt.grid(column=0, row=1, sticky=tk.W)

    # button_browse.grid(column=1, row=4, sticky=tk.W+tk.E, pady=PX, padx=PX)
    # button_browse.update()
    # print(button_browse.winfo_width())

    label_filepath.grid(column=0, row=0, pady=(PY,0), sticky=tk.W+tk.E)
    input_filepath.grid(column=0, row=1, sticky=tk.W+tk.E)
    button_browse.grid(column=0, row=2, pady = (PX, 0), padx=PX, 
        sticky=tk.W+tk.E)

    label_surveyname.grid(column=0, row=3, pady=(PY,0), sticky=tk.W+tk.E)
    input_surveyname.grid(column=0, row=4, sticky=tk.W+tk.E)

    frame_datetime.grid(column=0, row=5, rows=2, pady=(PY*2, 0), 
        sticky=tk.W+tk.E)
    # label_datetime.grid(column=0, row=6, pady=(PY,0), sticky=tk.W)
    # input_datetime.grid(column=0, row=7, sticky=tk.W)
    # frame_datetime.update()
    label_date.pack(side='left', expand=1, fill='y')
    label_time.pack(side='right', expand=1, fill='y')
    pick_day.pack(side='left', padx=(PX//2), pady=PY)
    pick_month.pack(side='left', padx=(PX//2), pady=PY)
    pick_year.pack(side='left', padx=(PX//2), pady=PY)
    input_time.pack(side='left', padx=PX, pady=PY)

    pick_day.current(0)
    pick_month.current(0)
    pick_year.current(0)

    label_institute.grid(column=0, row=7, pady=(PY,0), sticky=tk.W+tk.E)
    pick_institute.grid(column=0, row=8, sticky=tk.W+tk.E)
    pick_institute.current(0)

    label_department.grid(column=0, row=9, pady=(PY,0), sticky=tk.W+tk.E)
    pick_department.grid(column=0, row=10, sticky=tk.W+tk.E)
    pick_department.current(0)
    # input_department.grid(column=0, row=13, sticky=tk.W+tk.E)
    # input_filepath.configure(width=FIELD_SIZE)
    # input_filepath.insert(0, "Provide an input file")
    button_upload.grid(column=0, row=13, pady=PX, padx=PX, sticky=tk.W+tk.E)


    input_filepath.insert(0, "")
    input_filepath.configure(state='readonly')
    
    # hor_sep = ttk.Separator(rootwindow, orient=tk.VERTICAL)
    # hor_sep.grid(column=1, row=1, sticky=tk.N+tk.S, rowspan=13 )
    # print(rootwindow.winfo_height())
    # print(dir(rootwindow))
    # print(dir(rootwindow.winfo_children()[0]))
    # print((rootwindow.winfo_children()))
    for widget in rootwindow.winfo_children():
        widget.grid_configure(padx=PX, ipady=PY)
        


    rootwindow.update()
    ttk.Separator(rootwindow,
                orient=tk.VERTICAL, 
                style='TSeparator',
                cursor='man',
                ).grid(column=1, row=0, sticky=tk.N+tk.S, rowsp=300)
                # ).place(x=20, y=20, relheight=1)


    tree = ttk.Treeview(rootwindow, columns=("surveyname","date",
            "uploadtime","ogfilepath","filename","pk"), show='headings', 
            displaycolumns=(0,1,2))
    tree.heading("surveyname",  text="Survey name", anchor="w")
    tree.heading("date",        text="Survey Timestamp", anchor="center")
    tree.heading("uploadtime",  text="Upload Timestamp", anchor="center")
    tree.heading("pk",          text="ID", anchor="w")
    tree.column("surveyname", stretch=True, minwidth=250)
    tree.column("date",         stretch=True, minwidth=100, width=150, 
                anchor='center')
    tree.column("uploadtime",   stretch=True, minwidth=100, width=200, 
                anchor='center')
    tree.rowconfigure(0, weight=1)
    tree.grid(column=3, row=1, rowspan=14, columns=4, 
                sticky=tk.N+tk.W+tk.E+tk.S, padx=PX, pady=PY)
    
    ogfilename = tk.StringVar()
    ogfilename.set('')

    label_associatedfile = tk.Label(rootwindow, textvariable=ogfilename, 
                                    anchor='w')
    label_sortby    = tk.Label(rootwindow, text="Sort by:", anchor='w')
    pick_order      = ttk.Combobox(rootwindow, text="sort_by", 
        values=sort_keys, state='readonly')
    label_filter    = tk.Label(rootwindow, text="Filter:", anchor='w')
    input_filter    = tk.Entry(rootwindow, width=17)

    button_generate = tk.Button(rootwindow, 
                        text = 'GENERATE REPORTS',  state='disabled',
                        command=Threaded_Generate_Action)
    button_view     = tk.Button(rootwindow, 
                        text = 'VIEW REPORTS',      state='disabled',
                        command=View_Reports)
    button_delete   = tk.Button(rootwindow, 
                        text = 'DELETE SURVEY',     state='disabled',
                        command=Delete_Reports)
    button_downall  = tk.Button(rootwindow, 
                        text = 'DOWNLOAD REPORTS',  state='disabled',
                        command=Copy_All_Reports)
    button_viewsum  = tk.Button(rootwindow,
                        text = 'VIEW SUMMARY',      state='disabled',
                        command=Open_Associated_Summary)
    button_savecopy = tk.Button(rootwindow,
                        text = 'SAVE A COPY OF \nSUMMARY', state='disabled',
                        command=Copy_Summary)
    button_clearbox = tk.Button(rootwindow,
                        text = 'clear filter', command=Clear_Filter)
    button_order    = tk.Button(rootwindow,
                        text = f"{'^' if order else 'v'}", 
                        command=Change_Sort_Order)

    button_generate.grid(column=7, row=2, sticky=tk.E+tk.W, padx=PX)
    button_view.grid(column=7, row=3, sticky=tk.E+tk.W, padx=PX)
    button_delete.grid(column=7, row=4, sticky=tk.E+tk.W, padx=PX)
    button_downall.grid(column=7, row=5, sticky=tk.E+tk.W, padx=PX)
    button_viewsum.grid(column=7, row=6, sticky=tk.E+tk.W, padx=PX)
    button_savecopy.grid(column=7, row=7, sticky=tk.E+tk.W, padx=PX)

    label_associatedfile.grid(column=3, row=15, columns=4, 
                            sticky=tk.N+tk.W+tk.E+tk.S, padx=PX, pady=PY)
    label_sortby.grid(column=7, row=12, sticky=tk.W, padx=PX)
    pick_order.grid(column=7, row=13, sticky=tk.W, padx=PX)
    pick_order.current(0)
    button_order.grid(column=7, row=12, sticky=tk.E, padx=PX, ipadx=PX/2)
    
    input_filter.grid(column=7, row=1, sticky=tk.E, padx=PX)
    label_filter.grid(column=7, row=1, sticky=tk.W, padx=PX)
    button_clearbox.grid(column=7, row=0, sticky=tk.E, padx=PX, pady=0)

    ttk.Separator(rootwindow,
                orient=tk.HORIZONTAL, 
                style='TSeparator',
                cursor='man',
                ).grid(column=0, row=998, columns=999, sticky=tk.E+tk.W)


    frame_footer = tk.Frame(rootwindow)
    frame_footer.grid(row=999, column=0, columns=999, sticky=tk.E+tk.W)
    # binfo, lmadeby = createFooter(frame_footer)
    createFooter(frame_footer)

    tree.bind('<ButtonRelease-1>', enableButtons)
    # tree.bind('<Up>', enableButtons)
    # tree.bind('<Down>', enableButtons)
    # tree.bind('<KeyRelease>', enableButtons)
    tree.bind('<<TreeviewSelect>>', enableButtons)
    tree.bind('<FocusOut>', disableButtons)
    # tree.bind('<Double-1>', openSubprocess)
    tree.bind('<<TreeviewOpen>>', openSubprocess)
    input_filter.bind('<Return>', updateView)
    # input_filter.bind('<KeyPress>', updateView)
    input_filter.bind('<KeyRelease>', updateView)
    # input_datetime.bind('<Triple-Button-1>', enterDate)
    input_time.bind('<Triple-Button-1>', 
                    lambda e:timevalue.set(enterTime()))
    # input_filter.bind('<Escape>', Clear_filter)
    # pick_order.bind("<FocusIn>", updateView)
    pick_order.bind("<<ComboboxSelected>>", updateView)
    pick_institute.bind("<<ComboboxSelected>>", updateDeptBox)

    """ Test 500 records upload to DB"""
    # bf = Create_Busy_Frame(rootwindow)
    # bf.update()
    # for i in range(500):
    #     testinp = [
    #         str(i),
    #         parser.parse(f"{(i%31)+1} Jan 2000"),
    #         'dummy-institute', 
    #         'mock-dept',
    #         './cas-copy.xlsx',
    #         './cas-copy.xlsx', 
    #         datetime.now()
    #     ]
    #     Upload_Report(testinp)
    updateDeptBox()
    updateView()
    rootwindow.mainloop()
    # con.commit()
    con.close()
    print("Connection closed!")
