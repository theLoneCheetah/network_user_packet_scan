import pytest
from random import randint
from packet_scan_handler import PacketScanHandler
from database_manager import DatabaseManager, SwitchPortData
from L2_switch import L2Switch
from my_exception import MyException, ExceptionType


# mock class as a database manager
class FakeDatabaseManager(DatabaseManager):
    # init by defined data without real connection
    def __init__(self, test_data):
        self.test_data = test_data

    # get these data
    def get_switch_port(self, usernum: int) -> SwitchPortData:
        return self.test_data[usernum]
    
    # pass while deleting
    def __del__(self) -> None:
        pass

# mock class as a switch manager
class FakeL2Switch(L2Switch):
    # init with some known model without real connection
    def __init__(self, ipaddress, user_port, print_output=False):
        # Пропускаем реальное подключение
        self._ipaddress = ipaddress
        self._model = "DES-3028"

    # return random rx and tx bytes
    def get_packets_port(self):
        return randint(0, 10 ** 8), randint(0, 10 ** 8)
    
    # pass while deleting
    def __del__(self) -> None:
        pass

# some fake data for tests
fake_usernum = 12345
fake_data = {fake_usernum: {"switchP": "192.168.1.100", "PortP": 5}}


# test getting switch and port
def test_get_switch_port_success(monkeypatch):
    # substitute real database with a fake one with fake data
    fake_db = FakeDatabaseManager(fake_data)
    monkeypatch.setattr("packet_scan_handler.DatabaseManager", lambda: fake_db)   # lambda puts this fake object

    # create handler and get switch and port directly
    handler = PacketScanHandler(fake_usernum)
    handler._db_manager = FakeDatabaseManager(fake_data)
    handler._PacketScanHandler__get_switch_port()   # this method gets data from the database

    # check that data received correctly
    assert handler._record_data["switch"] == "192.168.1.100"
    assert handler._record_data["port"] == 5

# test scenario when user is not found and capture output
def test_no_user_in_db(monkeypatch, capsys):
    # fake database that return None when user not found
    class EmptyDB:
        def get_switch_port(self, usernum):
            return None

    # substitute with the fake database object
    monkeypatch.setattr("packet_scan_handler.DatabaseManager", lambda: EmptyDB())

    # create handler and try to start packet statistics
    handler = PacketScanHandler(99999)
    handler.check_packet()   # this method tries to get data from the database

    # capture output, there must be a special exception
    captured = capsys.readouterr()
    assert "Exception while working with the database record:" in captured.out

# test exception when switch is not available with capturing output
def test_switch_unavailable(monkeypatch, capsys):
    # user fake database with fake data
    fake_db = FakeDatabaseManager(fake_data)
    monkeypatch.setattr("packet_scan_handler.DatabaseManager", lambda: fake_db)

    # fake switch manager that always puts unavailability exception
    class UnavailableSwitch:
        def __init__(self, ip, port, print_output=False):
            raise MyException(ExceptionType.SWITCH_NOT_AVAILABLE)

    # use fake switch object
    monkeypatch.setattr("packet_scan_handler.L2Switch", UnavailableSwitch)

    # create handler and try to start packet statistics
    handler = PacketScanHandler(fake_usernum)
    handler.check_packet()   # in __scan_packet method there wiil be exception

    # capture output, there must be two exception messages
    captured = capsys.readouterr()
    assert "Exception while working with equipment:" in captured.out
    assert "L2: свитч недоступен" in captured.out

# test successful packet getting
def test_get_packets_port(monkeypatch):
    # substitute with fake object
    monkeypatch.setattr("packet_scan_handler.L2Switch", FakeL2Switch)
    
    # create handler and use fake switch object
    handler = PacketScanHandler(fake_usernum)
    handler._L2_manager = FakeL2Switch(*fake_data[fake_usernum])

    # get packet statistics directly and check the values
    rx, tx = handler._PacketScanHandler__get_packet_port()   # this method gets rx and tx bytes from the switch manager
    assert 0 <= rx <= 10 ** 8
    assert 0 <= tx <= 10 ** 8

# test 
def test_full_integration(tmp_path, monkeypatch):
    # create temporary file instead of pipe
    test_file = tmp_path / "test_output.txt"
    
    # create handler and substitute real database with a fake one with fake data
    handler = PacketScanHandler(fake_usernum)
    fake_db = FakeDatabaseManager(fake_data)
    monkeypatch.setattr("packet_scan_handler.DatabaseManager", lambda: fake_db)
    
    try:
        # use fake switch manager
        handler._L2_manager = FakeL2Switch(*fake_data[fake_usernum])
        
        # override scanning method for only one iteration
        def limited_scan():
            try:
                # open test file
                with open(test_file, "w", buffering=1) as f:
                    # get packet statistics directly
                    rx, tx = handler._PacketScanHandler__get_packet_port()
                    
                    # convert to megabit
                    rx_mbit = handler._byte_to_megabit(rx)
                    tx_mbit = handler._byte_to_megabit(tx)

                    # write in file
                    f.write(f"{rx_mbit} {rx_mbit} {tx_mbit} {tx_mbit}\n")
                    f.flush()
                
                # imitate sys exit
                raise SystemExit()
            
            # catch and pass to exit
            except SystemExit:
                pass
        
        # substitute with restricted test method
        handler._PacketScanHandler__scan_packet = limited_scan
        
        # start scanning, one iteration
        handler.check_packet()
        
        # read data from file
        with open(test_file, "r") as f:
            line = f.readline().strip()
        
        # check that line contains 4 megabit numbers
        is_valid = lambda s: len(s.split()) == 4 and all(n.isdigit() and 0 <= int(n) <= handler._byte_to_megabit(10**8) for n in s.split())
        assert is_valid(line)
    
    # remove test file if another tests needed
    finally:
        if test_file.exists():
            test_file.unlink()
