import socket

class XGT:
    def __init__(self, ip: str, port: int):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))

    def _make_frame(self, rw_mode='r', type='bit', addr=''):
        '''
        Generate frame to send PLC.

        Parameters:
            rw_mode: Read / Write mode. Can be [r, w]

            type: Data Type. Can be [bit, byte, word, dword, lword, seq]
        
        Returns:
            List
        '''
        assert rw_mode in ['r', 'w']
        assert type in ['bit', 'byte', 'word', 'dword', 'lword', 'seq']
        assert addr != ''

        frame = []

        frame.extend("LSIS-XGT"+[0, 0]) # Company ID
        frame.extend([0x00, 0x00]) # PLC Info
        frame.extend([0xA0]) # CPU Info
        frame.extend([0x33]) # Source of Frame
        frame.extend([0x00, 0x00]) # Invoked ID
        frame.extend([0x0E, 0x00]) # Length
        frame.extend([0x00]) # Position
        frame.extend([0x00]) # Checksum

        # Command
        if rw_mode == 'r':
            frame.extend([0x54, 0x00])
        elif rw_mode == 'w':
            frame.extend([0x58, 0x00])

        # Data Type
        if type == 'bit':
            frame.extend([0x00, 0x00])
        elif type == 'byte':
            frame.extend([0x01, 0x00])
        elif type == 'word':
            frame.extend([0x02, 0x00])
        elif type == 'dword':
            frame.extend([0x03, 0x00])
        elif type == 'lword':
            frame.extend([0x04, 0x00])
        elif type == 'seq':
            frame.extend([0x14, 0x00])

        frame.extend([0x00, 0x00]) # Reserved
        frame.extend([0x01, 0x00]) # Block No.
        frame.extend([0x04, 0x00]) # Variable Length
        frame.extend([0x25, 0x40, 0x57, 0x30]) # Data Address

        return frame
    
    def read(self, type='bit', addr=''):
        frame = self._make_frame(rw_mode='r', type=type, addr=addr)
        self.s.send(frame)
        companyId = self.s.recv(10)
        PLCinfo = self.s.recv(2)
        CPUinfo = self.s.recv(1)
        sourceOfFrame = self.s.recv(1)
        invokedId = self.s.recv(2)
        length = self.s.recv(2)
        position = self.s.recv(1)
        checksum = self.s.recv(1)
        command = self.s.recv(2)
        dataType = self.s.recv(2)
        reserved = self.s.recv(2)
        errorState = self.s.recv(2)
        varLength = self.s.recv(2)
        dataCount = self.s.recv(2)
        data = self.s.recv(2)

        return {
            'companyId': '',
            'PLCinfo': {
                'CPUtype': '',
                'duplex': '',
                'CPUstate': '',
                'systemState': ''
            },
            'CPUinfo': '',
            'sourceOfFrame': '',
            'invokeId': 0,
            'length': 0,
            'position': {
                'slot': 0,
                'base': 0
            }
        }
    
    def close(self):
        self.s.close()