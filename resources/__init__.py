# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.backgroud_jobs import BackgroundJobsResource
from resources.backgroud_jobs_restart import BackgroundJobsRestartResource
from resources.health_check import HealthCheck
from resources.hello import HelloWorld
from resources.iapi import iapi_resources


api_resources = {
    '/hello': HelloWorld,
    '/common/health_check': HealthCheck,
    **{f'/iapi{k}': val for k, val in iapi_resources.items()},
    '/background_jobs': BackgroundJobsResource,
    '/background_jobs/restart': BackgroundJobsRestartResource,
    
}
