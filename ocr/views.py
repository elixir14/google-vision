import os
from logging import getLogger

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

from .constants import CardSide
from .cloud_vision import VisionApi
from .models import ScannedCardMaster, ScannedCardDetail
from .serializers import ScannedCardMasterSerializer, ScannedCardDetailSerializer
from .utils import get_ocr_data
from .predictions import predicate_item
logger = getLogger(__name__)

# Create your views here.


def get_card_ocr_data(scanned_card_master=None):
    if scanned_card_master is None:
        logger.error("scanned_card_master is not initialized")
        raise Exception("Scanned card object is not initialized.")
    card_files = {}
    if scanned_card_master.card_front.name:
        card_files[os.path.join(settings.MEDIA_URL, scanned_card_master.card_front.name)] = CardSide.FRONT
    if scanned_card_master.card_back.name:
        card_files[os.path.join(settings.MEDIA_URL, scanned_card_master.card_back.name)] = CardSide.BACK


    if card_files:
        card_ocr_data = []
        response_data = get_ocr_data(images=card_files.keys())
        for file_path, descriptions in response_data.iteritems():
            if file_path in card_files.keys():
                card_ocr_data.append({card_files.get(file_path) : descriptions})
        return card_ocr_data
    else:
        logger.error("file_list is not empty")
        raise Exception("No scanned card found.")


def process_scanned_data_item(scanned_card_master, item):
    scanned_card_detail = ScannedCardDetail()
    scanned_card_detail.scanned_card = scanned_card_master
    scanned_card_detail.text = item[0]
    scanned_card_detail.bounding_cortdinate = str(item[1])
    scanned_card_detail.predicated_caption = predicate_item(item[0])

    #TODO: Implement Prediction logic.
    return scanned_card_detail


@api_view(['POST'])
def scanned_info(request):

    scanned_card_master_serializer = ScannedCardMasterSerializer(data=request.data)
    if not scanned_card_master_serializer.is_valid():
        return Response(scanned_card_master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    scanned_card_master = ScannedCardMaster(**scanned_card_master_serializer.validated_data)
    scanned_card_master.save()
    ocr_data_list = get_card_ocr_data(scanned_card_master=scanned_card_master)

    for ocr_data in ocr_data_list:
        for card_side, descriptions in ocr_data.iteritems():
            for item in descriptions:
                if not item:
                    continue
                scanned_card_detail = process_scanned_data_item(scanned_card_master, item)
                scanned_card_detail.card_side = card_side
                scanned_card_detail.save()
    details = ScannedCardDetailSerializer(ScannedCardDetail.objects.filter(
        scanned_card=scanned_card_master), many=True)

    return Response(details.data, status=status.HTTP_201_CREATED)


class UserAcceptedViewSet(viewsets.ModelViewSet):
    queryset = ScannedCardDetail.objects.all()

    def update(self, request, pk=None):
        """Update group details.

        Returns:
            Group details with media and group contacts.

        Raises:
            DoesNotExist: An error occurred accessing the group_id.
        """
        group_data = []
        try:
            group_data = self.queryset.get(user_id=request.user.id, id=pk)
            serializer_class = ScannedCardDetailSerializer
        except ScannedCardDetail.DoesNotExist:
            return Response("Scanned card (%s) detail not found" % request.data['id'],
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            if group_data:
                group_updated_data = {}
                group_updated_data = request.data
                group_updated_data['accepted_caption'] = request.data.get("accepted_caption")

                serializer = self.serializer_class(
                    group_data, data=group_updated_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Data cannot be updated', status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response("Internal Error", status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def user_accepted(request):
    """Update user accepted details based on predicted details.

       Returns:
           200 OK response.

       Raises:
           DoesNotExist: An error occurred accessing the scanned_card_detail id.
       """
    try:
        item = request.data
        for item in request.data['data']:
            print item
            scanned_data = ScannedCardDetail.objects.filter(id=item['id']).update(accepted_caption = item['accepted_caption'])
        # scanned_data.accepted_caption = item['accepted_caption']
        # scanned_data.update()
        return Response(status=status.HTTP_200_OK)
        # serializer = ScannedCardDetailSerializer1(data=request.data, many=True)
        # print serializer.initial_data
        # if serializer.is_valid():
        #     print 'VVVVVVV'
        #     serializer.save()
        return Response(status=status.HTTP_200_OK)
        # scanned_data = ScannedCardDetail.objects.get(id=request.data['id'])
        # scanned_data.accepted_caption = request.data['accepted_caption']
        # scanned_data.save()
    except Exception, ex:
        return Response("Scanned card (%s) detail not found" % ex.message,
                        status=status.HTTP_400_BAD_REQUEST)

    scanned_card_detail_serializer = ScannedCardDetailSerializer(data=request.data, partial=True)

    if scanned_card_detail_serializer.is_valid():
        scanned_card_detail_serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(scanned_card_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def predictive_accuracy(request):
    return Response("ddd", status=status.HTTP_200_OK)