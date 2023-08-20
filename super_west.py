#!/usr/bin/env python3

import tkinter
import tkinter.font
import random
import os

__version__ = "1.3"

gamer_list = ["大龙马", "大唐僧", "小唐僧", "大悟空", "小悟空", "大八戒", "小八戒", "大沙僧", "小沙僧", "大龙马"]
gamer_image_list = []
pressed_gamer_list = ["龙马", "唐僧", "悟空", "八戒", "沙僧", "龙马"]
gamer_list_score = [5, 80, 2, 60, 2, 40, 2, 20, 2, 5]

TOTAL_SCORE_VAR = None
CURRENT_SCORE_VAR = None

GAME_STATUS_NEW = 0
GAME_STATUS_RUNNING = 1
GAME_STATUS_READY = 2
GAME_STATUS_TERMINATED = 3


class ScoreManager(object):  # 要面向对象编程，记住了
    def __init__(self):
        super().__init__()
        self.pressed_score_list = {}

    def append_pressed_btn_score_var(self, btn_key, var_obj):  # 面向接口编程，不能对外提供持有的对象
        if not isinstance(var_obj, tkinter.IntVar):
            raise ValueError("not match value")
        self.pressed_score_list[btn_key] = var_obj

    def obtain_pressed_btn_variable(self, btn_key):
        return self.pressed_score_list[btn_key]

    def count_pressed_score(self, select_man_name):
        all_score = []
        for pressed_btn, score_int_var in self.pressed_score_list.items():
            if pressed_btn.cget("text") in select_man_name:
                all_score.append(score_int_var.get())
        return sum(all_score)

    def obtain_all_pressed_total_score(self):
        all_score = []
        for pressed_btn, score_int_var in self.pressed_score_list.items():
            all_score.append(score_int_var.get())
        return sum(all_score)

    def clear_pressed_score(self):
        for score_int_var in self.pressed_score_list.values():
            score_int_var.set(0)

    def check_can_start(self):
        for score_int_var in self.pressed_score_list.values():
            if score_int_var.get() > 0:
                return True
        return False


class RootWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.game_zone = None
        self.status_zone = None
        self.score_manager = ScoreManager()
        self.game_status = GameStatus(GAME_STATUS_NEW)
        self.init_window_info()
        self.init_game_zone()
        self.init_status_zone()

    def init_window_info(self):
        self.geometry("800x700")
        self.title("西游记_v" + __version__)

    def init_game_zone(self):
        self.game_zone = GameZone(self, self.score_manager, self.game_status, bg="yellow")
        self.game_zone.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    def init_status_zone(self):
        self.status_zone = StatusZone(self, self.score_manager,
                                      self.game_status, width=200)  # Frame的宽度width，当在内部有了控件时，width功能完全没用，还得Frame中的控件决定
        self.status_zone.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.status_zone.pack_propagate(flag=False)  # 调用该方法后，Frame大小才会生效，不会自适应

    def start_game(self):
        self.game_zone.start_game()


