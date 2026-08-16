#!/bin/bash

# Standort für die Sonnenauf-/-untergangsberechnung (Bad Salzuflen)
# Benoetigt das Paket "sunwait" (apt install sunwait)
LAT="52.0833N"
LON="8.7667E"

# Nachts (nach Sonnenuntergang bis Sonnenaufgang) nur Helligkeitsstufe 0,
# tagsueber die uebliche Helligkeit.
current_brightness() {
    if [ "$(sunwait poll "$LAT" "$LON")" = "NIGHT" ]; then
        echo 0
    else
        echo 1
    fi
}

# Funktion, um die Temperatur zu aktualisieren
# (hier Platzhalter- steckt bei euch z.B. eine Abfrage an eine Hausautomation)
update_temperature() {
    #temp=$(curl -s 'http://your-home-automation/...' | ...)
    last_update=$(date +%s)
}

# Funktion zum Anzeigen der Uhrzeit
display_time() {
    for i in {1..5}; do
        dcled -b $1 --clock24h
    done
}

# Funktion zum Anzeigen des Wochentags, gross und mittig, ohne zu scrollen.
display_weekday() {
    case "$(date +%u)" in
        1) wd="Mo" ;;
        2) wd="Di" ;;
        3) wd="Mi" ;;
        4) wd="Do" ;;
        5) wd="Fr" ;;
        6) wd="Sa" ;;
        7) wd="So" ;;
    esac
    dcled -b $1 -f -s $2 -m "$wd"
}

# Funktion zum Anzeigen des Datums, gross und mittig, ohne zu scrollen.
display_date() {
    dcled -b $1 -f -s $2 -m "$(date +%d.%m)"
}

# Funktion zum Anzeigen der Temperatur
#display_temperature() {
#    for i in {1..2}; do
#        echo "$1" | dcled -b $2 -s $3
#    done
#}

# Initialisierung der Variablen
last_update=0
temp=""

while true; do
    UhrzeitStunde=$(date +%H)
    Brightness=$(current_brightness)
    Speed=40
    current=1

    # Überprüfen, ob 30 Minuten (1800 Sekunden) vergangen sind
    current_time=$(date +%s)
    if [ $(($current_time - $last_update)) -ge 1800 ]; then
        update_temperature
    fi

    # Anzeige der Uhrzeit
    display_time ${Brightness}

    # Anzeige des Wochentags
    display_weekday ${Brightness} 3000

    # Anzeige der Temperatur
 #   display_temperature "${temp}" ${Brightness} 60

    # Wiederholte Anzeige der Uhrzeit
    display_time ${Brightness}

    # Anzeige des Datums
    display_date ${Brightness} 3000

    # Weitere Logik kann hier eingefügt werden...
done

