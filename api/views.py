from itertools import groupby
from operator import itemgetter

from rest_framework.response import Response

from rest_framework.views import APIView

from .models import (
        Airplane,
        BoardingPass,
        Flight,
        Passenger,
        Purchase,
        Seat,
        SeatType
)

from .serializers import (
    PassengerSerializer,
    PurchaseSerializer,
    AirplaneSerializer,
    SeatTypeSerializer,
    SeatSerializer,
    FlightSerializer,
    BoardingPassSerializer
)


def getInfoSeat(idAsiento):
    """Obtiene información del asiento del pasajero"""
    seatSerializado = SeatSerializer(
            Seat.objects.filter(seat_id__in=[idAsiento]),
            many=True
        ).data
    return seatSerializado[0]


def setAsiento(posicion, dataPasajero, lista):
    """Establece los asientos en la lista y en 'setId' del pasajero"""
    boxLetra = lista[posicion[0]]
    ubicacion = posicion[1]
    if ubicacion not in boxLetra:
        boxLetra.append(ubicacion)
        dataPasajero['seatId'] = ubicacion
    else:
        boxLetra.append(ubicacion + 1)
        dataPasajero['seatId'] = ubicacion + 1
    return dataPasajero


def checkSeatConsecutivos(filaAsiento, listaPasajeros, numeroPurchase):
    """
    Comprueba y retorna lista de asientos disponibles.
    Retorna lista con booleano y diccionario {letra: [asientos_disponible]}.
    Ordenada de Menor a MAyor, la cantidad de espacios vacíos
    """
    check = False
    dictNumeros = {}
    for key, numerosFila in filaAsiento.items():
        if len(numerosFila) > len(listaPasajeros):
            for k, g in groupby(enumerate(numerosFila), lambda ix: ix[0] - ix[1]):
                x = list(map(itemgetter(1), g))
                if len(x) >= len(listaPasajeros):
                    if key not in dictNumeros.keys():
                        dictNumeros[key] = x
    if len(list(dictNumeros.keys())):
        check = True
    return [check, sortMayorMenorAsiento(dictNumeros, False)]


def sortMayorMenorAsiento(sinAsiento_Dict, boolReverse):
    """
    Ordena por cantidad de pasajeros sin asiento.
    Recibe un diccionario y un booleano.
    """
    # print(type(sinAsiento_Dict))
    return dict(
            sorted(
                sinAsiento_Dict.items(),
                key=lambda k: len(k[1]),
                reverse=boolReverse
            )
        )


def checkAsientosCompatibles(listaPasajeros):
    """
    Comprueba si grupo contiene almenos 1 asiento
    Retorna una lista: True/False y lista ordenada, valores None al final.
    """
    check = []
    ordenados = sorted(
            listaPasajeros,
            key=lambda x: -x['seatId']
            if x['seatId'] is not None else
            float('inf')
        )
    # print(ordenados)
    for item in ordenados:
        if item['seatId'] is None:
            check.append(False)
        else:
            check.append(True)
        # print(item['seatId'])
    return [any(check), ordenados]


def setIdSeatPassenger(idColumnRowSeat, pasajeros):
    """
    Establece seatID y columnID a pasajero.
    Retorna una lista de los pasajeros actualizada.
    """
    idSeat = idColumnRowSeat[0]
    columna = idColumnRowSeat[1]
    asientos = idColumnRowSeat[2]
    # print(idSeat, columna, asientos)

    for i in range(len(pasajeros)):
        pasajeros[i]['seatId'] = idSeat[i]
        # pasajeros[i]['seatColumn'] = columna
    return pasajeros


def getSeatID(letra, posicionGrupo, avionId):
    """Obtiene ID de 'Seat'"""
    # print(letra, posicionGrupo, avionId)
    asientos = Seat.objects.filter(
                    airplane_id=avionId
                    ).filter(
                        seat_column=letra
                    ).filter(
                        seat_row__in=posicionGrupo
                    )
    data = SeatSerializer(asientos, many=True).data
    columnSeat = [item['seatColumn'] for item in data][0]
    rowSeat = [item['seatRow'] for item in data]
    idSeat = [item['seatId'] for item in data]
    return (idSeat, columnSeat, rowSeat)


def establecerAsientos(dictPasajeros, tipoAsiento, avionId, infoListaAsientos):
    """Lógica para establecer asiento en lista y en datos del pasajero"""
    # print(tipoAsiento)#, avionId)

    listaAsientoCate = infoListaAsientos[tipoAsiento]
    letrasColumnas = list(listaAsientoCate.keys())[2:]
    rango = listaAsientoCate['rango']
    limite = listaAsientoCate['limite']

    llavesPurchaseID = list(dictPasajeros.keys())
    necesitaAsientos = {}

    for id in llavesPurchaseID:
        ubicacion_seat = []

        almenosUnSeat, listaPasajeros = checkAsientosCompatibles(
                                            dictPasajeros[id]
                                        )
