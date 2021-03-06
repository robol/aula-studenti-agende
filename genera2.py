#!/usr/bin/env python3

import json, datetime, sys

import requests, browser_cookie3, json

cj = browser_cookie3.chrome(domain_name = "agende.unipi.it")

slots = [
    ( "09:30", "12:00" ),
    ( "12:00", "14:30" ),
    ( "15:00", "17:00" ),
    ( "17:00", "19:00" ),
    ( "19:00", "20:30" )
]

def add_slot(custom_id, text, start, end, maxBookings, booking_start, booking_end):
    data = {
        "customId": custom_id,
        "slotText": text,
        "slotStart": start,
        "slotEnd": end,
        "MaxBookings": int(maxBookings),
        "slotBookingStart": booking_start,
        "slotBookingEnd": booking_end
    }

    headers = {
        "content-type": "application/json",
    }

    cookies = requests.utils.dict_from_cookiejar(cj)

    r = requests.post("https://agende.unipi.it/api/v1.0/Slots/addSlot",
                      data = json.dumps(data),
                      cookies = cookies,
                      headers = headers)

    res = r.json()
    if 'success' in res:
        return res['success']
    else:
        print("Error:")
        print(res)


def crea_appuntamenti(customId, inizio, fine, maxBookings):
    giorno = datetime.timedelta(days = 1)
    anticipo_prenotazioni = datetime.timedelta(days = 2, hours = 1)

    success = True
    while inizio <= fine:
        if inizio.weekday() < 5:
            for slot in slots:
                text = "%s - %s" % (slot[0], slot[1])
                start_h, start_m = slot[0].split(":")
                end_h, end_m = slot[1].split(":")
                slotstart = datetime.timedelta(hours = int(start_h) - 2, minutes = int(start_m))
                slotend   = datetime.timedelta(hours = int(end_h) - 2, minutes = int(end_m))
                success = success and add_slot(customId, "", (inizio + slotstart).isoformat(), 
                                               (inizio + slotend).isoformat(), 
                                               maxBookings, 
                                               (inizio - anticipo_prenotazioni).isoformat(),
                                               (inizio + slotend).isoformat())
                print("Aggiunto %s" % text)

                if not success:
                    return False

        inizio = inizio + giorno
    
    return success
    

if __name__ == "__main__":

    data_inizio = datetime.datetime.fromisoformat(sys.argv[2])
    data_fine   = datetime.datetime.fromisoformat(sys.argv[3])
    customid = sys.argv[1]
    maxbookings = sys.argv[4] if len(sys.argv) > 4 else 45

    app = crea_appuntamenti(customid, data_inizio, data_fine, maxbookings)

    
