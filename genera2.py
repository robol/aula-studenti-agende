#!/usr/bin/env python3

import json, datetime, sys

import requests, browser_cookie3, json

cj = browser_cookie3.chrome(domain_name = "agende.unipi.it")

def add_slot(custom_id, text, start, end, maxBookings, booking_start, booking_end):
    data = {
        "customId": custom_id,
        "slotText": text,
        "slotStart": start,
        "slotEnd": end,
        "maxBookings": maxBookings,
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

    return res['success']


def crea_appuntamenti(customId, inizio, fine):
    ora_inizio_mattina = datetime.timedelta(hours = 7, minutes = 00)
    ora_fine_mattina   = datetime.timedelta(hours = 11, minutes = 30)
    ora_inizio_pomeriggio = datetime.timedelta(hours = 12, minutes = 00)
    ora_fine_pomeriggio = datetime.timedelta(hours = 17, minutes = 30)
    giorno = datetime.timedelta(days = 1)
    ora = datetime.timedelta(hours = 1)
    anticipo_prenotazioni = datetime.timedelta(days = 2, hours = 2)
    maxBookings = 45

    success = True
    
    while inizio <= fine:
        if inizio.weekday() < 5:
            text = "Mattina - %s" % inizio.strftime("%d/%m/%y")
            success = success and add_slot(customId, text,
                                           (inizio + ora_inizio_mattina).isoformat(),
                                           (inizio + ora_fine_mattina).isoformat(),
                                           maxBookings,
                                           (inizio - anticipo_prenotazioni).isoformat(),
                                           (inizio + ora_fine_mattina).isoformat())
            print("Aggiunto %s" % text)
            
            if not success:
                return False

            text = "Pomeriggio - %s" % inizio.strftime("%d/%m/%y")
            success = success and add_slot(customId, text,
                                           (inizio + ora_inizio_pomeriggio).isoformat(),
                                           (inizio + ora_fine_pomeriggio).isoformat(),
                                           maxBookings,
                                           (inizio - anticipo_prenotazioni).isoformat(),
                                           (inizio + ora_fine_pomeriggio).isoformat())
            print("Aggiunto %s" % text)
            
            if not success:
                return False
            

        inizio = inizio + giorno
    
    return success
    

if __name__ == "__main__":

    data_inizio = datetime.datetime.fromisoformat(sys.argv[2])
    data_fine   = datetime.datetime.fromisoformat(sys.argv[3])
    customid = sys.argv[1]

    app = crea_appuntamenti(customid, data_inizio, data_fine)

    
