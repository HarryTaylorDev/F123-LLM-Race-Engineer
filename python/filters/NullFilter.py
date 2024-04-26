from datetime import timedelta
from ctypes import Array
import datetime
import logging
from typing import cast, Dict, Optional
import logging
import utilities.data as du

from filters.Filter import Filter
from packets.packets import (SessionHistoryPacket, EventPacket, Packet, PacketId, ParticipantsPacket, SessionPacket)

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

    def filter_event(self, packet: EventPacket):
        event_code = du.to_string(packet.eventStringCode)
        if event_code == EventStringCode.SESSION_START.value:
            print_with_session_timestamp(
                packet.sessionTime, 'Race Start Imminent.')
        elif event_code == EventStringCode.SESSION_END.value:
            print_with_session_timestamp(
                packet.sessionTime, 'Race Over')
            self._reset()
        elif event_code == EventStringCode.FASTEST_LAP.value:
            data = cast(FastestLap, packet.eventDetails.FastestLap)
            driver_name = self._get_driver_name(data.vehicleIdx)
            print_with_session_timestamp(
                packet.sessionTime,
                f'{driver_name} has set the fastest lap time of \
{str(datetime.timedelta(seconds=data.lapTime))[3:-3]}.')
        elif event_code == EventStringCode.DRIVE_THROUGH_SERVED.value:
            data = cast(DriveThroughPenaltyServed,
                        packet.eventDetails.DriveThroughPenaltyServed)
            driver_name = self._get_driver_name(data.vehicleIdx)
            print_with_session_timestamp(
                packet.sessionTime,
                f'{driver_name} has served a drive through penalty.')
        elif event_code == EventStringCode.STOP_GO_SERVED.value:
            data = cast(StopGoPenaltyServed,
                        packet.eventDetails.StopGoPenaltyServed)
            driver_name = self._get_driver_name(data.vehicleIdx)
            print_with_session_timestamp(
                packet.sessionTime,
                f'{driver_name} has served a stop-and-go penalty.')

    def filter_participants(self, packet: ParticipantsPacket):
        if self.participants is not None:
            return
        self.participants = packet.participants

    def _reset(self):
        self.participants = None
        self.session_displayed = False