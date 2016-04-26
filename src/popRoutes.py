'''
Popular Route Report
Here the TreeView widget is configured as a multi-column listbox
Retrieves popular route report and converts it into a format recognized
by the treebuilding fucntion
then displays month, list of train#, list of reservations

'''
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import pymysql
from dbhook import *


class popRoutes(object):
	"""use a ttk.TreeView as a multicolumn ListBox"""
	def __init__(self):
		self.tree = None
		self._setup_widgets()
		self._build_tree()
	def _setup_widgets(self):
		s = """\
click on header to sort by that column
to change width of column drag boundary
		"""
		msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
			padding=(10, 2, 10, 6), text=s)
		msg.pack(fill='x')
		container = ttk.Frame()
		container.pack(fill='both', expand=True)
		# create a treeview with dual scrollbars
		self.tree = ttk.Treeview(columns=data_header, show="headings")
		vsb = ttk.Scrollbar(orient="vertical",
			command=self.tree.yview)
		hsb = ttk.Scrollbar(orient="horizontal",
			command=self.tree.xview)
		self.tree.configure(yscrollcommand=vsb.set,
			xscrollcommand=hsb.set)
		self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
		vsb.grid(column=1, row=0, sticky='ns', in_=container)
		hsb.grid(column=0, row=1, sticky='ew', in_=container)
		container.grid_columnconfigure(0, weight=1)
		container.grid_rowconfigure(0, weight=1)
	def _build_tree(self):
		for col in data_header:
			self.tree.heading(col, text=col.title(),
				command=lambda c=col: sortby(self.tree, c, 0))
			# adjust the column's width to the header string
			self.tree.column(col,
				width=tkFont.Font().measure(col.title()))
		for item in data_list:
			self.tree.insert('', 'end', values=item)
			# adjust column's width if necessary to fit each value
			for ix, val in enumerate(item):
				col_w = tkFont.Font().measure(val)
				if self.tree.column(data_header[ix],width=None)<col_w:
					self.tree.column(data_header[ix], width=col_w)
def sortby(tree, col, descending):
	"""sort tree contents when a column header is clicked on"""
	# grab values to sort
	data = [(tree.set(child, col), child) \
		for child in tree.get_children('')]
	# if the data to be sorted is numeric change to float
	#data =  change_numeric(data)
	# now sort the data in place
	data.sort(reverse=descending)
	for ix, item in enumerate(data):
		tree.move(item[1], '', ix)
	# switch the heading so it will sort in the opposite direction
	tree.heading(col, command=lambda col=col: sortby(tree, col, \
		int(not descending)))
# the data ...
data_header = ['Months', 'Train #', 'Reservations']
data_list = [(1,0,0) ,(2,'4441 7772 9991', '1 1 1') ,(3, 2221, 1) ,(4, '1112 1231 8881', '1 1 1') ,
(5, '3331 6671', '1 1') ,(6, '1111 2341 4442', '3 3 3') ,(7, 0, 0) ,(8, 0, 0) ,(9, 0, 0) ,(10, 0, 0) ,
(11, 0, 0) ,(12, 0, 0)]
#[('Hyundai', 'brakes') ,('Honda', 'light') ,('Lexus', 'battery') ,('Benz', 'wiper') ,('Ford', 'tire') ,('Chevy', 'air') ,('Chrysler', 'piston') ,('Toyota', 'brake pedal') ,('BMW', 'seat')]

root = tk.Tk()
root.wm_title("View Popular Routes")
mc_listbox = popRoutes()
root.mainloop()
