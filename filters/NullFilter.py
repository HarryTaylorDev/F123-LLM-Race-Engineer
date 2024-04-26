from datetime import timedelta
from ctypes import Array
import datetime
import logging
from typing import cast, Dict, Optional
import logging
import utilities.data as du

from filters.Filter import Filter
from packets.packets import (Packet, SessionHistoryPacket,SessionPacket, ParticipantsPacket)

from constants.constants import (
    DRIVER_NAMES, EventStringCode, NULL_BYTE_VALUE, PenaltyId, SESSION_TEXT,
    TRACK_NAMES, WEATHER_TEXT)

from packets.packet_data import (
    LapDataData, LapHistoryData,LobbyInfoData, FastestLap, ParticipantsData,CarStatusData,CarTelemetryData,CarDamageData, Penalty,
    RaceWinner, Retirement, StartLights, StopGoPenaltyServed)


def get_driver_name(driver_id: int, fallback_name: str) -> str:
    try:
        return DRIVER_NAMES[driver_id]
    except KeyError:
        pass
    return fallback_name

def print_with_session_timestamp(timestamp: float, string: str):
    time_string = (str(datetime.timedelta(seconds=timestamp))[:-3] if
                   timestamp != 0 else '0:00:00.000')
    logging.info(f'[{time_string}] {string}')
    
def create_time_of_day_string(timestamp: int) -> str:
    return str(datetime.timedelta(minutes=timestamp))



class NullFilter(Filter):
    def __init__(self):
        self.data = {}
        self.session_displayed = False
        self.participants: Optional[Array[ParticipantsData]] = None

    def _get_driver_name(self, vehicle_index: int):
        participant = cast(Array[ParticipantsData],
                           self.participants)[vehicle_index]
        return get_driver_name(
            participant.driverId, du.to_string(participant.name))

    def filter_lap_data(self, packet):
        """
        Process lap data packets.
        """
        driver_id = packet.playerCarIndex  # Corrected attribute access
        lap_number = packet.currentLapNum
        lap_time = packet.lastLapTime

        if driver_id not in self.lap_history:
            self.lap_history[driver_id] = []

        self.lap_history[driver_id].append((lap_number, lap_time))

    def cleanup(self):
        """
        Cleanup method (optional).
        """
        # Save or process lap history data before closing the application
        print("Lap history recorded:", self.lap_history)

if __name__ == "__main__":
    # Example usage
    filter_instance = LapHistoryFilter()
    filter_instance.run()
