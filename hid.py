descriptor = [
    0x05, 0x01, # Usage Page (Generic Desktop Ctrls)
    0x09, 0x02, # Usage (Mouse)
    0xA1, 0x01, # Collection (Application)
    0x85, 0x01, #   Report ID (1)
    0x09, 0x01, #   Usage (Pointer)
    0xA1, 0x00, #   Collection (Physical)
    0x05, 0x09, #     Usage Page (Button)
    0x19, 0x01, #     Usage Minimum (1)
    0x29, 0x03, #     Usage Maximum (3)
    0x14,       #     Logical Minimum (0)
    0x25, 0x01, #     Logical Maximum (1)
    0x75, 0x01, #     Report Size (1)
    0x95, 0x03, #     Report Count (3)
    0x81, 0x02, #     Input (Data,Var,Abs)
    0x75, 0x05, #     Report Size (5)
    0x95, 0x01, #     Report Count (1)
    0x81, 0x01, #     Input (Const,Array,Abs)
    0x05, 0x01, #     Usage Page (Generic Desktop Ctrls)
    0x09, 0x30, #     Usage (X)
    0x09, 0x31, #     Usage (Y)
    0x15, 0x81, #     Logical Minimum (-127)
    0x25, 0x7F, #     Logical Maximum (127)
    0x75, 0x08, #     Report Size (8)
    0x95, 0x02, #     Report Count (2)
    0x81, 0x06, #     Input (Data,Var,Rel)
    0x09, 0x38, #     Usage (Wheel)
    0x95, 0x01, #     Report Count (1)
    0x81, 0x06, #     Input (Data,Var,Rel)
    0xC0,       #   End Collection
    0xC0,       # End Collection
    0x09, 0x06, # Usage (Keyboard)
    0xA1, 0x01, # Collection (Application)
    0x85, 0x02, #   Report ID (2)
    0x75, 0x01, #   Report Size (1)
    0x95, 0x08, #   Report Count (8)
    0x05, 0x07, #   Usage Page (Kbrd/Keypad)
    0x19, 0xE0, #   Usage Minimum (224)
    0x29, 0xE7, #   Usage Maximum (231)
    0x14,       #   Logical Minimum (0)
    0x25, 0x01, #   Logical Maximum (1)
    0x81, 0x02, #   Input (Var)
    0x95, 0x01, #   Report Count (1)
    0x75, 0x08, #   Report Size (8)
    0x81, 0x03, #   Input (Const,Var)
    0x95, 0x05, #   Report Count (5)
    0x75, 0x01, #   Report Size (1)
    0x05, 0x08, #   Usage Page (LED)
    0x19, 0x01, #   Usage Minimum (Num Lock)
    0x29, 0x05, #   Usage Maximum (Kana)
    0x91, 0x02, #   Output (Var)
    0x95, 0x01, #   Report Count (1)
    0x75, 0x03, #   Report Size (3)
    0x91, 0x03, #   Output (Const, Var) --- 3b PADDING
    0x95, 0x06, #   Report Count (6)
    0x75, 0x08, #   Report Size (8)
    0x25, 0x65, #   Logical Maximum (101)
    0x05, 0x07, #   Usage Page (Kbrd/Keypad)
    0x18,       #   Usage Minimum (Keyboard No Event)
    0x29, 0x65, #   Usage Maximum (Keyboard Application)
    0x81, 0x00, #   Input
    0xC0,       # End Collection
]

def get_report_descriptor():
    return ''.join(['{:02x}'.format(i) for i in descriptor])


if __name__ == '__main__':
    print(get_report_descriptor())
