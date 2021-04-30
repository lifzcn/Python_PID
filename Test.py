# -*- coding: utf-8 -*-
# @Time    : 2021/4/30
# @Author  : Fazheng Li
# @FileName: Test.py
# @Software: PyCharm
# @Blog    ：https://github.com/theleolee

import time
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rcParams

from scipy.interpolate import make_interp_spline

from Algorithm import PID

config = {"font.family": "serif",
          "font.size": 12,
          "mathtext.fontset": "stix",
          "font.serif": ["SimSun"]}
rcParams.update(config)


def test_pid(P=0.2, I=0.0, D=0.0, L=100):
    pid = PID(P, I, D)

    pid.SetPoint = 0.0
    pid.setSampleTime(0.01)

    END = L
    feedback = 0

    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        # print(output)
        if pid.SetPoint > 0:
            feedback += output  # (output - (1/i))控制系统的函数
        if 9 <= i <= 40:
            pid.SetPoint = 1
        elif i > 40:
            pid.SetPoint = 0.5

        time.sleep(0.01)

        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)
        time_list.append(i)

    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
    feedback_smooth = make_interp_spline(time_list, feedback_list)(time_smooth)

    plt.figure(figsize=(8, 8 * 0.618))

    plt.plot(time_smooth, feedback_smooth)
    plt.plot(time_list, setpoint_list)

    plt.xlabel("Time(s)")
    plt.ylabel("PID(PV)")
    plt.title("TEST-PID Kp={} Ki={} Kd={}".format(P, I, D))

    plt.grid(True)
    plt.savefig("PID-Kp={},Ki={},Kd={}.jpg".format(P, I, D))
    plt.savefig("PID-Kp={},Ki={},Kd={}.pdf".format(P, I, D))
    plt.close()

    return 0


if __name__ == "__main__":
    test_pid(0.8, 1.0, 0.001, L=50)
