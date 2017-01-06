#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import bluetooth
import pygame
from pygame.locals import *

HID_HANDSHAKE = 0x0
HID_GET_REPORT = 0x4
HID_SET_REPORT = 0x5
HID_DATA = 0xA

HID_TYPE_RESERVED = 0
HID_TYPE_INPUT = 1
HID_TYPE_OUTPUT = 2
HID_TYPE_FEATURE = 3

CTRL = 17
INTR = 19

DIGITAL_ORDER = ["select", "l3", "r3", "start", "d-up", "d-right", "d-down", "d-left", "l2", "r2", "l1", "r1", "triangle", "circle", "cross", "square", "ps"]
ANALOG_ORDER = ["d-up", "d-right", "d-down", "d-left", "l2", "r2", "l1", "r1", "triangle", "circle", "cross", "square"]

class SixAxis:
    def __init__(self):
        self.ctrl=bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.intr=bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.bt_addr = "" #set the ps3 bluetooth address
        self.state = 0
        self.feature_ef_byte_6 = 0;
        self.buttons = {"d-left":0, "d-right":0, "d-up":0, "d-down":0, "cross":0, "square":0, "circle":0, "triangle":0, "select":0, "start":0, "ps":0, "r1":0, "r2":0, "r3":0, "l1":0, "l2":0, "l3":0}
        self.axis = {"left-x":128, "left-y":128, "right-x":128, "right-y":128}
        self.xcount = 0
        self.ycount = 0

    def hex2string(self, data):
        buf = "".join([chr(d) for d in data])
        return buf

    def connect(self):
        print ("trying to connect to %s on PSM 0x%X (ctrl)" % (self.bt_addr, CTRL))
        self.ctrl.connect((self.bt_addr, CTRL))
        print ("trying to connect to %s on PSM 0x%X (intr)" % (self.bt_addr, INTR))
        self.intr.connect((self.bt_addr, INTR))

        pygame.init()
        screen = pygame.display.set_mode((1280, 800), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        try:
            while True:
                pygame.time.delay(20)
                self.xcount -= 1
                self.ycount -= 1
                if not self.state:
                    data = self.ctrl.recv(1024)
                    if len(data):
                        self.process(data, CTRL)

                        #ctrl.send("00".decode("hex"))
                        #state = 1
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == K_a:
                                #self.buttons["d-left"] = 1
                                self.axis["left-x"] = 0
                            elif event.key == K_s:
                                #self.buttons["d-down"] = 1
                                self.axis["left-y"] = 255
                            elif event.key == K_d:
                                #self.buttons["d-right"] = 1
                                self.axis["left-x"] = 255
                            elif event.key == K_w:
                                #self.buttons["d-up"] = 1
                                self.axis["left-y"] = 0
                            elif event.key == K_ESCAPE:
                                raise Exception
                            elif event.key == K_LCTRL:
                                self.buttons["l2"] = 1
                            elif event.key == K_q:
                                self.buttons["r2"] = 1
                            elif event.key == K_TAB:
                                self.buttons["select"] = 1
                            elif event.key == K_LSHIFT:
                                self.buttons["l3"] = 1
                            elif event.key == K_v:
                                self.buttons["r3"] = 1
                            elif event.key == K_r:
                                self.buttons["square"] = 1
                            elif event.key == K_SPACE:
                                self.buttons["cross"] = 1
                            elif event.key == K_e:
                                self.buttons["circle"] = 1
                            elif event.key == K_f:
                                self.buttons["triangle"] = 1
                            elif event.key == K_BACKSPACE:
                                self.buttons["start"] = 1
                            elif event.key == K_RSHIFT:
                                self.buttons["ps"] = 1
                            elif event.key == K_LEFT:
                                self.buttons["d-left"] = 1
                            elif event.key == K_RIGHT:
                                self.buttons["d-right"] = 1
                            elif event.key == K_UP:
                                self.buttons["d-up"] = 1
                            elif event.key == K_DOWN:
                                self.buttons["d-down"] = 1
                        elif event.type == pygame.KEYUP:
                            if event.key == K_a:
                                #self.buttons["d-left"] = 0
                                self.axis["left-x"] = 128
                            elif event.key == K_s:
                                #self.buttons["d-down"] = 0
                                self.axis["left-y"] = 128
                            elif event.key == K_d:
                                #self.buttons["d-right"] = 0
                                self.axis["left-x"] = 128
                            elif event.key == K_w:
                                #self.buttons["d-up"] = 0
                                self.axis["left-y"] = 128
                            elif event.key == K_LCTRL:
                                self.buttons["l2"] = 0
                            elif event.key == K_q:
                                self.buttons["r2"] = 0
                            elif event.key == K_TAB:
                                self.buttons["select"] = 0
                            elif event.key == K_LSHIFT:
                                self.buttons["l3"] = 0
                            elif event.key == K_v:
                                self.buttons["r3"] = 0
                            elif event.key == K_r:
                                self.buttons["square"] = 0
                            elif event.key == K_SPACE:
                                self.buttons["cross"] = 0
                            elif event.key == K_e:
                                self.buttons["circle"] = 0
                            elif event.key == K_f:
                                self.buttons["triangle"] = 0
                            elif event.key == K_BACKSPACE:
                                self.buttons["start"] = 0
                            elif event.key == K_RSHIFT:
                                self.buttons["ps"] = 0
                            elif event.key == K_LEFT:
                                self.buttons["d-left"] = 0
                            elif event.key == K_RIGHT:
                                self.buttons["d-right"] = 0
                            elif event.key == K_UP:
                                self.buttons["d-up"] = 0
                            elif event.key == K_DOWN:
                                self.buttons["d-down"] = 0
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                self.buttons["r1"] = 1
                            elif event.button == 2:
                                self.buttons["triangle"] = 1
                            elif event.button == 3:
                                self.buttons["l1"] = 1
                        elif event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:
                                self.buttons["r1"] = 0
                            elif event.button == 2:
                                self.buttons["triangle"] = 0
                            elif event.button == 3:
                                self.buttons["l1"] = 0
                        elif event.type == pygame.MOUSEMOTION:
                            #print event
                            #self.axis["right-x"] = max(min(128 + event.rel[0]*3, 255), 0)
                            x = 128
                            y = 128
                            self.xcount = abs(event.rel[0])
                            self.ycount = abs(event.rel[1])
                            if event.rel[0] > 0:
                                x = 255
                            elif event.rel[0] < 0:
                                x = 0
                            if event.rel[1] > 0:
                                y = 255
                            elif event.rel[1] < 0:
                                y = 0
                            self.axis["right-x"] = x
                            self.axis["right-y"] = y
                            #self.axis["right-y"] = max(min(128 + event.rel[1]*3, 255), 0)
                            #print "x: %s y: %s"%(self.axis["right-x"], self.axis["right-y"])
                    buf = self.hex2string(self.assemble_input())
                    self.intr.send("A101".decode("hex")+buf)

                    if self.xcount == 0:
                        self.axis["right-x"] = 128
                    if self.ycount == 0:
                        self.axis["right-y"] = 128
        finally:
            self.ctrl.close()
            self.intr.close()

    def process(self, data, psm):
        transaction = (ord(data[0]) & 0xf0) >> 4
        print ("transaction: 0x%x" % transaction)
        if transaction == HID_GET_REPORT:
            typ = ord(data[0]) & 0x03
            if typ == HID_TYPE_RESERVED:
                return -1

            report = ord(data[1])
            self.send_report(psm, typ, report)
        elif transaction == HID_SET_REPORT or transaction == HID_DATA:
            typ = ord(data[0]) & 0x03
            if typ == HID_TYPE_RESERVED:
                return -1

            report = ord(data[1])
            self.process_report(typ, report, data[2:])
            if psm == CTRL:
                c = (HID_HANDSHAKE << 4) | 0x0
                self.ctrl.send(chr(c))

    def send_report(self, psm, typ, report):
        buf = ""
        if typ == HID_TYPE_FEATURE:
            print ("HID_TYPE_FEATURE")
            if report == 0x01:
                buf = self.assemble_feature_01()
            elif report == 0xef:
                buf = self.assemble_feature_ef()
            elif report == 0xf2:
                buf = self.assemble_feature_f2()
            elif report == 0xf8:
                buf = self.assemble_feature_f8()
        if typ == HID_TYPE_INPUT:
            print ("HID_TYPE_INPUT")

        buf = chr(0x0a | typ) + chr(report) + buf

        if psm == CTRL:
            self.ctrl.send(buf)
        elif psm == INTR:
            self.intr.send(buf)

    def process_report(self, typ, report, data):
        if typ == HID_TYPE_INPUT:
            pass
        elif typ == HID_TYPE_OUTPUT:
            pass
        elif typ == HID_TYPE_FEATURE:
            if report == 0xef:
                self.process_feature_ef(data)
            elif report == 0xf4:
                self.process_feature_f4(data)

    def assemble_feature_01(self):
        data = [
            0x01, 0x03, 0x00, 0x05, 0x0c, 0x01, 0x02, 0x18,
            0x18, 0x18, 0x18, 0x09, 0x0a, 0x10, 0x11, 0x12,
            0x13, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x02,
            0x02, 0x02, 0x02, 0x00, 0x00, 0x00, 0x04, 0x04,
            0x04, 0x04, 0x00, 0x00, 0x02, 0x01, 0x02, 0x00,
            0x64, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        return self.hex2string(data)

    def assemble_feature_ef(self):
        data = [
            0xef, 0x04, 0x00, 0x05, 0x03, 0x01, 0xb0, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x02, 0x74, 0x02, 0x71, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04
        ]

        data[6] = self.feature_ef_byte_6;
        return self.hex2string(data)

    def assemble_feature_f2(self):
        data = [
            0xff, 0xff, 0x00, 0x00, 0x1e, 0x3d, 0x24, 0x97,
            0xde, 0x00, 0x03, 0x50, 0x89, 0xc0, 0x01, 0x8a,
            0x09
        ]
        return self.hex2string(data)

    def assemble_feature_f8(self):
        data = [
            0x01, 0x00, 0x00, 0x00
        ]
        return self.hex2string(data)

    def process_feature_ef(self, data):
        self.feature_ef_byte_6 = ord(data[6])

    def process_feature_f4(self, data):
        self.state = 1

    def assemble_input(self):
        buf = [0 for i in xrange(0, 48)]

        for i in xrange(0, 17):
            byte = 1 + (i / 8)
            offset = i % 8
            if self.buttons[DIGITAL_ORDER[i]]:
                buf[byte] |= (1 << offset)

        buf[5] = self.axis["left-x"]
        buf[6] = self.axis["left-y"]
        buf[7] = self.axis["right-x"]
        buf[8] = self.axis["right-y"]

        for i in xrange(0, 12):
            buf[13 + i] =  255 if self.buttons[ANALOG_ORDER[i]] else 0

        buf[28] = 0x03
        buf[29] = 0x05
        buf[30] = 0x16

        buf[31] = 0x00
        buf[32] = 0x00
        buf[33] = 0x00
        buf[34] = 0x00
        buf[35] = 0x33
        buf[36] = 0x02
        buf[37] = 0x77
        buf[38] = 0x01
        buf[39] = 0x9e

        return buf

if __name__ == '__main__':
    s = SixAxis()
    s.connect()