#
#  Se ubican todos los pasajeros con todos o almenos 1 asiento asignado
#  los que tienen el mismo 'purchaseId' se sientan en la misma fila.
#
        if almenosUnSeat:
            for item in listaPasajeros:
                # try:
                #     print(item['seatId'], item['seatColumn'])
                # except Exception:
                #     pass
                if item['purchaseId'] == id:
                    # SI tengo un 'seatColumn' tengo un 'seatId'
                    # y viceversa
                    if 'seatColumn' in item.keys():

                        ubicacion_seat = [
                            item['seatColumn'],
                            item['seatRow'],
                            item['seatRow'],
                        ]

                        listaAsientoCate[
                            item['seatColumn']
                        ].append(item['seatRow'])

                    else:

                        if ubicacion_seat[1] + 1 >= rango[1]:
                            ubicacion_seat = [
                                ubicacion_seat[0],
                                ubicacion_seat[2] - 1,
                                ubicacion_seat[2],
                            ]
                        elif ubicacion_seat[1] + 1 < rango[1]:
                            ubicacion_seat = [
                                ubicacion_seat[0],
                                ubicacion_seat[1] + 1,
                                ubicacion_seat[2],
                            ]

                        listaAsientoCate[ubicacion_seat[0]].append(
                            ubicacion_seat[1]
                            )

                        idSeatPasajero = getSeatID(
                                            letra=ubicacion_seat[0],
                                            posicionGrupo=[ubicacion_seat[1]],
                                            avionId=avionId
                                        )

                        idSeat = idSeatPasajero[0][0]
                        columna = idSeatPasajero[1]
                        filaNumero = idSeatPasajero[2][0]

                        item['seatId'] = idSeat
                else:
                    ubicacion_seat.clear()
        else:
            if id not in necesitaAsientos.keys():
                necesitaAsientos[id] = listaPasajeros

    necesitaAsientos = sortMayorMenorAsiento(necesitaAsientos, True)

    # asignados = []
    for key, pasajerosLista in necesitaAsientos.items():
        ids = [i['purchaseId'] for i in pasajerosLista]
        idGrupo = ids[0]
        asignados = []
        for letra in letrasColumnas:
            fila = listaAsientoCate[letra]
            tamanoPasajeros = len(pasajerosLista)
            sizeFilaAsiento = len(listaAsientoCate[letra])

            if idGrupo in asignados:
                break
            else:
                nueva = fila + ids

                if len(nueva) <= limite:
                    # asignados.append(idGrupo)
                    # print(nueva, len(nueva), limite, rango[1])
                    listaAsientoCate[letra] = nueva

                    x = listaAsientoCate[letra].index(idGrupo)
                    y = x + len(pasajerosLista)
                    posiciones = [i for i in range(rango[0], rango[1])][x:y]
                    # print(idGrupo, x, y, posiciones)

                    idSeatPasajero = getSeatID(
                                            letra,
                                            posiciones,
                                            avionId
                                        )
                    # print(idSeatPasajero)

                    pasajerosActualizados = setIdSeatPassenger(
                                                idSeatPasajero,
                                                pasajerosLista
                                            )
                    dictPasajeros[key] = []
                    dictPasajeros[key] = pasajerosActualizados
                    asignados.append(idGrupo)

    return dictPasajeros


def dataPassenger(lista):
    """
    Obtiene data pasajeros, retorna 'dict' ordenado acendentemente y
    agrupados por 'purchase_id'.
    """
    data = {}
    for item in lista:
        if item['seatId'] is not None:
            passengerItem = PassengerSerializer(Passenger.objects.get(passenger_id=item['passengerId'])).data
            seatItem = SeatSerializer(Seat.objects.get(seat_id=item['seatId'])).data
            item.update(passengerItem)
            item.update(seatItem)
        else:
            passengerItem = PassengerSerializer(Passenger.objects.get(passenger_id=item['passengerId'])).data
            item.update(passengerItem)

    ids = sorted(set([i['purchaseId'] for i in lista]), key=int)
    # print(ids)
    for id in ids:
        for item in lista:
            if item['purchaseId'] == id:
                if id not in data.keys():
                    data[id] = [item]
                else:
                    data[id].append(item)
    return data


