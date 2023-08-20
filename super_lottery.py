# coding=utf-8
import random
import tkinter
from tkinter import messagebox

gamer_list = []
going = True


def lottery_roll(var_str_list, var2):
    global going
    if going:
        lottery_rule(var_str_list)
        window.after(60, lottery_roll, var_str_list, var2)
    else:
        var2.set('抽奖池{}人'.format(len(gamer_list)))
        going = True


def lottery_rule(var_str_list):
    show_members = []
    for i in range(min(len(gamer_list), len(var_str_list))):
        man = random.choice(gamer_list)
        try_max = 0
        while man in show_members and try_max <= 10:
            man = random.choice(gamer_list)
            try_max += 1
        show_members.append(man)

    for index, every_str_var in enumerate(var_str_list):
        every_str_var.set(show_members[index])
    return show_members


def lottery_start(var_str_list, var2):
    if len(var_str_list) >= len(gamer_list):
        messagebox.showwarning("提醒", "人数不够了，快去抓几个大佬")
        return False
    var2.set('谁是幸运者？')
    lottery_roll(var_str_list, var2)
    return True


def lottery_end(str_var_list, man_duplicate_switch):
    global going, gamer_list
    show_mans = lottery_rule(str_var_list)
    if not man_duplicate_switch:
        for man in show_mans:
            gamer_list.remove(man)
    going = False


class LoveWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("叫我王员外的抽奖工具_v1.0")
        self.init_bind_window_change()
        man_count_frame = tkinter.Frame(self)
        count_tips = tkinter.Label(man_count_frame, text="每轮人数", anchor=tkinter.W, width=8)
        count_tips.pack(side=tkinter.LEFT)
        man_count = tkinter.Scale(man_count_frame, from_=1, to_=10, tickinterval=1, orient='horizontal', length=300,
                                  fg='red',
                                  )
        man_count.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)
        man_count_frame.pack(side=tkinter.TOP, fill=tkinter.X)
        activity_title_frame = tkinter.Frame(self)
        activity_tips_label = tkinter.Label(activity_title_frame, text="抽奖主题", anchor=tkinter.W, width=8)
        activity_tips_label.pack(side=tkinter.LEFT)
        title_var_str = tkinter.StringVar(value="公司年会大奖")
        activity_title_input = tkinter.Entry(activity_title_frame, textvariable=title_var_str)
        activity_title_input.pack(side=tkinter.LEFT, fill=tkinter.X, expand=tkinter.TRUE)
        activity_title_frame.pack(side=tkinter.TOP, fill=tkinter.X)

        def come_on_baby():
            all_man = self.man_list(input_man.get(1.0, "end"))
            if not title_var_str.get():
                tkinter.messagebox.showerror("无主题", "没有主题,抽什么奖?")
            if not all_man:
                tkinter.messagebox.showerror("无人", "没有人，抽什么奖？")
                return
            LotteryWindow(self, man_count.get(), title_var_str.get(), all_man, allow_duplicate_man.get())

        is_remove_frame = tkinter.Frame(self)
        is_remove_tips = tkinter.Label(is_remove_frame, text="重复抽奖", width=7, anchor=tkinter.W)
        is_remove_tips.pack(side=tkinter.LEFT)
        allow_duplicate_man = tkinter.BooleanVar()
        allow_duplicate_man.set(True)
        is_remove_switch = tkinter.Checkbutton(is_remove_frame, text="允许", onvalue=True, offvalue=False,
                                               variable=allow_duplicate_man)
        is_remove_switch.pack(side=tkinter.LEFT, fill=tkinter.X)
        is_remove_frame.pack(side=tkinter.TOP, fill=tkinter.X)

        setting_man_frame = tkinter.Frame(self)
        setting_man_tips = tkinter.Label(setting_man_frame, text="抽奖池子", anchor=tkinter.N, width=8)
        setting_man_tips.pack(side=tkinter.LEFT, fill=tkinter.Y)
        input_man = tkinter.Text(setting_man_frame, height=10, wrap="word")
        input_man.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.TRUE)
        input_man.insert("insert", "张三 李四 王五 赵六 铁蛋 王员外 李美 王者 Tom Jack 美女 帅哥 史泰龙 施瓦辛格")
        setting_man_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.TRUE)

        rocket_btn = tkinter.Button(self, text="进入抽奖区", command=come_on_baby, height=2, bg="orange", fg='white',
                                    font='Helvetica -15')
        rocket_btn.pack(side=tkinter.BOTTOM, fill=tkinter.X)

    def man_list(self, all_man_str):
        print(all_man_str)
        man_result = []
        for line in all_man_str.split():
            man_result.extend(line.split())
        return man_result

    def init_bind_window_change(self):
        self.bind("<Visibility>", lambda event: self.focus_force())


