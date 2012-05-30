import json
import urllib
from xml.dom.minidom import parseString

def getconcerts(artist, state = 'CA'):
    cell = []
    url = "http://api.jambase.com/search?state=" + state + "&band=" + artist + "&apikey=7w7rfp6khsqd6hfcf6gwvu5j"
    response = urllib.urlopen(url)
    data = response.read()
    response.close()
    dom = parseString(data)
    if dom.getElementsByTagName("errorNode") == []:
        if dom.getElementsByTagName("event_date") and dom.getElementsByTagName("venue_name") and dom.getElementsByTagName("venue_city") and dom.getElementsByTagName("ticket_url"):
            cell.append(artist)
            cell.append(dom.getElementsByTagName("event_date")[0].toxml().replace('<event_date>', '').replace('</event_date>',''))
            cell.append(dom.getElementsByTagName("venue_name")[0].toxml().replace('<venue_name>', '').replace('</venue_name>',''))
            cell.append(dom.getElementsByTagName("venue_city")[0].toxml().replace('<venue_city>', '').replace('</venue_city>','') + ", " + state)
            cell.append(dom.getElementsByTagName("ticket_url")[0].toxml().replace('<ticket_url>', '').replace('</ticket_url>',''))
    return cell