def structureDataResponse(vueloData, dataLista):
    """
    Retorna la respuesta de API con estructura requerida.
    """

    response = {
        'flightId': vueloData['flightId'],
        'takeoffDateTime': vueloData['takeoffDateTime'],
        'takeoffAirport': vueloData['takeoffAirport'],
        'landingDateTime': vueloData['landingDateTime'],
        'landingAirport': vueloData['landingAirport'],
        'airplaneId': vueloData['airplane']['airplaneId'],
        'passengers': []
    }
    for item in dataLista:
        for k, itemPasajeros in item.items():
            for elemento in itemPasajeros:
                dataPasajero = {
                    'passengerId': elemento['passengerId'],
                    'dni': elemento['dni'],
                    'name': elemento['name'],
                    'age': elemento['age'],
                    'country': elemento['country'],
                    'boardingPassId': elemento['boardingPassId'],
                    'purchaseId': elemento['purchaseId'],
                    'seatTypeId': elemento['seatTypeId'],
                    'seatId': elemento['seatId']
                }

                response['passengers'].append(dataPasajero)
    return response


#######################
#  Clase View API
#
class VuelosAPI(APIView):
    """
    Clase API solamente responde 'GET', retorna datos del vuelo y listado de
    pasajeros.
    """
    def get(self, request, vueloID, format='json'):
        airNova_P = {
            # 1 - 4
            'rango': [1, 5],
            'limite': 5 - 1,
            'A': [],
            'B': [],
            'F': [],
            'G': []
        }

        airNova_EP = {
            # 8 - 15
            'rango': [8, 16],
            'limite': 16 - 8,
            'A': [],
            'B': [],
            'C': [],
            'E': [],
            'F': [],
            'G': []
        }

        airNova_E = {
            # 19 - 34
            'rango': [19, 35],
            'limite': 35 - 19,
            'A': [],
            'B': [],
            'C': [],
            'E': [],
            'F': [],
            'G': []
        }

        airMax_P = {
            # 1 - 5
            'rango': [1, 6],
            'limite': 6 - 1,
            'A': [],
            'E': [],
            'I': []
        }

        airMax_EP = {
            # 9 - 14
            'rango': [9, 15],
            'limite': 15 - 9,
            'A': [],
            'B': [],
            'D': [],
            'E': [],
            'F': [],
            'H': [],
            'I': []
        }
        airMax_E = {
            # 18 - 31
            'rango': [18, 32],
            'limite': 32 - 18,
            'A': [],
            'B': [],
            'D': [],
            'E': [],
            'F': [],
            'H': [],
            'I': []
        }

        avionesDict = {
            1: {
                'premium': airNova_P,
                'eco_premium': airNova_EP,
                'eco': airNova_E
            },
            2: {
                'premium': airMax_P,
                'eco_premium': airMax_EP,
                'eco': airMax_E
            },
        }

        categoriaAsiento = {
            1: 'premium',
            2: 'eco_premium',
            3: 'eco'
        }

        if vueloID == 0:
            return Response({'code': 404, 'data': {}}, status=404)
        else:
            vuelo = Flight.objects.filter(flight_id=vueloID)
            existe = vuelo.exists()
            if not existe:
                return Response({'code': 404, 'data': {}}, status=404)
            else:
                vueloSerializer = FlightSerializer(vuelo, many=True).data[0]
                idAvion = vueloSerializer['airplane']['airplaneId']
                dataAvionDict = avionesDict[idAvion]

                boardingPass = BoardingPass.objects.filter(
                                flight_id=vueloID
                            ).order_by('-purchase_id')

                premiumData = BoardingPassSerializer(boardingPass.filter(seat_type_id=1), many=True).data
                ecoPremiumData = BoardingPassSerializer(boardingPass.filter(seat_type_id=2), many=True).data
                ecoData = BoardingPassSerializer(boardingPass.filter(seat_type_id=3), many=True).data

                pasajerosPremium = dataPassenger(premiumData)
                pasajerosEcoPremium = dataPassenger(ecoPremiumData)
                pasajerosEco = dataPassenger(ecoData)

                # # # #    Premium
                pasajerosPremium = establecerAsientos(
                    dictPasajeros=pasajerosPremium,
                    tipoAsiento=categoriaAsiento[1],
                    avionId=idAvion,
                    infoListaAsientos=dataAvionDict
                )
                # # # # #    Económico Premium
                pasajerosEcoPremium = establecerAsientos(
                    dictPasajeros=pasajerosEcoPremium,
                    tipoAsiento=categoriaAsiento[2],
                    avionId=idAvion,
                    infoListaAsientos=dataAvionDict
                )
                # # # #    Económico
                pasajerosEco = establecerAsientos(
                    dictPasajeros=pasajerosEco,
                    tipoAsiento=categoriaAsiento[3],
                    avionId=idAvion,
                    infoListaAsientos=dataAvionDict
                )

                listaDatosPasajeros = [
                            pasajerosPremium,
                            pasajerosEcoPremium,
                            pasajerosEco
                        ]

                responseDataAPI = structureDataResponse(
                                            vueloSerializer,
                                            listaDatosPasajeros
                                        )

                return Response(
                            {'code': 200, 'data': responseDataAPI},
                            status=200
                        )
