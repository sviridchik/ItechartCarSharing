from django.shortcuts import render


# Create your views here.
class TripList(RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = (IsAuthenticated)

    # -------------- trip price ---------------------


class TripPriceList(CreateAPIView):
    queryset = TripPrice.objects.all()
    serializer_class = TripPriceSerializer
    permission_classes = (IsAuthenticated)

    def get(self, request, format=None):
        trip = TripPrice.objects.all()
        serializer = TripPriceSerializer(trip, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TripPriceListDetail(APIView):
    queryset = TripPrice.objects.all()
    serializer_class = TripPriceSerializer
    permission_classes = (IsAuthenticated)

    def get_object(self, pk):
        try:
            return TripPrice.objects.get(pk=pk)
        except TripPrice.DoesNotExist:
            return Response({"error": "there is no such price"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        car = self.get_object(pk)
        serializer = TripPriceSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        car = self.get_object(pk)

        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------- trip log ---------------------
class LogList(CreateAPIView):
    queryset = TripLog.objects.all()
    serializer_class = TripLogSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        trip = TripLog.objects.all()
        serializer = TripLogSerializer(trip, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
