# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, ScratchPad, DropDown, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget
from datetime import datetime
alt = "mod4"
#  alt = "mod1"

import subprocess
# TODO
need_commands = {
        "terminator":   "terminator",
        "emacsclient":  "emacsclient -c",
        "chrome":       "google-chrome-stable",
        "line":         "line.sh",
        }

not_found = "send-notify"


def cmd_exists(cmd):
    return subprocess.call(
            "type " + cmd.split(" ")[0], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

for k, v in need_commands.items():
    if not cmd_exists(v):
        need_commands[k] = None


keys = [
    # Switch between windows in current stack pane
    Key(
        [alt], "j",
        lazy.layout.down()
    ),
    Key(
        [alt], "k",
        lazy.layout.up()
    ),
    Key(
        [alt], "p",
        lazy.layout.previous(),
    ),

    Key([alt, "shift"], "h",
        lazy.layout.move_left()),
    Key([alt, "shift"], "l",
        lazy.layout.move_right()),

    # Move windows up or down in current stack
    Key(
        [alt, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [alt, "control"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [alt], "space",
        lazy.layout.shuffle_up()
    ),

    # Swap panes of split stack
    Key(
        [alt, "shift"], "space",
        lazy.layout.rotate()
    ),
    Key(
        [alt], "n",
        lazy.next_layout()
    ),

    Key([alt], "Return", lazy.spawn("alacritty")),
    Key([alt, "shift"], "Return", lazy.spawn("alacritty")),
    Key([alt], "g", lazy.spawn("google-chrome-stable --renderer-process-limit=1")),
    Key([alt], "e", lazy.spawn("emacsclient -c")),
    Key([alt, "control"], "l", lazy.spawn("i3lock")),
    Key([alt, "shift"], "l", lazy.spawn("sh -c 'i3lock && systemctl suspend'")),
    #Key([alt], "u", lazy.spawn("rofi -show window -monitor -4")),
    Key([alt], "u", lazy.findwindow()),

    Key([alt], "i", lazy.layout.grow()),
    Key([alt], "m", lazy.layout.shrink()),
    # Key([alt], "n", lazy.layout.normalize()),
    # Key([alt], "o", lazy.layout.maximize()),

    Key([alt], "f", lazy.window.toggle_floating()),

    # Toggle between different layouts as defined below
#      Key([alt], "tab", lazy.nextlayout()),
    Key([alt, 'shift'], "d", lazy.window.kill()),

    Key([alt, "control"], "r", lazy.restart()),
    Key([alt, "control"], "q", lazy.shutdown()),
#    Key([alt], "t", lazy.spawncmd()),
    Key([alt], "t", lazy.spawn("rofi -show run")),

    # move section
    Key([alt, "shift"], "j", lazy.layout.section_down()),
    Key([alt, "shift"], "k", lazy.layout.section_up()),

    Key([alt, 'shift'], 'i',
            lazy.layout.collapse_branch()),
    Key([alt, 'shift'], 'u',
            lazy.layout.expand_branch()),
    Key([alt, 'shift'], 'y',
            lazy.layout.move_left()),
    Key([alt, 'shift'], 'o',
            lazy.layout.move_right()),


    # change screen
    # Key([alt], "l", lazy.to_screen(0)),
    # Key([alt], "h", lazy.to_screen(1)),

    Key([alt], "l", lazy.next_screen()),
#TODO
#Key([alt], "a", lazy.group.group.set_label(using prompt widget)),

    Key([alt], 'F1',
            lazy.widget['prompt'].exec_general(
                'section(add)',
                'layout',
                'add_section')),

    Key([alt], 'F2',
            lazy.widget['prompt'].exec_general(
                'section(del)',
                'layout',
                'del_section')),

    Key([alt], 'F12', lazy.group['scratchpad'].dropdown_toggle('memo')),
]

group_format = '{:^10}'

groups = [
	ScratchPad("scratchpad", [
        DropDown("memo", "terminator -e lb", opacity=0.8),
    ]),

    Group('1', label=group_format.format('res_work[1]'), spawn='alacritty'),
    Group('2', label=group_format.format('nslfmt[2]')),
    Group('3', label=group_format.format('qtile[3]')),
    Group('4', label=group_format.format('[4]')),
    Group('7', label=group_format.format('[7]')),
    Group('8', label=group_format.format('google[8]')),
    Group('9', label=group_format.format('thesis[9]'), layout='treetab'),
    Group('0', label=group_format.format('info[0]'), layout='treetab'),
]

for i in groups:
    if isinstance(i, ScratchPad):
        continue

    # alt1 + letter of group = switch to group
    keys.append(
        Key([alt], i.name, lazy.group[i.name].toscreen())
    )

    # alt1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([alt, "shift"], i.name, lazy.window.togroup(i.name))
    )

borders = {
        'border_normal': '#000066',
        'border_forcus': '#0000FF',
        'border_width': 2,
}

layouts = [
      layout.MonadTall(**borders),
      layout.Stack(stacks=2),
      layout.TreeTab(),
      layout.Max(),
]

widget_defaults = dict(
    font='Arial',
    # font='Ricty'
    fontsize=16,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method='block',
                    inactive='999999'
                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Volume(),
                widget.CurrentScreen(),
                widget.CurrentLayout(),
                # widget.TextBox("default config", name="default"),
                # widget.TaskList(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %H:%M'),
            ],
            size=30,
            background=['222222', '111111'],
        ),
        bottom=bar.Bar(
            [
                widget.Battery(),
                # widget.GmailChecker(),
                # widget.KeyboardLayout(),
                #widget.CPUGraph(),
                #widget.MemoryGraph(),
                #widget.NetGraph(),
                # submit thesis
                #widget.Clipboard(),
                #widget.Notify(),
                # widget.HDDGraph(path='/'),
                #widget.DF(visible_on_warn=False),
                # widget.LoadAverageGraph(),
                #widget.QuickExit(),
            ],
            size=30,
            background=['222222', '111111'],
            ),
    ),

    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method='block',
                    inactive='999999'
                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.CurrentScreen(),
                widget.Pomodoro(),
                widget.CurrentLayout(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %H:%M'),
                #widget.QuickExit(),
            ],
            size=30,
            background=['222222', '111111'],
        ),
    ),
]