class GameZone(tkinter.Frame):
    def __init__(self, master, score_manager, game_status, **kwargs):
        super().__init__(master, **kwargs)
        self.score_manager = score_manager
        self.game_status = game_status
        self.pig_image = tkinter.PhotoImage(file="res" + os.sep + "ba_jie_80.png")
        self.pig_image_60 = tkinter.PhotoImage(file="res" + os.sep + "ba_jie_60.png")
        self.pig_image_80 = tkinter.PhotoImage(file="res" + os.sep + "ba_jie_80.png")

        self.sha_seng_image = tkinter.PhotoImage(file="res" + os.sep + "sha_seng_80.png")
        self.sha_seng_image_60 = tkinter.PhotoImage(file="res" + os.sep + "sha_seng_60.png")
        self.sha_seng_image_80 = tkinter.PhotoImage(file="res" + os.sep + "sha_seng_80.png")

        self.wu_kong_image = tkinter.PhotoImage(file="res" + os.sep + "sun_wu_kong_80.png")
        self.wu_kong_image_60 = tkinter.PhotoImage(file="res" + os.sep + "sun_wu_kong_60.png")
        self.wu_kong_image_80 = tkinter.PhotoImage(file="res" + os.sep + "sun_wu_kong_80.png")

        self.tang_seng_image = tkinter.PhotoImage(file="res" + os.sep + "tang_seng_80.png")
        self.tang_seng_image_60 = tkinter.PhotoImage(file="res" + os.sep + "tang_seng_60.png")
        self.tang_seng_image_80 = tkinter.PhotoImage(file="res" + os.sep + "tang_seng_80.png")

        self.bai_long_ma_image = tkinter.PhotoImage(file="res" + os.sep + "bai_long_ma_80.png")
        self.bai_long_ma_image_60 = tkinter.PhotoImage(file="res" + os.sep + "bai_long_ma_60.png")
        self.bai_long_ma_image_80 = tkinter.PhotoImage(file="res" + os.sep + "bai_long_ma_80.png")
        self.init_global_image()
        self.create_press_btn()
        self.gamer_label_all = []
        self.game_score_panel = None
        self.create_game_panel()
        self.current_select_man_index = 0
        self.pre_man = None
        self.game_speed = 10
        self.random_move_block_times = 10

    def init_global_image(self):
        global gamer_image_list
        gamer_image_list.append(self.bai_long_ma_image_60)
        gamer_image_list.append(self.tang_seng_image_80)
        gamer_image_list.append(self.tang_seng_image_60)
        gamer_image_list.append(self.wu_kong_image_80)
        gamer_image_list.append(self.wu_kong_image_60)
        gamer_image_list.append(self.pig_image_80)
        gamer_image_list.append(self.pig_image_60)
        gamer_image_list.append(self.sha_seng_image_80)
        gamer_image_list.append(self.sha_seng_image_60)
        gamer_image_list.append(self.bai_long_ma_image_60)

    def create_press_btn(self):
        global gamer_list
        pressed_btn_score_frame = tkinter.Frame(self)  # 怎么又变成包含内容了，这个height没啥用

        def change_score(event):
            global TOTAL_SCORE_VAR
            global GAME_STATUS_NEW
            if TOTAL_SCORE_VAR.get() <= 0:
                return
            current_pressed_btn = event.widget
            score_variable = self.score_manager.obtain_pressed_btn_variable(current_pressed_btn)
            score_variable.set(score_variable.get() + 1)
            TOTAL_SCORE_VAR.set(TOTAL_SCORE_VAR.get() - 1)
            self.game_status.set_status(GAME_STATUS_NEW)

        for index in range(len(pressed_gamer_list)):
            cell_frame = tkinter.Frame(pressed_btn_score_frame)
            show_score_text = tkinter.Label(cell_frame, font=('Arial', 22), fg='red')
            show_score_text.pack(side=tkinter.TOP)
            btn_text = pressed_gamer_list[index]
            if "沙僧" in btn_text:
                use_image = self.sha_seng_image
            elif "龙马" in btn_text:
                use_image = self.bai_long_ma_image
            elif "唐僧" in btn_text:
                use_image = self.tang_seng_image
            elif "悟空" in btn_text:
                use_image = self.wu_kong_image
            elif "八戒" in btn_text:
                use_image = self.pig_image
            else:
                raise RuntimeError("use_image can not be null")
            pressed_btn = tkinter.Button(cell_frame, width=80, height=80, text=btn_text,
                                         image=use_image, repeatdelay=100, repeatinterval=100,
                                         activebackground='orange')
            pressed_btn.pack(side=tkinter.TOP)
            pressed_btn.bind("<Button-1>", func=change_score)
            int_var = tkinter.IntVar()
            show_score_text.configure(textvariable=int_var)
            self.score_manager.append_pressed_btn_score_var(pressed_btn, int_var)
            cell_frame.grid(column=index, row=0, sticky=tkinter.EW)
            pressed_btn_score_frame.columnconfigure(index, weight=1)
        pressed_btn_score_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X, ipady=2)

    def create_game_panel(self):
        game_panel = tkinter.Frame(self)
        game_panel.pack_configure(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)
        top_frame = tkinter.Frame(game_panel, bg="grey")
        top_frame.pack(side=tkinter.TOP, fill=tkinter.X)
        bottom_frame = tkinter.Frame(game_panel, bg="purple")
        bottom_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        left_frame = tkinter.Frame(game_panel, bg="orange")
        left_frame.pack(side=tkinter.LEFT, fill=tkinter.Y)
        right_frame = tkinter.Frame(game_panel, bg="pink")
        right_frame.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.create_man(top_frame, [9, 3, 9, 1, 2, 5, 6, 8], side=tkinter.TOP)
        self.create_man(right_frame, [9, 2, 9, 1, 5, 7], side=tkinter.RIGHT)
        self.create_man(bottom_frame, [9, 3, 2, 9, 2, 5, 6, 8], side=tkinter.BOTTOM, need_reversed=True)
        self.create_man(left_frame, [9, 4, 2, 9, 2, 6], side=tkinter.LEFT, need_reversed=True)
        self.game_score_panel = GameScorePanel(game_panel)
        self.game_score_panel.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def create_man(self, box, gamer_list_index, side, need_reversed=False):
        global gamer_list
        global gamer_image_list
        secret_box = []
        if side == tkinter.TOP or side == tkinter.BOTTOM:
            for index, man_index in enumerate(gamer_list_index):
                show_man_text = gamer_list[man_index]
                use_image = gamer_image_list[man_index]
                gamer = tkinter.Label(box, text=show_man_text, width=72, height=72, image=use_image, relief='groove')
                gamer.grid(column=index, row=0)
                secret_box.append(gamer)
                box.columnconfigure(index, weight=1)
        else:
            for index, man_index in enumerate(gamer_list_index):
                show_man_text = gamer_list[man_index]
                use_image = gamer_image_list[man_index]
                gamer = tkinter.Label(box, text=show_man_text, width=72, height=72, image=use_image, relief="groove")
                gamer.grid(column=0, row=index)
                secret_box.append(gamer)
                box.rowconfigure(index, weight=1)
        if need_reversed:
            secret_box.reverse()
        self.gamer_label_all.extend(secret_box)

    def after_loop(self, times):
        global GAME_STATUS_READY
        if self.current_select_man_index == len(self.gamer_label_all):
            self.current_select_man_index = 0
        current_man = self.gamer_label_all[self.current_select_man_index]
        current_man_old_bg = current_man.cget("bg")
        if self.pre_man:
            self.pre_man.config(bg=current_man_old_bg)
        current_man.config(bg="red")
        self.pre_man = current_man
        if times > 0:
            times -= 1
            self.gamer_label_all[self.current_select_man_index].after(self.game_speed,
                                                                      func=lambda: self.after_loop(times))
            self.current_select_man_index += 1
            self.game_speed_control(times)
        else:
            select_man_str = self.obtain_current_selected_man_str()
            select_man_score_index = gamer_list.index(select_man_str)
            print("选中:" + select_man_str)
            print(self.current_select_man_index)
            print(self.score_manager.count_pressed_score(select_man_str))
            self.game_status.set_status(GAME_STATUS_READY)
            self.game_score_panel.set_current_score(
                gamer_list_score[select_man_score_index] * self.score_manager.count_pressed_score(select_man_str))

    def obtain_current_selected_man_str(self):
        return self.gamer_label_all[self.current_select_man_index].cget("text")

    def game_speed_control(self, times):
        if times == 40:
            self.game_speed = self.game_speed + 10
        elif times == 20:
            self.game_speed = self.game_speed + 20
        elif times == 10:
            self.game_speed = self.game_speed + 80
        elif times == 5:
            self.game_speed = self.game_speed + 180

    def start_game(self):
        self.game_speed = 30
        random_num = random.randint(80, 120)
        print("random:" + str(random_num))
        self.after_loop(random_num)


