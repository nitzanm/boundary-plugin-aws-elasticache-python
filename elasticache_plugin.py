import boto
import boto.elasticache
import sys

from boundary_aws_plugin.cloudwatch_plugin import CloudwatchPlugin
from boundary_aws_plugin.cloudwatch_metrics import CloudwatchMetrics


class ElasticacheCloudwatchMetrics(CloudwatchMetrics):
    def __init__(self, access_key_id, secret_access_key):
        return super(ElasticacheCloudwatchMetrics, self).__init__(access_key_id, secret_access_key, 'AWS/ElastiCache')

    def get_region_list(self):
        # Some regions are returned that actually do not support Elasticache.  Skip those.
        return [r for r in boto.elasticache.regions() if r.name not in ['cn-north-1', 'us-gov-west-1']]

    def get_entities_for_region(self, region):
        ec = boto.elasticache.connect_to_region(region.name, aws_access_key_id=self.access_key_id,
                                                aws_secret_access_key=self.secret_access_key)
        return ec.describe_cache_clusters()['DescribeCacheClustersResponse']['DescribeCacheClustersResult']['CacheClusters']

    def get_entity_source_name(self, cache):
        return cache['CacheClusterId']

    def get_entity_dimensions(self, region, cache):
        return dict(CacheClusterId=cache['CacheClusterId'])

    def get_metric_list(self):
        return (
            ('HealthyHostCount', 'Average', 'AWS_ELB_HEALTHY_HOST_COUNT'),
            ('UnHealthyHostCount', 'Average', 'AWS_ELB_UNHEALTHY_HOST_COUNT'),
            ('RequestCount', 'Sum', 'AWS_ELB_REQUEST_COUNT'),
            ('Latency', 'Average', 'AWS_ELB_LATENCY'),
            ('HTTPCode_ELB_4XX', 'Sum', 'AWS_ELB_HTTP_CODE_4XX'),
            ('HTTPCode_ELB_5XX', 'Sum', 'AWS_ELB_HTTP_CODE_5XX'),
            ('HTTPCode_Backend_2XX', 'Sum', 'AWS_ELB_HTTP_CODE_BACKEND_2XX'),
            ('HTTPCode_Backend_3XX', 'Sum', 'AWS_ELB_HTTP_CODE_BACKEND_3XX'),
            ('HTTPCode_Backend_4XX', 'Sum', 'AWS_ELB_HTTP_CODE_BACKEND_4XX'),
            ('HTTPCode_Backend_5XX', 'Sum', 'AWS_ELB_HTTP_CODE_BACKEND_5XX'),
            ('BackendConnectionErrors', 'Sum', 'AWS_ELB_BACKEND_CONNECTION_ERRORS'),
            ('SurgeQueueLength', 'Maximum', 'AWS_ELB_SURGE_QUEUE_LENGTH'),
            ('SpilloverCount', 'Sum', 'AWS_ELB_SPILLOVER_COUNT'),
        )


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        import logging
        logging.basicConfig(level=logging.INFO)

    plugin = CloudwatchPlugin(ElasticacheCloudwatchMetrics, '', 'boundary-plugin-aws-elb-python-status')
    plugin.main()