countdown_widget = next(
        (widget for widget in screens[0].bottom.widgets
            if widget.name == 'countdown'),
        None)

if countdown_widget is not None:
    keys.append(Key([alt], "c", lazy.widget['countdown'].toggle_visible()))

#  keys.append(Key([alt, "shift"], "t", lazy.widget['cpugraph'].toggle_visible()))

# Drag floating layouts.
#  mouse = [
#      Drag(
#          [alt], "Button1", lazy.window.set_position_floating(),
#          start=lazy.window.get_position()),
#      Drag(
#          [alt], "Button3", lazy.window.set_size_floating(),
#          start=lazy.window.get_size()),
#      Click([alt], "Button2", lazy.window.bring_to_front())
#  ]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = False

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.

wmname = "LG3D"
from libqtile import hook
import subprocess

import glob
file_lists = glob.glob('/home/hima/wallpapers/*')

def wallpaper():
    import random
    import time

    random.shuffle(file_lists)
    c = 0

    while True:
        import subprocess
        subprocess.Popen(['feh', '--bg-max', file_lists[c%len(file_lists)]])
        c += 1
        time.sleep(300)

from threading import Thread
wallpaper_thread = Thread(target=wallpaper)

@hook.subscribe.startup_once
def startup_once():
    subprocess.Popen(['fcitx-autostart'])
    subprocess.Popen(['xrandr', '--size', '1920x1080'])
    #subprocess.Popen(['start-pulseaudio-x11'])
    subprocess.Popen(['xmodmap', '/home/hima/.xmodmap'])
    subprocess.Popen(['xcompmgr', '-c'])
#      subprocess.Popen(['start_chrome.sh'])
    subprocess.Popen(['emacs', '--daemon'])


@hook.subscribe.startup
def startup():
    if wallpaper_thread.isAlive():
        wallpaper_thread.join()

    wallpaper_thread.start()