class LotteryWindow(tkinter.Toplevel):
    def __init__(self, master, man_count, activity_title, all_man, duplicate_man):
        super().__init__(master)
        self.master = master
        self.master.state("icon")
        self.man_count = man_count
        self.human_frame_1 = None
        self.human_frame_2 = None
        self.show_mans = None
        self.is_start = True
        self.all_man = all_man
        self.allow_duplicate_switch = duplicate_man
        self.activity_title = tkinter.StringVar(value=activity_title)
        self.init_window_attr()
        self.init_data()
        self.init_view()
        self.bind_esc()

    def bind_esc(self):
        def exit_game(event):
            result = tkinter.messagebox.askyesno("结束", "确认结束吗?")
            if result:
                self.destroy()
            else:
                self.focus_force()

        self.bind("<Escape>", func=exit_game)

    def init_window_attr(self):
        self.geometry('800x500+500+200')
        self.attributes("-fullscreen", True)
        self.attributes('-alpha',0.7)
        # self.overrideredirect(True)

    def init_data(self):
        global gamer_list
        gamer_list = self.all_man

    def update_mans(self):
        for widget in self.human_frame_1.winfo_children():
            widget.destroy()
        for widget in self.human_frame_2.winfo_children():
            widget.destroy()
        self.show_mans = []
        max_man = 10
        if self.man_count > max_man:
            raise RuntimeError()
        first_group_man = min(5, self.man_count)
        self.create_name(self.human_frame_1, 0, first_group_man)
        if self.man_count != 5:
            self.create_name(self.human_frame_2, 5, self.man_count)

    def create_name(self, parent_frame, range_start, range_end):
        base_font = -40 #字体越来越大的效果，很好看
        for love_man in range(range_start, range_end):
            self.show_mans.append(tkinter.StringVar(value="幸运儿"))
            man_name = tkinter.Label(parent_frame, textvariable=self.show_mans[love_man], justify='left',
                                     anchor=tkinter.CENTER,
                                     height=2,
                                     font='楷体 ' + str(base_font), foreground='black', padx=10)
            man_name.pack(side=tkinter.LEFT)
            base_font = base_font + -10

    def init_view(self):
        show_label1_title = tkinter.Label(self, textvariable=self.activity_title, justify='left', anchor=tkinter.CENTER,
                                          height=4,
                                          font='楷体 -80 bold', foreground='black')
        show_label1_title.pack()
        self.human_frame_1 = tkinter.Frame(self)
        self.human_frame_1.pack()
        self.human_frame_2 = tkinter.Frame(self)
        self.human_frame_2.pack()
        self.update_mans()
        tip_join_man_count_var = tkinter.StringVar(value='{}人参与抽奖'.format(len(gamer_list)))
        show_label2 = tkinter.Label(self, textvariable=tip_join_man_count_var, justify='left', anchor=tkinter.CENTER,
                                    height=4,
                                    font='楷体 -25 bold', foreground='red')
        show_label2.pack(side=tkinter.TOP, pady=20)

        def let_love(event=None):
            if self.is_start and lottery_start(self.show_mans, tip_join_man_count_var):
                self.is_start = False
                start_stop_btn["text"] = "停止"
            else:
                lottery_end(self.show_mans, self.allow_duplicate_switch)
                start_stop_btn["text"] = "抽奖"
                self.is_start = True

        start_stop_btn = tkinter.Button(self, text='开始', command=let_love, width=15,
                                        height=1,
                                        bg='red',
                                        font='宋体 -30 bold', fg='white')  # 服了，字符多大，控件就多大
        start_stop_btn.pack(side=tkinter.TOP)
        self.bind("<space>", let_love)  # 为啥<space>不好使，<Return>也不好使？原因找到了,因为没有焦点
        self.focus_force()

    def destroy(self):
        self.master.state("normal")
        super().destroy()


if __name__ == '__main__':
    window = LoveWindow()
    window.mainloop()
