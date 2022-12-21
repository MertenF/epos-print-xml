def parse_code(asb: int) -> [str]:
    msg = []
    if asb & 0x00000001:
        msg.append('No printer response')
    if asb & 0x00000002:
        msg.append('Printing is succssfully completed')
    if asb & 0x00000004:
        msg.append('Status of the drawer kick number 3 connector pin = "H"')
    if asb & 0x00000008:
        msg.append('Offline status')
    if asb & 0x00000020:
        msg.append('Cover is open')
    if asb & 0x00000040:
        msg.append('Paper feed switch is feeding paper')
    if asb & 0x00000100:
        msg.append('Waiting for online recovery')
    if asb & 0x00000200:
        msg.append('Panel switch is ON')
    if asb & 0x00000400:
        msg.append('Mechanical error generated')
    if asb & 0x00000800:
        msg.append('Auto cutter error generated')
    if asb & 0x00002000:
        msg.append('Unrecoverable error generated')
    if asb & 0x00004000:
        msg.append('Auto recovery error generated')
    if asb & 0x00010000:
        msg.append('Waiting for insertion of a slip sheet for slip printing')
    if asb & 0x00020000:
        msg.append('Roll paper has almost run out')
    if asb & 0x00040000:
        msg.append('Waiting for ejection of a slip sheet for slip printing')
    if asb & 0x00080000:
        msg.append('Roll paper has run out')
    if asb & 0x01000000:
        msg.append('Buzzer is sounding OR Waiting for paper removal')
    if asb & 0x80000000:
        msg.append('No paper is detected with the paper removal detector ')
    if asb & 0x80000000:
        msg.append('Spooler stopped')

    return msg


if __name__ == '__main__':
    print(parse_code(0))
    print(parse_code(252641308))
    print(parse_code(251658268))
