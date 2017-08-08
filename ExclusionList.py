EXCLUDED_LIST = ["101hotels.ru",
                 "a-hotel.com",
                 "accommodationinczech.",
                 "agoda.com",
                 "albena.bg",
                 "alltherooms.com",
                 "amoma.com",
                 "amfostacolo.ro",
                 "andorraresorts.com",
                 "airbnb.",
                 "arinsal.co.uk",
                 "atrapalo.com",
                 "balkanholidays.",
                 "balkantourbox.com",
                 "beachbulgaria.",
                 "bedandbreakfast.eu",
                 "bedroomvillas.",
                 "belgium-tourism.be",
                 "bestbgproperties.",
                 "bgaccommodations.",
                 "bgstay.com",
                 "booked.net",
                 "booking.com",
                 "booking-hotel-accommoda",
                 "budgetplaces.com",
                 "bulgarholidays.uk",
                 "bulgariabeachresorts.co",
                 "bulgarianestates.org",
                 "bulgarianproperties.",
                 "bulgariatour.cz",
                 "centraldereservas.com",
                 "ceskehory.cz",
                 "chamonix.net",
                 "champtrip.",
                 "chiangdao.com",
                 "cleartrip.com",
                 "czechiatravel.cz",
                 "czechtourism.com",
                 "destination-bg.com",
                 "destinia.",
                 "directbooking.",
                 "directrooms.com",
                 "eatstaylovebulgaria.com",
                 "ebookers.com",
                 "esquiades.com",
                 "europeanexplorer.",
                 "execstays.com",
                 "expats.cz",
                 "expedia.",
                 "facebook.com",
                 "find-bulgaria.com",
                 "findmeahotelroom.com",
                 "firmy.cz",
                 "firstchoice.co.uk",
                 "fischer.cz",
                 "fivestaralliance.com",
                 "getaroom.",
                 "gogo.bg",
                 "goibibo.com",
                 "holidaycheck.de",
                 "holidayhome.cz",
                 "holidaypark.cz",
                 "homeaway.co.uk",
                 "hotel-board.com",
                 "hostelbookers.",
                 "hostelscentral.com",
                 "hoteles.com",
                 "hostelsclub.com",
                 "hostelworld.",
                 "hotelfizz.com",
                 "hotellook.com",
                 "hotelopia.com",
                 "hotelroomscanner.",
                 "hotels.com",
                 "hotels.guide-bulgaria.c",
                 "hotels-in-bulgaria.com",
                 "hotelscombined.",
                 "hotelsclick.com",
                 "hotel.",
                 "hotelchains.",
                 "hotels.",
                 "hotelseurope.com",
                 "hikersbay.",
                 "hrs.",
                 "ihr24.com",
                 "infotel.co.uk",
                 "investbulgaria.com",
                 "ixigo.com",
                 "j2ski.com",
                 "jetcost.co.uk",
                 "kayak.",
                 "krapets.com",
                 "lastminute.com",
                 "leadingcourses.com",
                 "letsbookhotel.com",
                 "limba.com",
                 "logitravel.co.uk",
                 "lonelyplanet.",
                 "loveholidays.com",
                 "makemytrip.com",
                 "mountvacation.co.uk",
                 "novinite.com",
                 "noviteimoti.com",
                 "odalys-vacances.com",
                 "odalys-vacation-rental.",
                 "old33.hotelsbg.net",
                 "onetwotrip.",
                 "orbitz.com",
                 "oyster.com",
                 "pension.cz",
                 "paradise.ro",
                 "pinterest.",
                 "plaja.ro",
                 "plovdivhotels.com",
                 "priceline.",
                 "purpletravel.co.uk",
                 "quehoteles.com",
                 "readytotrip.com",
                 "reinisfischer.com",
                 "rentalhomes.com",
                 "rentbyowner.",
                 "renthome.bg",
                 "riu.com",
                 "rivierabulgaria.com",
                 "rome2rio.",
                 "roomdi.com",
                 "roomex.com",
                 "rooms.bg",
                 "rumbo.",
                 "sefibo.",
                 "shutterstock.",
                 "skiffor.com",
                 "skiplagged.",
                 "slevomat.cz",
                 "soyoutravel.com",
                 "star-tur.com",
                 "sunshine.co.uk",
                 "thomson.co.uk",
                 "tiscover.com",
                 "tophotels.org",
                 "tourister.ru",
                 "travelguru.com",
                 "travelko.com",
                 "travelocity.com",
                 "travelpoint-bg.com",
                 "travelport.cz",
                 "travelrepublic.co.uk",
                 "travelweekly.com",
                 "tripadvisor.",
                 "tripvizor.",
                 "tripwise.eu",
                 "trivago.",
                 "tropki.com",
                 "turistika.cz",
                 "ultimate-ski.com",
                 "viamichelin.com",
                 "visitbulgaria.net",
                 "volagratis.com",
                 "vyletnik.cz",
                 "wego.",
                 "wegotravel.",
                 "wikipedia.",
                 "wiztours.com",
                 "yatra.com",
                 "yelp.",
                 "youtube.com"]


def is_excluded(url):
    ret = False
    for site in EXCLUDED_LIST:
        if site in url:
            ret = True
            break
    return ret
