import tkinter
import random
 
 
class MainWindow(tkinter.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("王员外爬格子练习器_v1.0")
        self.wm_geometry('800x600')
        self.last_index = 0
        self.str_var_list = []
        self.cancel_after_id = None
        self.current_status = "new"
        self.change_interval_var = tkinter.DoubleVar(value=3)
        self.source_list = ['1234', '1243', '1324', '1342', '1423', '1432', '2134', '2143', '2314', '2341', '2413',
                            '2431', '3124', '3142', '3214', '3241', '3412', '3421', '4123', '4132', '4213', '4312', '4321']
        default_number = self.source_list[0]
        self.number_box = tkinter.Frame(self)
        self.number_box.place(in_=self, relx=0.5,
                              rely=0.5, anchor=tkinter.CENTER)
        for num in default_number:
            self.str_var_list.append(self.create_label(self.number_box, num))
        self.init_top_zone()
        self.init_start_btn()
 
    def init_top_zone(self):
        my_top_zone = tkinter.Frame(self)
        my_top_zone.pack(side=tkinter.TOP, anchor=tkinter.W,
                         pady=2, fill=tkinter.X)
        tips = tkinter.Label(
            my_top_zone, text="每个数字代表品格，欢迎挑战您的手速", font=('微软雅黑', 12), fg="red")
        tips.pack(side=tkinter.LEFT, anchor=tkinter.W)
        interval_zone = tkinter.Frame(my_top_zone)
        interval_zone.pack(side=tkinter.RIGHT, anchor=tkinter.E)
        choice_label = tkinter.Label(interval_zone, text="品格切换速度(秒):")
        choice_label.pack(side=tkinter.LEFT)
        chice_interval = tkinter.OptionMenu(
            interval_zone, self.change_interval_var, "0.3", "0.5", "1", "2", "3", "4", "5", "6")
        chice_interval.pack(side=tkinter.LEFT, anchor=tkinter.E)
 
    def init_start_btn(self):
        def run_start():
            if self.current_status == "new":
                self.change_number()
                start_btn["text"] = "停止"
                self.current_status = "running"
            else:
                self.after_cancel(self.cancel_after_id)
                self.current_status = "new"
                start_btn['text'] = "开始"
        start_btn = tkinter.Button(self, text="开始", font=(
            '微软雅黑', 35), fg='red', command=run_start)
        start_btn.pack(side=tkinter.BOTTOM, fill=tkinter.X)
 
    def change_number(self):
        index = random.randint(0, len(self.source_list) - 1)
        if self.last_index == index:
            index = index + 1
            if index == len(self.source_list):
                index = 0
        self.last_index = index
        result = self.source_list[index]
        for index, var in enumerate(self.str_var_list):
            var.set(result[index])
        safe_mill = int(self.change_interval_var.get() * 1000)
        self.cancel_after_id = self.after(
            safe_mill, func=self.change_number)
 
    def create_label(self, master, text) -> tkinter.Label:
        str_var = tkinter.StringVar(value=text)
        my_label = tkinter.Label(
            master, textvariable=str_var, font=('微软雅黑', 220), padx=10)
        my_label.pack(side=tkinter.LEFT)
        return str_var
 
 
if __name__ == "__main__":
    root_window = MainWindow()
    root_window.mainloop()