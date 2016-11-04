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

logger = getLogger(__name__)

# Create your views here.


def get_ocr_data(images = []):
    vision_api = VisionApi()
    vision_response = vision_api.detect_text(images)
    print vision_response
    locale = ''
    response_data = {}
    for file_path, value in vision_response.iteritems():
        file_path = file_path.replace(settings.MEDIA_URL,'')
        if value:
            response_data[file_path] = value[0]['description'].split('\n')

    return response_data


def get_card_ocr_data(scanned_card_master=None):
    if scanned_card_master is None:
        logger.error("scanned_card_master is not initialized")
        raise Exception("Scanned card object is not initialized.")
    file_list = {}
    if scanned_card_master.card_front.name:
        file_list[os.path.join(settings.MEDIA_URL, scanned_card_master.card_front.name) =
    if scanned_card_master.card_back.name:
        file_list.append(os.path.join(settings.MEDIA_URL, scanned_card_master.card_back.name))

    print file_list

    if file_list:
        card_ocr_data = []
        response_data = get_ocr_data(images=file_list)
        for response_data
    else:
        logger.error("file_list is not empty")
        raise Exception("No scanned card found.")


@api_view(['POST'])
def scanned_info(request):

    scanned_card_master_serializer = ScannedCardMasterSerializer(data=request.data)
    if not scanned_card_master_serializer.is_valid():
        return Response(scanned_card_master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    scanned_card_master = ScannedCardMaster(**scanned_card_master_serializer.validated_data)
    scanned_card_master.save()
    print scanned_card_master.card_front
    # print scanned_card_master_serializer.card_front
    locale, descriptions = get_card_ocr_data(scanned_card_master=scanned_card_master)
    #
    # scanned_card_master.locale = locale
    # scanned_card_master.save()
    return Response("kkk", status=status.HTTP_400_BAD_REQUEST)

    scanned_card_detail_list = []
    for item in descriptions:
        if not item:
            continue
        scanned_card_detail = ScannedCardDetail()
        scanned_card_detail.scanned_card = scanned_card_master
        scanned_card_detail.text = item
        scanned_card_detail.bounding_cortdinate = ''
        scanned_card_detail.predicated_caption = 0
        scanned_card_detail.save()
        scanned_card_detail_list.append(scanned_card_detail)

    print scanned_card_master.id

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