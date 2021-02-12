from django.shortcuts import render
from django.db import IntegrityError, transaction
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import  api_view, action
import json
# models
from .models import *
# serializers
from .serializers import *
# api response pattern 
from mysite.apiResponse import prepareResponse
# Create your views here.

class testViewApi(viewsets.ModelViewSet):
    serializer_class = TestModelApiSerializer
    @action(detail=True, methods=['POST'])
    def records(self, request):
        # GET total records
        items = TestModelApi.objects.all()

        # create pagination
        post = json.loads(request.body)
        start = (post['page'] - 1) * 30
        end = start + 30

        # sort update
        if post['sort']['order'] == False:
            post['sort']['type'] = "-" + post['sort']['type']

        # search for the data
        if len(post['search']) >= 1:
            items = items.filter(Q(name__contains=post['search'][0]))

        total = items.count()
        # GET all records from the table
        items = items.order_by(
            post['sort']['type'])[start:end]

        serializer = TestModelApiSerializer(items, many=True)
        # return the data
        return Response(prepareResponse({"total": total, "page": post['page'], "count": items.count()}, [], True, 'data returned successfuly', []))

    @action(detail=True, methods=['GET'])
    def record(self, request, id=None):
        """
        GET record by id .
        """
        if request.method == "GET":
            # GET records from table
            item = TestModelApi.objects.filter(
                id=id).first()
            if item:
                serializer = TestModelApiSerializer(item, many=False)
                return Response(
                    prepareResponse(
                        [], serializer.data, True, "data returned successfuly", []
                    )
                )
            # if record not found
            else:
                return Response(prepareResponse([], [], False, "Record not found", []), 404)

    @action(detail=True, methods=['DELETE'])
    @transaction.atomic
    def delete(self, request, id=None):
        """
        delete records by id .
        """
        try:
            # GET records from table
            item = TestModelApi.objects.filter(
                id=id).first()
            if item:
                with transaction.atomic():
                    # delete record
                    TestModelApi.objects.filter(id=id).update(state="Deleted")
                    return Response(
                        prepareResponse(
                            [], [], True, "Record deleted", []), 201
                    )
            # if record not found
            else:
                return Response(
                    prepareResponse([], [], False, "Record not found", []), 404
                )
        except Exception as error:
            return Response(
                prepareResponse(
                    [], [], False, "Please refresh your token", []), 401
            )

    @action(detail=True, methods=['POST'])
    @transaction.atomic
    def update(self, request, id=None):
        """
        update records by id .
        """

        # GET records from table
        item = TestModelApi.objects.get(id=id)

        try:
            if item:
                # update all from post
                for attr, value in list(request.data.items()):
                    # if field is allowed
                    if attr not in TestModelApi.protected():
                        setattr(item, attr, value)
                try:
                    with transaction.atomic():
                        # save data
                        item.save()

                    # GET new data
                    serializer = TestModelApiSerializer(item, many=False)
                    # retuen new data
                    return Response(
                        prepareResponse(
                            [], [], True, "Record updated", []), 201
                    )

                except Exception as errors:

                    # return valiation error
                    return Response(
                        prepareResponse(
                            [], [], False, "Unprocessable entity", errors),
                        422,
                    )
            # if record not found
            else:
                return Response(
                    prepareResponse([], [], False, "Record not found", []), 404
                )
        except Exception as error:
            return Response(
                prepareResponse(
                    [], [], False, "Please refresh your token", []), 401
            )

    @action(detail=True, methods=['POST'])
    @transaction.atomic
    def create(self, request):
        """
        create new records  .
        """
        try:
            item = TestModelApi()
            # create all from post
            for attr, value in list(request.data.items()):
                # if field is allowed
                if attr not in TestModelApi.protected():
                    setattr(item, attr, value)
                # set uuid
            with transaction.atomic():
                # save data
                item.save()
                # GET new data
                serializer = TestModelApiSerializer(item, many=False)
                # retuen new data
                return Response(
                    prepareResponse(
                        [], serializer.data, True, "Record created", []
                    ),
                    201,
                )

        except Exception as errors:

            return Response(
                prepareResponse(
                    [], [], False, "Unprocessable entity", errors
                ),
                422,
            )

