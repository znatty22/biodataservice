"""
Views for endpoints that are not part of the biodata CRUD API
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.db import models
import django_rq
from rq.job import Job, NoSuchJobError, JobStatus
from redis import Redis

from biodata.api import models as m

DISTINCT_VAL_THRESHOLD = 15


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint
    """
    return Response(
        {
            'message': 'Welcome to the Biodataservice API',
            'status': status.HTTP_200_OK
        }
    )


def summary_task(study_id):
    """
    Collect stats for a study: total count for each entity and distinct
    values per entity attribute
    """
    def entity_stats(model_cls):
        stats = {
            'total': model_cls.objects.count(),
        }
        distincts = {}
        for f in model_cls._meta.fields:
            if not isinstance(f, models.ForeignKey):
                ds = {
                    value
                    for value, *_ in
                    model_cls.objects.values_list(f.attname).distinct()
                }
                if len(ds) > DISTINCT_VAL_THRESHOLD:
                    ds = 'Too many distinct values to list'

                distincts[f.attname] = ds

        stats['distinct_values'] = distincts

        return stats

    return {
        'study_id': study_id,
        'stats': {
            m.Participant.__name__: entity_stats(m.Participant),
            m.Biospecimen.__name__: entity_stats(m.Biospecimen)
        }
    }


@api_view(['GET'])
def summary(request, study_id):
    """
    Endpoint to compute study stats in async task
    """
    try:
        study = m.Study.objects.get(kf_id=study_id)
    except m.Study.DoesNotExist:
        return Response({
            'message': f'Could not compute stats! Study {study_id}'
        }, status=status.HTTP_404_NOT_FOUND)

    def job_id(study_id):
        return f'{study_id}-summary-job'

    q = django_rq.get_queue('biodataservice')

    print(f'Jobs in queue: {q.job_ids}')

    # Look for existing job
    try:
        job = q.fetch_job(job_id(study_id))
    except NoSuchJobError:
        print('Job does not exist')
        job = None

    # No job yet, or job previous failed
    if (not job) or (job and job.get_status() == JobStatus.FAILED):
        job = q.enqueue(
            summary_task, args=(study_id,), job_id=job_id(study_id),
            result_ttl=10
        )
        print(f'Submitted new job: {job.id}')

        return Response({
            'message': f'Submitted status computation for {study_id}'
        })
    # Try getting result from the job if it finished
    else:
        try:
            return Response(job.result)
        except AttributeError:
            return Response({
                'message': f'Stats computation for {study_id} not complete '
                'yet! Check back soon!'
            })
