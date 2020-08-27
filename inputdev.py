import struct

try:
    from gi.repository import GObject as gobject
except ImportError:
    import gobject

import evdev as ev
import keymap

class Device:
    def __init__(self, report_id):
        self.state = [
            0xA1, # This is an input report by USB
            report_id, # Report Id assigned for Mouse, in HID Descriptor
        ]
        self.watches = [] # list of watch descriptors to be deleted on disconnect

    def __del__(self):
        for watch in self.watches:
            gobject.source_remove(watch)

    def register_intr_sock(self, sock):
        self.sock = sock

    def hotplug_plug_dev(self, udev_device):
        ev_device = ev.InputDevice(udev_device.get('DEVNAME'))
        ev_device.repeat = ev.device.KbdInfo(repeat=0, delay=0)
        print("Adding new %s" % ev_device)
        watch = gobject.io_add_watch(ev_device, gobject.IO_IN, self.ev_cb)
        # device unplug event:
        gobject.io_add_watch(ev_device, gobject.IO_HUP, self.del_watch, watch)
        if watch not in self.watches:
            self.watches.append(watch)

    def del_watch(self, ev_device, io_type, watch):
        print("Removing %s" % ev_device)
        gobject.source_remove(watch)
        self.watches.remove(watch)
        return False

class Mouse(Device):
    def __init__(self, report_id=0x01):
        Device.__init__(self, report_id)

        self.state.extend([
            # (D7 being the first element, D0 being last)
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ],
            0x00, # X
            0x00, # Y
            0x00, # Wheel
        ])

    def update_state(self):
        event = self.event

        self.state[3] = 0
        self.state[4] = 0
        self.state[5] = 0

        if event.code == ev.ecodes.REL_X:
            self.state[3] = event.value
        elif event.code == ev.ecodes.REL_Y:
            self.state[4] = event.value
        elif event.code == ev.ecodes.REL_WHEEL:
            self.state[5] = event.value
        elif event.code == ev.ecodes.BTN_LEFT:
            self.state[2][7] = event.value
        elif event.code == ev.ecodes.BTN_MIDDLE:
            self.state[2][5] = event.value
        elif event.code == ev.ecodes.BTN_RIGHT:
            self.state[2][6] = event.value

    def ev_cb(self, dev, io_type):
        event = dev.read_one()
        if event.type and event.type in [
                ev.ecodes.EV_REL,
                ev.ecodes.EV_ABS,
                ev.ecodes.EV_KEY
        ]:
            self.event = event
            self.update_state()
            self.sock.send(self.to_bstr())

        return True

    def to_bstr(self):
        # Convert the hex array to a string
        hex_str = b""
        for element in self.state[:3]:
            if type(element) is list:
                # This is our bit array - convert it to a single byte represented
                # as a char
                bin_str = ""
                for bit in element:
                    bin_str += str(bit)
                hex_str += struct.pack("B", int(bin_str, 2))
            else:
                # This is a hex value - we can convert it straight to a char
                hex_str += struct.pack("B", element)

        for element in self.state[3:]:
            if element > 127:
                element = 127

            hex_str += struct.pack("b", element)

        return hex_str

class Keyboard(Device):
    def __init__(self, report_id=0x02):
        Device.__init__(self, report_id)

        self.state.extend([
            # Bit array for Modifier keys
            # (D7 being the first element, D0 being last)
            [
                0,  # Right GUI - (usually the Windows key)
                0,  # Right ALT
                0,  # Right Shift
                0,  # Right Control
                0,  # Left GUI - (again, usually the Windows key)
                0,  # Left ALT
                0,  # Left Shift
                0,  # Left Control
            ],
            0x00, # Vendor reserved
            0x00, # Rest is space for 6 keys
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
        ])

    def update_state(self):
        event = self.event
        try:
            evdev_code = ev.ecodes.KEY[event.code]
        except KeyError:
            print("Unknown event code (%d)" % event.code)
            return

        modkey_element = keymap.modkey(evdev_code)
        if modkey_element > 0:
            # Need to set one of the modifier bits
            if self.state[2][modkey_element] == 0:
                self.state[2][modkey_element] = 1
            else:
                self.state[2][modkey_element] = 0
        else:
            # Get the hex keycode of the key
            hex_key = keymap.convert(ev.ecodes.KEY[event.code])
            # Loop through elements 4 to 9 of the input report structure
            for i in range(4, 10):
                if self.state[i] == hex_key and event.value == 0:
                    # Code is 0 so we need to depress it
                    self.state[i] = 0x00
                elif self.state[i] == 0x00 and event.value == 1:
                    # If the current space is empty and the key is being pressed
                    self.state[i] = hex_key
                    break

    def ev_cb(self, dev, io_type):
        event = dev.read_one()
        if event.type == ev.ecodes.EV_KEY and event.value < 2:
            self.event = event
            self.update_state()
            self.sock.send(self.to_bstr())

        return True

    def to_bstr(self):
        # Convert the hex array to a string
        hex_str = b""
        for element in self.state:
            if type(element) is list:
                # This is our bit array - convert it to a single byte represented
                # as a char
                bin_str = ""
                for bit in element:
                    bin_str += str(bit)
                hex_str += struct.pack("B", int(bin_str, 2))
            else:
                # This is a hex value - we can convert it straight to a char
                hex_str += struct.pack("B", element)

        return hex_str