class GameScorePanel(tkinter.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        global CURRENT_SCORE_VAR
        CURRENT_SCORE_VAR = tkinter.IntVar()
        current_score = tkinter.Label(self, textvariable=CURRENT_SCORE_VAR, font=('Arial', 40))
        current_score.pack(side=tkinter.TOP)
        self.hide_score = tkinter.IntVar()
        trigger_score = tkinter.Label(self, textvariable=self.hide_score, text="?")
        trigger_score.pack(side=tkinter.TOP)
        compare_frame = tkinter.Frame(self)
        self.small_btn = tkinter.Button(compare_frame, text="小", font=('Arial', 15))
        self.small_btn.pack(side=tkinter.LEFT)
        self.middle_btn = tkinter.Button(compare_frame, text="中", font=('Arial', 15))
        self.middle_btn.pack(side=tkinter.LEFT)
        self.big_btn = tkinter.Button(compare_frame, text="大", font=('Arial', 15))
        self.big_btn.pack(side=tkinter.LEFT)
        compare_frame.pack(side=tkinter.TOP)
        self.listener_compare_small_and_big()

    def listener_compare_small_and_big(self):
        global CURRENT_SCORE_VAR

        def btn_trigger(btn_widget):
            if CURRENT_SCORE_VAR.get() == 0:
                return
            self.trigger_hide_score()
            current_hide_score = self.hide_score.get()
            if btn_widget is self.small_btn and current_hide_score <= 6:
                CURRENT_SCORE_VAR.set(CURRENT_SCORE_VAR.get() * 2)
            elif btn_widget is self.middle_btn and current_hide_score == 7:
                CURRENT_SCORE_VAR.set(CURRENT_SCORE_VAR.get() * 3)
            elif btn_widget is self.big_btn and current_hide_score >= 8:
                CURRENT_SCORE_VAR.set(CURRENT_SCORE_VAR.get() * 2)
            else:
                CURRENT_SCORE_VAR.set(0)

        self.small_btn["command"] = lambda: btn_trigger(self.small_btn)
        self.middle_btn["command"] = lambda: btn_trigger(self.middle_btn)
        self.big_btn["command"] = lambda: btn_trigger(self.big_btn)

    def trigger_hide_score(self):
        random_score = random.randint(1, 13)
        self.hide_score.set(random_score)

    def set_current_score(self, int_score):
        global CURRENT_SCORE_VAR
        CURRENT_SCORE_VAR.set(int_score)

    def get_current_sore(self):
        global CURRENT_SCORE_VAR
        return CURRENT_SCORE_VAR.get()


# 2个唐僧、2个驴、2个孙悟空、2个猪八戒、2个沙僧

class GameStatus(object):
    def __init__(self, status):
        self.current_status = status

    def set_status(self, status):
        self.current_status = status

    def get_status(self):
        return self.current_status


class StatusZone(tkinter.Frame):
    def __init__(self, master, score_manager, game_status, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.score_manager = score_manager
        self.game_status = game_status
        self.current_game_status = None
        global TOTAL_SCORE_VAR
        TOTAL_SCORE_VAR = tkinter.IntVar()  # 原因，IntVar对象依赖于当前Window对象，所以必须Window对象先创建
        total_score_font = tkinter.font.Font(family='Fixdsys', size=26, weight=tkinter.font.BOLD)
        current_total_score = tkinter.Label(self, textvariable=TOTAL_SCORE_VAR, font=total_score_font)
        current_total_score.pack(side=tkinter.TOP, pady=20)
        self.more_money_btn = tkinter.Button(self, text="加币", font=total_score_font, activeforeground="orange",
                                             background='Coral', fg='white')
        self.more_money_btn.pack(side=tkinter.TOP, ipadx=6)
        self.listener_more_monkey()
        self.start_btn = tkinter.Button(self, text="开始", font=('Arial', 14, 'bold'), fg='blue')
        self.start_btn.pack(side=tkinter.BOTTOM, fill=tkinter.X, padx=5, pady=5)
        self.listener_start_btn()
        self.obtain_btn = tkinter.Button(self, text="获取得分", font=('Arial', 14, 'bold'), fg="blue")
        self.obtain_btn.pack(side=tkinter.BOTTOM, fill=tkinter.X, padx=5, pady=5)
        self.listener_obtain_score()

    def listener_more_monkey(self):
        def invest_money():
            global TOTAL_SCORE_VAR
            TOTAL_SCORE_VAR.set(TOTAL_SCORE_VAR.get() + 10)

        self.more_money_btn.configure(command=invest_money)

    def listener_obtain_score(self):
        def obtain_score():
            if self.game_status.get_status() == GAME_STATUS_NEW:
                return
            global CURRENT_SCORE_VAR
            global TOTAL_SCORE_VAR
            TOTAL_SCORE_VAR.set(TOTAL_SCORE_VAR.get() + CURRENT_SCORE_VAR.get())
            self.score_manager.clear_pressed_score()
            CURRENT_SCORE_VAR.set(0)
            self.game_status.set_status(GAME_STATUS_NEW)

        self.obtain_btn.config(command=obtain_score)

    def listener_start_btn(self):
        def run_game():
            global GAME_STATUS_READY
            global TOTAL_SCORE_VAR
            if self.score_manager.check_can_start() and (
                    self.game_status.get_status() == GAME_STATUS_NEW or self.game_status.get_status() == GAME_STATUS_READY):
                self.restart_game()
                self.master.start_game()
                self.game_status.set_status(GAME_STATUS_RUNNING)

        self.start_btn["command"] = run_game

    def restart_game(self):
        global TOTAL_SCORE_VAR
        global CURRENT_SCORE_VAR
        if self.game_status.get_status() == GAME_STATUS_READY:
            TOTAL_SCORE_VAR.set(
                TOTAL_SCORE_VAR.get() - self.score_manager.obtain_all_pressed_total_score() + CURRENT_SCORE_VAR.get())


if __name__ == "__main__":
    root_window = RootWindow()  # 我曾经尝试在这里创建IntVar()，由于在这里创建，current_total_score的textvariable指向的是None，所以不行

    root_window.mainloop()
