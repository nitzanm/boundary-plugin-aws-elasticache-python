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
            ('CPUUtilization', 'Average', 'NEM_AWS_ELASTICACHE_CPU_UTILIZATION'),
            ('SwapUsage', 'Average', 'NEM_AWS_ELASTICACHE_SWAP_USAGE'),
            ('FreeableMemory', 'Average', 'NEM_AWS_ELASTICACHE_FREEABLE_MEMORY'),
            ('NetworkBytesIn', 'Sum', 'NEM_AWS_ELASTICACHE_NETWORK_BYTES_IN'),
            ('NetworkBytesOut', 'Sum', 'NEM_AWS_ELASTICACHE_NETWORK_BYTES_OUT'),
            ('CurrConnections', 'Average', 'NEM_AWS_ELASTICACHE_REDIS_CURR_CONNECTIONS'),
            ('Evictions', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_EVICTIONS'),
            ('Reclaimed', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_RECLAIMED'),
            ('NewConnections', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_NEW_CONNECTIONS'),
            ('BytesUsedForCache', 'Average', 'NEM_AWS_ELASTICACHE_REDIS_BYTES_USED_FOR_CACHE'),
            ('CacheHits', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_CACHE_HITS'),
            ('CacheMisses', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_CACHE_MISSES'),
            ('ReplicationLag', 'Average', 'NEM_AWS_ELASTICACHE_REDIS_REPLICATION_LAG'),
            ('GetTypeCmds', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_GET_TYPE_CMDS'),
            ('SetTypeCmds', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_SET_TYPE_CMDS'),
            ('KeyBasedCmds', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_KEY_BASED_CMDS'),
            ('StringBasedCmds', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_STRING_BASED_CMDS'),
            ('HashBasedCmds', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_HASH_BASED_CMDS'),
            ('ListBasedCmds', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_LIST_BASED_CMDS'),
            ('SetBasedCmds', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_SET_BASED_CMDS'),
            ('SortedSetBasedCmds', 'Sum', 'NEM_AWS_ELASTICACHE_REDIS_SORTED_SET_BASED_CMDS'),
            ('CurrItems', 'Average', 'NEM_AWS_ELASTICACHE_REDIS_CURR_ITEMS'),
            ('BytesUsedForCacheItems', 'Average', 'NEM_AWS_ELASTICACHE_MEMCACHED_BYTES_USED_FOR_CACHE_ITEMS'),
            ('BytesReadIntoMemcached', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_BYTES_READ_INTO_MEMCACHED'),
            ('BytesWrittenOutFromMemcached', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_BYTES_WRITTEN_OUT_FROM_MEMCACHED'),
            ('CasBadval', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_CAS_BADVAL'),
            ('CasHits', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_CAS_HITS'),
            ('CasMisses', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_CAS_MISSES'),
            ('CmdFlush', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_CMD_FLUSH'),
            ('CmdGet', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_CMD_GET'),
            ('CmdSet', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_CMD_SET'),
            ('CurrConnections', 'Average', 'NEM_AWS_ELASTICACHE_MEMCACHED_CURR_CONNECTIONS'),
            ('CurrItems', 'Average', 'NEM_AWS_ELASTICACHE_MEMCACHED_CURR_ITEMS'),
            ('DecrHits', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_DECR_HITS'),
            ('DecrMisses', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_DECR_MISSES'),
            ('DeleteHits', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_DELETE_HITS'),
            ('DeleteMisses', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_DELETE_MISSES'),
            ('Evictions', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_EVICTIONS'),
            ('GetHits', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_GET_HITS'),
            ('GetMisses', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_GET_MISSES'),
            ('IncrHits', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_INCR_HITS'),
            ('IncrMisses', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_INCR_MISSES'),
            ('Reclaimed', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_RECLAIMED'),
            ('BytesUsedForHash', 'Average', 'NEM_AWS_ELASTICACHE_MEMCACHED_BYTES_USED_FOR_HASH'),
            ('CmdConfigGet', 'Average', 'NEM_AWS_ELASTICACHE_MEMCACHED_CMD_CONFIG_GET'),
            ('CmdConfigSet', 'Average', 'NEM_AWS_ELASTICACHE_MEMCACHED_CMD_CONFIG_SET'),
            ('CmdTouch', 'Average', 'NEM_AWS_ELASTICACHE_MEMCACHED_CMD_TOUCH'),
            ('CurrConfig', 'Average', 'NEM_AWS_ELASTICACHE_MEMCACHED_CURR_CONFIG'),
            ('EvictedUnfetched', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_EVICTED_UNFETCHED'),
            ('ExpiredUnfetched', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_EXPIRED_UNFETCHED'),
            ('SlabsMoved', 'Average', 'NEM_AWS_ELASTICACHE_MEMCACHED_SLABS_MOVED'),
            ('TouchHits', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_TOUCH_HITS'),
            ('TouchMisses', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_TOUCH_MISSES'),
            ('NewConnections', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_NEW_CONNECTIONS'),
            ('NewItems', 'Sum', 'NEM_AWS_ELASTICACHE_MEMCACHED_NEW_ITEMS'),
            ('UnusedMemory', 'Average', 'NEM_AWS_ELASTICACHE_MEMCACHED_UNUSED_MEMORY'),
        )


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        import logging
        logging.basicConfig(level=logging.INFO)

    plugin = CloudwatchPlugin(ElasticacheCloudwatchMetrics, '', 'boundary-plugin-aws-elasticache-python-status')
    plugin.main()

