from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from website.models import Site, UserRecords, Tasks
from website.serializer import SiteSerializer, UserRecordsSerializer, InitiateTaskSerializer
from website.tasks import task_map

class UserRecordsLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class SiteViewSet(ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class UserRecordViewSet(ModelViewSet):
    queryset = UserRecords.objects.all()
    serializer_class = UserRecordsSerializer
    pagination_class = UserRecordsLimitOffsetPagination

    def get_queryset(self):
        queryset = UserRecords.objects.all()
        site_id = self.request.query_params.get('site_id', None)
        if site_id:
            queryset = queryset.filter(site_id=site_id)
        return queryset

    @action(detail=False, methods=['POST'], url_path='(?P<site_id>.+)/initiate-task')
    def initiate_task(self, request, site_id, *args, **kwargs):
        serializer = InitiateTaskSerializer(data=request.data)
        serializer.check_site_id(site_id)

        if serializer.is_valid():
            task_name = serializer.validated_data.get('task_name')
            task_function = task_map.get(task_name)
            
            if not task_function:
                return Response({"detail": "Invalid task_name"}, status=400)

            task_record = Tasks.objects.create(
                site_id=site_id,
                task_name=task_name,
                status=Tasks.PENDING,
                execution_time=0,
            )

            task_queue = task_record.get_task_priority()
            task_function.apply_async((site_id, task_record.id), queue=task_queue)
            return Response({"detail": "Task initiated"}, status=200)
        else:
            return Response(serializer.errors, status=400)